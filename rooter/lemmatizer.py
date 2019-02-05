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
from pyarabic import stack
from pyarabic.araby import FEH, LAM, AIN, HARAKAT
import lemma_const
from pyarabic.arabrepr import arepr
import re
#create index  by word stampfor dictionary to accelerate word search.
# the word stamp is the arabic word without any affixation  letters,
# for example
# the word قالب give قلب, by removing meem and beh, the word قوالب give قلب.
# the stamp is used as a first level of indexing, especially
# for verbs
# the stamp pattern is used to create the word stamp
   
WAZNS = {
         u"إفاع":["add_teh_marbuta",],
         u"إفعال":["normalize_hamza",],
         u'فتعال':["add_alef_noun", "normalize_hamza"],
         u'ستفعال':["add_alef_noun", "normalize_hamza"],
         u'نفعال':["add_alef_noun", "normalize_hamza"],
         #~ u'فعال':["add_alef_hamza_noun", "normalize_hamza"],

         u'فتعل':["add_alef",],
         u'فتع':["add_alef",  #"add_alef_maksura"
         ],
         u'فتيل':["add_alef","change_yeh"],
        u"نفعل":["add_alef",],
        u"نفع":["add_alef", 
        #~ "add_alef_maksura"
        ],
        u"نفيل":["add_alef","change_yeh"],
         u'ستفيل':["add_alef","change_yeh"],
         u'ستفعل':["add_alef", "change_yeh"],
         u'ستفع':["add_alef", 
         #~ "add_alef_maksura"
         ],
         #~ u"أفعال":["normalize_hamza",],
         

         }

class lemmaDict:
    """ a class to handle lemmas"""
    def __init__(self,):
        #~ self.debug = True
        self.debug = False
        pass

    @staticmethod
    def waznlike2(word1, wazn, extract_root = False):
        u"""If the  word1 is like a wazn (pattern),
        the letters must be equal,
        the wazn has FEH, AIN, LAM letters.
        this are as generic letters.
        The two words can be full vocalized, or partial vocalized

        Example:
            >>> word1 = u"ضارب"
            >>> wazn = u"فَاعِل"
            >>> araby.waznlike(word1, wazn)
            True

        @param word1: input word
        @type word1: unicode
        @param wazn: given word template  وزن
        @type wazn: unicode
        @param extract_root: return the root
        @type extract_root: unicode
        @return: if two words have similar vocalization
        @rtype: Boolean
        """
        stack1 = stack.Stack(word1)
        stack2 = stack.Stack(wazn)
        root = stack.Stack()
        last1 = stack1.pop()
        last2 = stack2.pop()
        vowels = HARAKAT
        while last1 != None and last2 != None:
            if last1 == last2 and last2 not in (FEH, AIN, LAM):
                last1 = stack1.pop()
                last2 = stack2.pop()
            elif last1 not in vowels and last2 in (FEH, AIN, LAM):
                root.push(last1)
                #~ print "t"
                last1 = stack1.pop()
                last2 = stack2.pop()
            elif last1 in vowels and last2 not in vowels:
                last1 = stack1.pop()
            elif last1 not in vowels and last2 in vowels:
                last2 = stack2.pop()
            else:
                break
        # reverse the root letters
        root.items.reverse()
        #~ print " the root is ", root.items#"".join(root.items)
        if not (stack1.is_empty() and stack2.is_empty()):
            return False
        # if one letter is remind after pop in one stack
        elif last1 != None or last2 != None:
            return False
        else:
            #~ print (u"word '%s' , wazn ='%s'"%(u"".join(stack1.items),u"".join(stack2.items))).encode('utf8') 
            if extract_root:
                return "".join(root.items)
            else:
                return True

    def get_wazn(self, stem):
        """ validate stem agnaist Schemes أوزان"""
        for wazn in WAZNS:
            #~ if araby.waznlike(starword,wazn):
            if len(wazn) == len(stem):
                if self.waznlike2(stem, wazn):
                    return wazn
        return ""

    def choose_stem(self, affixa_list):
        """ select a stem to return """
        stems = [d['stem'] for d in affixa_list]
        stems = list(set(stems))
        #~ ajust = False; # add ajust stems
        ajust = True; # add ajust stems
        # choose a stem
        self.log(affixa_list, "affix lists filtred")
        self.log(stems, "stems list")        

        #~ return self.get_stem()
        # return the shortest
        stem = min(stems, key=len)
        chosen_affixa = [d for d in affixa_list if d['stem'] == stem]
        if ajust:
            for aff in chosen_affixa:
                aff["stem"] = self.ajust_lemma(aff)
        #~ print(arepr(chosen_affixa))
        #choose the first one,
        # todo choose best one
        stem = chosen_affixa[0]['stem']
        return stem
    def ajust_lemma(self, affixa):
        """ ajust lemma from stems"""
        
        # add Alef for some verbs
        prefix = affixa['prefix']
        suffix = affixa['suffix']
        #~ suffix = affixa['suffix']
        stem = affixa['stem']

        # get wazn like
        wazn = self.get_wazn(stem)
        if wazn:
            actions = WAZNS[wazn]
            stem = self.do_actions(stem, actions, prefix, suffix)
            #~ print(actions)

        stem = self.ajust_supplements(stem, prefix, suffix)
        
        return stem
    def log(self, data, msg=""):
        """ display internal data"""
        if not self.debug:
            return False
        else:
            print(msg)
            print(arepr(data))

    def do_actions(self, stem, actions, prefix, suffix):
        """ do action by name """
        if  "add_alef" in actions:
            if prefix[-1:] in (araby.YEH, araby.NOON, araby.TEH, araby.ALEF_HAMZA_ABOVE, araby.ALEF):
                stem = araby.ALEF + stem
        if  "add_alef_noun" in actions:
            if prefix[-1:] in (araby.ALEF,):
                stem = araby.ALEF + stem
        #~ if  "add_alef_hamza_noun" in actions:
            #~ if prefix[-1:] in (araby.ALEF_HAMZA_ABOVE,):
                #~ stem = araby.ALEF + stem
        if "add_alef_maksura" in actions:
            stem += araby.ALEF_MAKSURA
        if "change_yeh" in actions:
            # ستطيع ="ستطاع
            # if before last letter
            beforelast = stem[-2:-1]
            if beforelast ==araby.YEH:
                stem = stem[:-2]+ araby.ALEF+stem[-1:]
        if "add_teh_marbuta" in actions:
            #~ if suffix.startswith(araby.TEH_MARBUTA) or suffix.startswith(araby.TEH):
                #~ stem += araby.TEH_MARBUTA
            stem += araby.TEH_MARBUTA
        if "normalize_hamza" in actions:
            last = stem[-1:]
            if last in (araby.YEH_HAMZA, araby.WAW_HAMZA):
                stem = stem[:-1]+ araby.HAMZA
                
        return stem

    def ajust_supplements(self, stem, prefix, suffix):
        """ do action by name """
        # supplements action
        #~ # قضائ، فضائ، كهربائي
        if stem.endswith(araby.ALEF+ araby.YEH_HAMZA) or stem.endswith(araby.ALEF+ araby.WAW_HAMZA):
            stem = stem[:-1] + araby.HAMZA
        #~ # ة أو ات
        #~ if suffix.startswith(araby.TEH_MARBUTA) or suffix.startswith(araby.ALEF +araby.TEH):
        #~ if suffix.startswith(araby.TEH_MARBUTA) :#or suffix.startswith(araby.ALEF +araby.TEH):
            #~ stem += araby.TEH_MARBUTA
        return stem
    def is_valid_verb_stem(self,stem, prefix, suffix):
        """validate verb form """
        # control on length
        if len(stem) > 6:
            return False
        else:
            #الفعل السداسي على وزن استفعل
            if len(stem)== 6 and not stem.startswith(araby.ALEF):
                return False
            #الفعل الخماسي
            # انفعل، افتعل، تفاعل، تفعلل
            # ستفعل من استفعل
            elif len(stem)== 5 and not (stem.startswith(araby.ALEF) or 
                 stem.startswith(araby.TEH) or
                  #~ stem.startswith(araby.SEEN)):
                  stem.startswith(araby.SEEN+araby.TEH)):
                return False
        invalid_letters = (araby.TEH_MARBUTA, araby.ALEF_HAMZA_BELOW)
        for c in invalid_letters:
            if c in stem:
                return False
        if stem.startswith(araby.ALEF) and  prefix[-1:] in (araby.YEH, araby.NOON, araby.TEH, araby.ALEF_HAMZA_ABOVE, araby.ALEF):
            return False
        return True
    def is_valid_noun_stem(self,stem, prefix, suffix):
        """validate noun form """
        return True

