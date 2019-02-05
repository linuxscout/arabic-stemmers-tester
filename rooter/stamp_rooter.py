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
import roots_const
import re
#create index  by word stampfor dictionary to accelerate word search.
# the word stamp is the arabic word without any affixation  letters,
# for example
# the word قالب give قلب, by removing meem and beh, the word قوالب give قلب.
# the stamp is used as a first level of indexing, especially
# for verbs
# the stamp pattern is used to create the word stamp
        
class stampRooter(abstractRooter):
    def __init__(self,):
        abstractRooter.__init__(self)
        self.stamp_pat = re.compile(u"[%s%s%s%s%s%s%s%s%s%s]"% (araby.ALEF, 
    araby.YEH, araby.HAMZA, araby.ALEF_HAMZA_ABOVE, araby.WAW_HAMZA,
     araby.YEH_HAMZA, araby.WAW, araby.ALEF_MAKSURA, araby.SHADDA, araby.TEH ), 
     re.UNICODE)         
        self.STAMP_DICT   ={}
        self.create_stamped_roots()

    def stamp_root(self, word):
        """ stamp root"""
        return self.word_stamp(word)


    def word_stamp(self, word):
        """
        generate a stamp for a word, 
        remove all letters which can change form in the word :
            - ALEF, 
            - HAMZA, 
            - YEH, 
            - WAW, 
            - ALEF_MAKSURA
            - SHADDA
        @return: stamped word
        """
        word = self.stamp_pat.sub('', word)
        # strip the last letter if is doubled
        if word[-1:] ==  word[-2:-1]:
            word = word[:-1]
        return word


    
    def create_stamped_roots(self, ):
        if  self.STAMP_DICT:
            return

        for root in roots_const.ROOTS:
            stmp =  self.word_stamp(root)
            #~ if stmp != root:
            if stmp in  self.STAMP_DICT:
                 self.STAMP_DICT[stmp].append(root)
            else:
                 self.STAMP_DICT[stmp]= [root,]
    #~ def is_stamped_root(self, word):
    def extract(self, word):
        """ test if word is a stop"""
        # calcul the stamp
        stmp =  self.word_stamp(word)
        # lookup for stamp roots
        return  self.STAMP_DICT.get(stmp, [])
