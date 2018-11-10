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
from nltk.stem.isri import ISRIStemmer
import snowballstemmer.arabic_stemmer
import snowballstemmer_modified.arabic_stemmer 
import naftawayh.wordtag
from stopwords.arabicstopwords import is_stop, stop_stem, stop_root
from pyarabic.arabrepr import arepr
import lemmatizer
#~ CUSTOM_PREFIX_LIST = [u'كال', u'أفبال', u'أفك', u'فك', u'أولل', u'', u'أف', u'ول', u'أوال', u'ف', u'و', u'أو', u'ولل', u'فب', u'أول', u'ألل', u'لل', u'ب', u'وكال', u'أوب', u'بال', u'أكال', u'ال', u'أب', u'وب', u'أوبال', u'أ', u'وبال', u'أك', u'فكال', u'أوك', u'فلل', u'وك', u'ك', u'أل', u'فال', u'وال', u'أوكال', u'أفلل', u'أفل', u'فل', u'أال', u'أفكال', u'ل', u'أبال', u'أفال', u'أفب', u'فبال']
#~ CUSTOM_SUFFIX_LIST = [u'كما', u'ك', u'هن', u'ي', u'ها', u'', u'ه', u'كم', u'كن', u'هم', u'هما', u'نا']
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
        
#Define an abstract Class for stemmer
class multiStemmer(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        tashaphyne.stemming.ArabicLightStemmer.__init__(self)
        self.config = {"affix":"default",
                        "root_dict":"no",
                        "stop_words":"no",
        }
    def help(self,):
        return repr(self.config)
    def getstem(self, word):
        """ get a stem from word"""
        self.light_stem(word)
        self.segment(word)
        affixation_list = self.get_affix_list()
        stems = [ d['stem'] for d in affixation_list]
        stems = list(set(stems))
        stems = u";".join(stems)
        return stems
    def getroot(self, word):
        """ get a stem from word"""
        self.light_stem(word)
        self.segment(word)
        affixation_list = self.get_affix_list()
        roots = [ d['root'] for d in affixation_list]
        roots = list(set(roots))
        roots = u";".join(roots)
        return roots

        
class customStemmer(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self)
        #set 
        self.set_prefix_list(CUSTOM_PREFIX_LIST)
        self.set_suffix_list(CUSTOM_SUFFIX_LIST)
        self.config["affix"] = "custom"
    def getstem(self,word):
        """ get a stem from word"""
        #~ return self.light_stem(word)
        stem = self.light_stem(word)
        return normalize_alef(stem)        
    def getroot(self,word):
        """ get a stem from word"""
        self.light_stem(word)
        return self.get_root()
        
class customStemmer_affix_stp(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self)
        #set 
        self.set_prefix_list(CUSTOM_PREFIX_LIST)
        self.set_suffix_list(CUSTOM_SUFFIX_LIST)
        self.config["affix"] = "custom"
    def getstem(self,word):
        """ get a stem from word"""
        if not is_stop(word):

            return self.light_stem(word)
            
        else:
            return stop_stem(word)
    def getroot(self,word):
        """ get a stem from word"""
        self.light_stem(word)
        return self.get_root()

class customStemmer_lemmatizer(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self)
        #set 
        self.set_prefix_list(CUSTOM_PREFIX_LIST)
        self.set_suffix_list(CUSTOM_SUFFIX_LIST)
        self.config["affix"] = "custom"
        self.debug = False
        self.lemmatizer = lemmatizer.lemmaDict()
        
    def getstem(self,word):
        """ get a stem from word"""
        if not is_stop(word):
            word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
            self.light_stem(word)
            self.segment(word)
            affixation_list = self.get_affix_list()
            # filter valid affixes
            affixation_list = filter(self.verify_affix, affixation_list)

            return self.lemmatizer.choose_stem(affixation_list)
        else:
            return stop_stem(word)
    
        
    def log(self, data, msg=""):
        """ display internal data"""
        if not self.debug:
            return False
        print(msg)
        print(arepr(data))
    def getroot(self,word):
        """ get a stem from word"""
        self.light_stem(word)
        return self.get_root()
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
class customStemmer_lemmatizer_tag(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self)
        #set 
        self.set_prefix_list(CUSTOM_PREFIX_LIST)
        self.set_suffix_list(CUSTOM_SUFFIX_LIST)
        self.config["affix"] = "custom"
        self.debug = False
        self.lemmatizer = lemmatizer.lemmaDict()
        # tagger
        self.tagger = naftawayh.wordtag.WordTagger(); 
        # noun stemmer config
        # create stemmer
        self.noun_stemmer = abstractStemmer()
        # config prefix and suffix list
        self.noun_stemmer.set_prefix_list(NOUN_PREFIX_LIST)
        self.noun_stemmer.set_suffix_list(NOUN_SUFFIX_LIST)
        # verb stemmer config
        # create stemmer
        self.verb_stemmer = abstractStemmer()
        # config prefix and suffix list
        self.verb_stemmer.set_prefix_list(VERB_PREFIX_LIST)
        self.verb_stemmer.set_suffix_list(VERB_SUFFIX_LIST)             
        
    def getstem(self,word):
        """ get a stem from word"""
        if not is_stop(word):
            word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
            self.light_stem(word)
            self.segment(word)
            affixation_list = self.get_affix_list()
            # filter valid affixes
            affixation_list = filter(self.verify_affix, affixation_list)

            return self.lemmatizer.choose_stem(affixation_list)
        else:
            return stop_stem(word)
    
        
    def log(self, data, msg=""):
        """ display internal data"""
        if not self.debug:
            return False
        print(msg)
        print(arepr(data))
    def getroot(self,word):
        """ get a stem from word"""
        self.light_stem(word)
        return self.get_root()
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


class customStemmer_stp(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self)
        self.config["stop_words"] = "yes"  
    def getstem(self,word):
        """ get a stem from word"""
        if not is_stop(word):
            return self.light_stem(word)
        else:
            return stop_stem(word)
    def getroot(self,word):
        """ get a stem from word"""
        if not is_stop(word):
            self.light_stem(word)
            return self.get_root()
        else:
            return stop_root(word)
        
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

class customStemmer_roots_stamp(customStemmer_roots):
    """ I will make more options for stemmer """
    def __init__(self,):
        customStemmer_roots.__init__(self)
        self.rootdict.algos = ['stamp']
class customStemmer_roots_extend(customStemmer_roots):
    """ I will make more options for stemmer """
    def __init__(self,):
        customStemmer_roots.__init__(self)
        self.rootdict.algos = ['extend']
        
class customStemmer_roots_rhyzome(customStemmer_roots):
    """ I will make more options for stemmer """
    def __init__(self,):
        customStemmer_roots.__init__(self)
        self.rootdict.algos = ['rhyzome']

class customStemmer_roots_virtual(customStemmer_roots):
    """ I will make more options for stemmer """
    def __init__(self,):
        customStemmer_roots.__init__(self)
        self.rootdict.algos = ['virtual']

class customStemmer_roots_matrix(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self)
        infixes_letters_custom = u"توطيدا"
        self.set_infix_letters(infixes_letters_custom)
        self.config["root_dict"] = "yes"
        #~ rootslib.create_stamped_roots()
        #~ rootslib.create_virtual_roots()
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
            root_result = self.rootdict.choose_root_matrix(word, affixation_list, self.debug_root)
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
        
class rootStemmer(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self,)
        self.rootdict = rootslibclass.rootDict()
        pass
    def getstem(self,word):
        """ get a stem from word"""
        return word
    def getroot(self,word):
        """ get a root from word"""

        word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
        stem = self.getstem(word)
        affixation_list= [{'prefix':'',
                'suffix':'',
                'root':stem,
                'stem':stem,
                },
                ]
        root_result = self.rootdict.choose_root(word, affixation_list)
        if root_result:
            return root_result
        else:
            return stem 

class customStemmer_tag_root(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self)
        self.config["root_dict"] = "yes"
        #~ rootslib.create_stamped_roots()
        #~ rootslib.create_virtual_roots()
        self.rootdict = rootslibclass.rootDict()
        
        # tagger
        self.tagger = naftawayh.wordtag.WordTagger(); 
        # noun stemmer config
        # create stemmer
        self.noun_stemmer = abstractStemmer()
        # config prefix and suffix list
        self.noun_stemmer.set_prefix_list(NOUN_PREFIX_LIST)
        self.noun_stemmer.set_suffix_list(NOUN_SUFFIX_LIST)
        # verb stemmer config
        # create stemmer
        self.verb_stemmer = abstractStemmer()
        # config prefix and suffix list
        self.verb_stemmer.set_prefix_list(VERB_PREFIX_LIST)
        self.verb_stemmer.set_suffix_list(VERB_SUFFIX_LIST)        
    def is_verb(self,word):
        """ is verb word"""
        #~ return True
        return self.tagger.is_verb(word)
        return False
    def is_noun(self, word):
        """ is noun word"""
        return self.tagger.is_noun(word)
        #~ return False
    def getstem(self,word):
        """ get a stem from word"""
        if is_stop(word):
            return stop_stem(word)
        elif self.is_verb(word):
            return self.verb_stemmer.light_stem(word)
        elif self.is_noun(word):
            return self.noun_stemmer.light_stem(word)
        else: # a non defined verb or noun
            return self.light_stem(word)
    def getroot(self,word):
        """ get a stem from word"""
        if not is_stop(word):
            word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
            # default
            self.light_stem(word)
            self.segment(word)
            affixation_list= self.get_affix_list()
            default_root = self.get_root()

            if self.is_noun(word):
                self.noun_stemmer.light_stem(word)
                self.noun_stemmer.segment(word)
                affixation_list= self.noun_stemmer.get_affix_list()
                default_root = self.noun_stemmer.get_root()                
            elif self.is_verb(word):
                self.verb_stemmer.light_stem(word)
                self.verb_stemmer.segment(word)
                affixation_list= self.verb_stemmer.get_affix_list()
                default_root = self.verb_stemmer.get_root()                

            # filter valid affixes
            #~ affixation_list = filter(self.verify_affix, affixation_list)

            #~ root_result = rootslib.choose_root(affixation_list)
            root_result = self.rootdict.choose_root(word, affixation_list)
            if root_result:
                return root_result
            else:
                return default_root

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

    def verify_roots(self, root_list):
        pass
        


class customStemmer_tag(customStemmer_tag_root):
    """ I will make more options for stemmer """
    def __init__(self,):
        #~ abstractStemmer.__init__(self)
        customStemmer_tag_root.__init__(self)

    def getroot(self,word):
        """ get a stem from word"""
        if not is_stop(word):
            word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
            # default
            self.light_stem(word)
            self.segment(word)
            affixation_list= self.get_affix_list()
            default_root = self.get_root()

            if self.is_noun(word):
                self.noun_stemmer.light_stem(word)
                self.noun_stemmer.segment(word)
                affixation_list= self.noun_stemmer.get_affix_list()
                default_root = self.noun_stemmer.get_root()                
            elif self.is_verb(word):
                self.verb_stemmer.light_stem(word)
                self.verb_stemmer.segment(word)
                affixation_list= self.verb_stemmer.get_affix_list()
                default_root = self.verb_stemmer.get_root()                

            # filter valid affixes
            #~ affixation_list = filter(self.verify_affix, affixation_list)

            #~ root_result = self.rootdict.choose_root(affixation_list)
            #~ if root_result:
                #~ return root_result
            #~ else:
                #~ return default_root
            return default_root

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

    def verify_roots(self, root_list):
        pass
           
#Define an abstract Class for stemmer
class abstractIsri(ISRIStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        ISRIStemmer.__init__(self)
        pass
    def getstem(self,word):
        """ get a stem from word"""
        return self.stem(word)
    def getroot(self,word):
        """ get a root from word"""
        return self.stem(word)
        
        
#Define an abstract Class for stemmer
class abstractIsri_custom(ISRIStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        ISRIStemmer.__init__(self)
        self.rootdict = rootslibclass.rootDict()
        
        pass
    def getstem(self,word):
        """ get a stem from word"""
        return self.stem(word)
    def getroot(self,word):
        """ get a root from word"""
        if not is_stop(word):
            word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
            stem = self.stem(word)
            affixation_list= [{'prefix':'',
                    'suffix':'',
                    'root':stem,
                    'stem':stem,
                    },
                    ]
            root_result = self.rootdict.choose_root(word, affixation_list)
            if root_result:
                return root_result
            else:
                return stem

        else:
            return stop_root(word)

#Define an abstract Class for stemmer
class abstractAssem_custom(snowballstemmer.arabic_stemmer.ArabicStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        snowballstemmer.arabic_stemmer.ArabicStemmer.__init__(self,)
        self.rootdict = rootslibclass.rootDict()
        pass
    def getstem(self,word):
        """ get a stem from word"""
        return self.stemWord(word)
    def getroot(self,word):
        """ get a root from word"""
        if not is_stop(word):
            word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
            stem = self.stemWord(word)
            affixation_list= [{'prefix':'',
                    'suffix':'',
                    'root':stem,
                    'stem':stem,
                    },
                    ]
            root_result = self.rootdict.choose_root(word, affixation_list)
            if root_result:
                return root_result
            else:
                return stem

        else:
            return stop_root(word)
            
#Define an abstract Class for stemmer
class abstractKhoja_custom(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self,)
        self.rootdict = rootslibclass.rootDict()
        pass
    def getstem(self,word):
        """ get a stem from word"""
        return word
    def getroot(self,word):
        """ get a root from word"""
        word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
        stem = self.getstem(word)
        affixation_list= [{'prefix':'',
                'suffix':'',
                'root':stem,
                'stem':stem,
                },
                ]
        root_result = self.rootdict.choose_root(word, affixation_list)
        if root_result:
            return root_result
        else:
            return stem
            
class abstractFarasa_custom(abstractStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        abstractStemmer.__init__(self,)
        self.rootdict = rootslibclass.rootDict()
        pass
    def getstem(self,word):
        """ get a stem from word"""
        return word
    def getroot(self,word):
        """ get a root from word"""

        word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
        stem = self.getstem(word)
        affixation_list= [{'prefix':'',
                'suffix':'',
                'root':stem,
                'stem':stem,
                },
                ]
        root_result = self.rootdict.choose_root(word, affixation_list)
        if root_result:
            return root_result
        else:
            return stem

#Define an abstract Class for stemmer
class abstractAssem(snowballstemmer_modified.arabic_stemmer.ArabicStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        snowballstemmer_modified.arabic_stemmer.ArabicStemmer.__init__(self,)
        #~ assem_rooter.ArabicStemmer.__init__(self,)
        pass
    def getstem(self,word):
        """ get a stem from word"""
        return self.stemWord(word)
    def getroot(self,word):
        """ get a root from word"""
        return self.stemWord(word)
        
#Define an abstract Class for stemmer
class abstractAssem_rooter(snowballstemmer.arabic_stemmer.ArabicStemmer):
    """ I will make more options for stemmer """
    def __init__(self,):
        snowballstemmer.arabic_stemmer.ArabicStemmer.__init__(self,)
        pass
    def getstem(self,word):
        """ get a stem from word"""
        return self.stemWord(word)
    def getroot(self,word):
        """ get a root from word"""
        return self.stemWord(word)

        
class factory_stemmer(object):
    """ a factory for stemmers"""
    @staticmethod
    def get_stemmers():
        """
        get the name list of exisiting stemmers
        """
        namelist =["default",
        "custom-tag-root",
        "custom-tag",
        "isri",
        "isri+rooter",
        "assem",
        "assem-stemmer",
        "assem+rooter",
        "khoja+rooter",
        "farasa+rooter",
        "custom-affix",
        "custom-affix-stp",
        "custom-root",
        "custom-root-matrix",
        "custom-stp",
        "rooter-only",
        "multi",
        "lemmatizer",
        "stamp",
        "rhyzome",
        "extend",
        "virtual",
        ]
        return namelist
    @staticmethod
    def create_stemmer(name):
        """
        """
        if name == "default":
            """ no options"""
            asl = abstractStemmer()
        elif name == "isri":
            """ no options"""
            asl = abstractIsri()
        elif name == "isri+rooter":
            """ no options"""
            asl = abstractIsri_custom()
        elif name == "assem":
            """ no options"""
            asl = abstractAssem_rooter()
        elif name == "assem+rooter":
            """ no options"""
            asl = abstractAssem_custom()
        elif name == "khoja+rooter":
            """ no options"""
            asl = abstractKhoja_custom()
        elif name == "farasa+rooter":
            """ no options"""
            asl = abstractFarasa_custom()
        elif name == "assem-stemmer":
            """ no options"""
            asl = abstractAssem()
        elif name == "custom-affix":
            asl = customStemmer()
        elif name == "custom-affix-stp":
            asl = customStemmer_affix_stp()
        elif name == "custom-root":
            asl = customStemmer_roots()
        elif name == "stamp":
            asl = customStemmer_roots_stamp()
        elif name == "extend":
            asl = customStemmer_roots_extend()
        elif name == "rhyzome":
            asl = customStemmer_roots_rhyzome()
        elif name == "virtual":
            asl = customStemmer_roots_virtual()
        elif name == "custom-root-matrix":
            asl = customStemmer_roots_matrix()
        elif name == "custom-tag-root":
            asl = customStemmer_tag_root()
        elif name == "custom-tag":
            asl = customStemmer_tag()
        elif name == "custom-stp":
            asl = customStemmer_stp()
        elif name == "rooter-only":
            asl = rootStemmer()
        elif name == "multi":
            asl = multiStemmer()
        elif name == "lemmatizer":
            asl = customStemmer_lemmatizer()
        else:
            """ no options"""
            asl = abstractStemmer()            
        return asl
            
    def help():
        """ Display help of stemmers"""
        pass
        print("Available stemmers are:\n%s"%get_stemmers())
        
    
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
