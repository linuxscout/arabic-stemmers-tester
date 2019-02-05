#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  stopclass.py
#  
#  Copyright 2018 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
import pyarabic.araby as araby
from abstract_rooter import abstractRooter
import re
import itertools

AFFIXATION_LETTERS = u"أابةتدسطفكلمنهويءئى"
        
class matrixRooter(abstractRooter):
    def __init__(self,):
        abstractRooter.__init__(self)

    def extract(self, word, affixation_letters = AFFIXATION_LETTERS):
        """ extract all possibles roots as matrix """
        # create the matrix columns values size
        # if the word has n character, the columns size is n
        # every columns has a number of poosible values,
        # if the letter is original, the columns correspaneding to this letters has 1 case
        # if the letter can be added, the columns takes two values (original, added)
        # Qal => 1 2 1
        # the number of possible cases is 1*2*1 
        # Qwl and Qyl
        # for ktab => 2,2,2,1 => number of rows is 8 cases
        # k t a b
        # 0 0 0 1 => b
        # 0 0 1 1 => ab
        # 0 1 0 1 => tb
        # 0 1 1 1 => tab
        # 1 0 0 1 => kb
        # 1 0 1 1 => kab
        # 1 1 0 1 => ktb
        # 1 1 1 1 => ktab
        # If we consider that 'a' can be 'w' or 'y' we can get more cases.
        # we can elimine more the 4 letters root cases.
        cards = [] # cardinalities
        #~ affixation_letters = u"أابةتدسطفكلمنهويءئى"
        #~ affixation_letters = u"أابةتدسطفكلمنهويءئى"
        chunks = []
        # previous letter, used to handle some special case
        previous = ""
        for c in word:

            # only added
            if c in (araby.TEH_MARBUTA, ):
               chunks.append(['-'])

            elif c in affixation_letters:
                # can be added with alteration
                if c in (araby.ALEF, araby.WAW, araby.YEH):
                    chunks.append(['-', araby.WAW, araby.YEH])
                # alterned 
                elif c in (araby.ALEF_MAKSURA, ):
                    chunks.append(['-', araby.YEH])
                elif c in araby.HAMZAT:
                    chunks.append(['-', araby.HAMZA])
                # conditional
                elif c == araby.DAL:
                    if previous == araby.ZAIN:
                        chunks.append(['-', c])
                    else:
                        chunks.append([c])
                elif c == araby.TAH:
                    if previous == araby.DAD:
                        chunks.append(['-', c])
                    else:
                        chunks.append([c])
                # added not alterned
                else:
                    chunks.append(['-', c])
            else:
                # alterned  and normalized 
                if c in (araby.YEH_HAMZA, ):
                    chunks.append([araby.YEH, araby.WAW, araby.HAMZA]) 
                # normalized
                elif c in araby.HAMZAT:
                    chunks.append([araby.HAMZA])
                # alterned 
                elif c in (araby.ALEF_MAKSURA, ):
                    chunks.append([araby.YEH])                
                # ordinary
                else:
                    chunks.append([c])
            previous = c
        # make matrix and cardinalities
        matrix = []
        for ch in chunks:
            cards.append(len(ch))
            matrix.append(range(len(ch)))
        matrix =  list(itertools.product(*matrix))
        #~ logger.debug("Cardinalities %s",cards)
        #~ logger.debug("Chunks %s" , arepr(chunks))
        #~ logger.debug("Matrix %d", len(matrix))
        #~ for ch in matrix:
            #~ print(ch)

        chunks_root =  itertools.product(*chunks)
        templates_list = []
        # generate all cases
        for ch in chunks_root:
            temp = {"word": word, 
                "template":u''.join(ch), 
                'root':u''.join([x for  x in ch if x!='-']),
                }
            templates_list.append(temp)
        # filter by root length
        templates_list = [ d for d in templates_list if len(d['root']) <=4 ]
        incompleted_templates_list = [ d for d in templates_list if len(d['root']) <3 ]
        #~ self.debug_algo2(u"Incomplete Templates List ", arepr(incompleted_templates_list))

        ext_list = self.extend_matrix(incompleted_templates_list)
        
        #~ logger.debug("Templates %d", len(templates_list))
        #~ self.debug_algo2(u"Templates List ",arepr(templates_list))
        #~ self.debug_algo2(u"Extented Templates List ",arepr(ext_list))
        templates_list.extend(ext_list)
        return templates_list
    @staticmethod
    def extend_matrix(temp_list):
        """
        Extend roots according to templates
        """
        new_temp_list =[]
        for item in temp_list:
            psudoroot = item['root']
            temp = item['template']
            reduced = re.sub('^[-]+','',temp)
            reduced = re.sub('[-]+$','',reduced)
            extended = []
            if len(reduced) == 2 and len(psudoroot) == 2:
                # add Yeh or waw at begin
                extended.append(araby.WAW + psudoroot)
                extended.append(araby.YEH + psudoroot)
                # add Yeh or waw at middle
                extended.append("".join([psudoroot[0],araby.WAW, psudoroot[1]]))
                extended.append("".join([psudoroot[0],araby.YEH, psudoroot[1]]))
                # add Yeh or waw at end
                extended.append(psudoroot+araby.WAW)
                extended.append(psudoroot+araby.YEH)
                # add double letter جد =>جدد
                extended.append(psudoroot + psudoroot[-1:])
            for ext_root in extended:
                new_temp_list.append({'root':ext_root,
                'template':temp,
                'word':item["word"],
                'reduced':reduced,
                })
                
        return new_temp_list  
