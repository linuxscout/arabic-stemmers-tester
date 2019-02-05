#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  abstractstemmer.py
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
import re
import pyarabic.araby as araby
import tashaphyne.stemming
import tashaphyne.stem_const
import abstract_stem_const as absconst 
from stopwords.arabicstopwords import is_stop, stop_stem, stop_root
from pyarabic.arabrepr import arepr
CUSTOM_SUFFIX_LIST = absconst.STEMMING_SUFFIX_LIST
CUSTOM_PREFIX_LIST = absconst.STEMMING_PREFIX_LIST

NOUN_PREFIX_LIST = absconst.NOUN_PREFIX_LIST
NOUN_SUFFIX_LIST = absconst.NOUN_SUFFIX_LIST
VERB_PREFIX_LIST = absconst.VERB_PREFIX_LIST
VERB_SUFFIX_LIST = absconst.VERB_SUFFIX_LIST
ALEFAT_PAT = re.compile(u"["+u"".join([araby.ALEF_MADDA, araby.ALEF_HAMZA_ABOVE,
                                       araby.ALEF_HAMZA_BELOW, araby.HAMZA_ABOVE,
                                       araby.HAMZA_BELOW])+u"]")
                                    
def normalize_alef(word):
    """
    Normalize HAMZAT to ALEF
    """
    return ALEFAT_PAT.sub(araby.ALEF, word)
#~ import rootslib
import rootslibclass

#Define an abstract Class for stemmer
class abstractStemmer(tashaphyne.stemming.ArabicLightStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        tashaphyne.stemming.ArabicLightStemmer.__init__(self)
        self.config = {"affix":"default",
                        "root_dict":"no",
                        "stop_words":"no",
        }
        self.debug_root = False
    def help(self,):
        return repr(self.config)
    def getstem(self, word):
        """ get a stem from word"""
        return self.light_stem(word)
    def getroot(self, word):
        """ get a stem from word"""
        self.light_stem(word)
        return self.get_root()
    def verify_affix(self,affix_list):
        pass
    def verify_roots(self, root_list):
        pass
        
        
class customStemmer_roots(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self)
        infixes_letters_custom = u"توطيدا"
        self.set_infix_letters(infixes_letters_custom)
        self.config["root_dict"] = "yes"
        self.rootdict = rootslibclass.rootDict()
    
    def getstem(self,word):
        """ get a stem from word"""
        if not is_stop(word):
            return self.light_stem(word)
        else:
            return stop_stem(word)
    def getroot(self,word):
        """ get a stem from word"""
        if not is_stop(word):
            word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
            self.light_stem(word)
            self.segment(word)
            affixation_list = self.get_affix_list()
            # filter valid affixes
            affixation_list = filter(self.verify_affix, affixation_list)

            #~ root_result = rootslib.choose_root(affixation_list)
            root_result = self.rootdict.choose_root(word, affixation_list, self.debug_root)
            if root_result:
                return root_result
            else:
                return self.get_root()

        else:
            return stop_root(word)
    def verify_affix(self, affix_tuple):
        #مراجعة مبسطة
        # أل التعريف مع ضمير متصل
        prefix = affix_tuple.get('prefix', '')
        suffix = affix_tuple.get('suffix', '')
        if ((u"ال" in prefix or u"لل" in prefix) and 
            (u'ه' in suffix or u'ك' in suffix)
            ):
                return False
        # حروف الجر مع واو جمع مذكر سالم
        #ولمثنى المرفوع
        if ((u"ك" in prefix or u"ب" in prefix or u"لل" in prefix) and 
            (u'و' in suffix or u'ان' in suffix)
            ):
                return False
        return True

        
class customStemmer_roots_rhyzome(customStemmer_roots):
    """ I will make more options for stemmer """
    def __init__(self,):
        customStemmer_roots.__init__(self)
        self.rootdict.algos = ['rhyzome']

        
    
def main(args):
    word = u"يستعملونهم"
    words = [u"بساكنيها", u"وسواكنها",u"يستعملونها", u"يندرجون",
    u'ينتقي',
    u"يقترب",
    u"يغتر",
    u"يستمر",  
    u"يستهينهم",
    u'ويستنفرهم', u'ويستعملهم', u'ويستقدمهم', u'ويستهينهم', u'ويستغلهم', u'ويستعلمهم', u'ويستفزهم', u'يطعهم', u'يستملهم', u'ويطعهم', u'ويستملهم', u'ويستميلهم', u'ويستحمهم', u'ويستحلهم', u'ويستحييهم', u'ويستدرجهم', u'ويستطرقهم', u'ويستنصرهم', u'ويستصرخهم', u'ويستعطفهم', u'ويستنكحهم', u'ويستنزفهم', u'ويستكهلكه'      
    ]

    #~ for name in ('default', 'custom', 'isri', 'assem'):
    print(u'\t'.join(['stemmer','word', 'root', 'stem' ]))
    #~ names = factory_stemmer.get_stemmers()
    names = ['lemmatizer']
    for word in words: 
        for name in names:
            asl = factory_stemmer.create_stemmer(name);
            print(u'\t'.join([name,word, asl.getroot(word), asl.getstem(word) ]).encode('utf8'))
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
