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
import roots_const
import re
class rootMatrix
    """ a class to handle roots and lookup for roots """
    def __init__(self,):
        self.STAMP_DICT   ={}
        self.VIRTUAL_DICT ={}
        self.stamp_pat = re.compile(u"[%s%s%s%s%s%s%s%s%s]"% (araby.ALEF, 
    araby.YEH, araby.HAMZA, araby.ALEF_HAMZA_ABOVE, araby.WAW_HAMZA,
     araby.YEH_HAMZA, araby.WAW, araby.ALEF_MAKSURA, araby.SHADDA, ), 
     re.UNICODE)     

        self.create_stamped_roots()
        self.create_virtual_roots()
        self.debug = False
        self.use_cache = True
        self.cache = {'virtual':{},
        'rhyzome':{},
        'stamped':{},
        'extend':{},
        }
    @staticmethod
    def is_root(word):
        """ test if word is a root"""
        return word in roots_const.ROOTS
    @staticmethod
    def normalize_root(word):
        """ test if word is a root"""
        # change alef madda to hamza + ALEF
        word = word.replace(araby.ALEF_MADDA, araby.HAMZA+ araby.ALEF)
        word = word.replace(araby.TEH_MARBUTA, '')
        word = word.replace(araby.ALEF_MAKSURA, araby.YEH)
        return araby.normalize_hamza(word)
        
    @staticmethod
    def extend_root(psudoroot, wazn =""):
        """ extend a psudo root"""
        extended = []
        # convert ALEF to WAW or YEH
        if araby.ALEF in psudoroot:
            extended.append(psudoroot.replace(araby.ALEF, araby.WAW))
            extended.append(psudoroot.replace(araby.ALEF, araby.YEH))
        #~ if len(psudoroot) == 3 and araby.YEH in psudoroot:
            #~ extended.append(psudoroot.replace(araby.YEH, araby.WAW))
        #~ if len(psudoroot) == 3 and araby.WAW in psudoroot:
            #~ extended.append(psudoroot.replace(araby.WAW, araby.YEH))
            #~ extended.append(psudoroot.replace(araby.ALEF, araby.YEH))
        # extend root according to length,
        # if wazn (rooton) is given we can know where to add missed letter
        if not wazn:
            if psudoroot in (u'خذ',u'مر',u'كل'):
                extended.append(araby.HAMZA + psudoroot)
            if len(psudoroot) == 2:
                # add Yeh or waw at begin
                extended.append(araby.WAW + psudoroot)
                #~ extended.append(araby.YEH + psudoroot)
                #~ extended.append(araby.HAMZA + psudoroot)
                # add Yeh or waw at middle
                extended.append("".join([psudoroot[0],araby.WAW, psudoroot[1]]))
                extended.append("".join([psudoroot[0],araby.YEH, psudoroot[1]]))
                # add Yeh or waw at end
                extended.append(psudoroot+araby.WAW)
                extended.append(psudoroot+araby.YEH)
                # add double letter جد =>جدد
                extended.append(psudoroot + psudoroot[-1:])
            #~ if len(psudoroot) == 1:
                #~ #is a begin
                #~ extended.append(psudoroot + araby.WAW  + araby.YEH )
                #~ extended.append(psudoroot + araby.YEH  +araby.WAW  )        
                #~ # is middle
                #~ extended.append(araby.WAW + psudoroot + araby.YEH )
                #~ extended.append(araby.WAW + psudoroot*2 )
                #~ extended.append(araby.YEH + psudoroot +araby.WAW)
                #~ extended.append(araby.YEH + psudoroot *2)        
                #~ extended.append(araby.HAMZA + psudoroot + araby.YEH )
                #~ extended.append(araby.HAMZA + psudoroot*2 )
                #~ extended.append(araby.HAMZA + psudoroot +araby.WAW)
                
                
                #~ #is end
                #~ extended.append(araby.WAW  + araby.YEH + psudoroot)
                #~ extended.append(araby.YEH  +araby.WAW  + psudoroot)          
        else:
            # given roots are
            if araby.FEH not in wazn:
                # add FEH
                # possible YEH, WAW
                # add Yeh or waw at begin
                extended.append(araby.WAW + psudoroot)
                extended.append(araby.HAMZA + psudoroot)
                #~ extended.append(araby.YEH + psudoroot)
                
            if araby.AIN not in wazn:
                #add AIN
                # possible َAdjwaf
                # add Yeh or waw at middle
                if len(psudoroot) == 2:
                    extended.append("".join([psudoroot[0],araby.WAW, psudoroot[1]]))
                    extended.append("".join([psudoroot[0],araby.YEH, psudoroot[1]]))

            if araby.LAM not in wazn:
                #add LAM
                # possible double مضعف
                # possible maqsur
                # add Yeh or waw at end
                extended.append(psudoroot+araby.WAW)
                extended.append(psudoroot+araby.YEH)
                # add double letter جد =>جدد
                extended.append(psudoroot + psudoroot[-1:])
                
                        
            if False and len(psudoroot) == 2:
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

        return extended

    @staticmethod
    def most_common(lst):
        triroots = [x for x in lst if len(x) == 3]
        if triroots:
            lst = triroots
        return max(set(lst), key=lst.count)

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
        # strip the last letter if is doubled
        if word[-1:] ==  word[-2:-1]:
            word = word[:-1]
        return self.stamp_pat.sub('', word)


    
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
    @staticmethod
    def virtualize_root(word):
        """ convert Weak letters into One code """
        word = word.replace(araby.ALEF, "?")
        word = word.replace(araby.YEH, "?")
        word = word.replace(araby.WAW, "?")
        word = word.replace(araby.ALEF_MAKSURA, "?")
        return word

    def create_virtual_roots(self, ):
        if  self.VIRTUAL_DICT:
            return

        for root in roots_const.ROOTS:
            vrtl =  self.virtualize_root(root)
            #~ if vrtl != root:
            if vrtl in  self.VIRTUAL_DICT:
                 self.VIRTUAL_DICT[vrtl].append(root)
            else:
                 self.VIRTUAL_DICT[vrtl]= [root,]


    def is_stamped_root(self, word):
        """ test if word is a stop"""
        # calcul the stamp
        stmp =  self.word_stamp(word)
        # lookup for stamp roots
        return  self.STAMP_DICT.get(stmp, [])

    def is_virtual_root(self, word):
        """ test if word is a valid virtual root"""
        # calcul the virtual root
        vrtl =  self.virtualize_root(word)
        # lookup for virtual roots
        return  self.VIRTUAL_DICT.get(vrtl, [])

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
    def valid_starstem(self, starword):
        
        """ validate starwoord agnaist Schemes أوزان"""
        accepted_wazns = []
        for wazn in WAZNS:
            #~ if araby.waznlike(starword,wazn):
            if len(wazn) == len(starword):
                root = self.waznlike2(starword, wazn, extract_root = True)
                if root:
                  accepted_wazns.append(root)
                  # extend roots to add removed letters according to wazn              
                  extended = self.extend_root(root, wazn)
                  
                  accepted_wazns.extend(extended)
                  if self.debug:
                      print(u"\t".join([starword, wazn,root, u";".join(extended)]).encode('utf8'))
        return accepted_wazns

    @staticmethod
    def filter_root_length_valid(roots):
        
        return [x for x in roots if len(x) >= 3 and len(x)<=4 and araby.ALEF not in x]
    
    @staticmethod    
    def debug_algo(debug, word,  level, name, candidats, roots, roots_tmp, accepted):
        if debug:
            print((u"*** Level %d: [%s] %s "%(level,name, word)).encode('utf8'))
            print("   Candidats    :", u"\t".join(candidats).encode('utf8'))
            print("   roots    :", u"\t".join(roots).encode('utf8'))
            print("   roots tmp:", u"\t".join(roots_tmp).encode('utf8'))
            print("   accepted :", u"\t".join(accepted).encode('utf8'))
        
    def choose_root(self, word, affixation_list, debug = False):
        """ test an algorithm to choose roots"""
        accepted = []
        all_accepted = []
        
        # if all algo, all algorithms will be tested over roots
        # we think to test all algorithms then get the most common root
        # the secnd way when all_algorithms is false, we use if else to get the given root, and stop when we can get one at least
        all_algo = True
        #roots
        stems = [ self.normalize_root(d['stem']) for d in affixation_list]
        roots = [ self.normalize_root(d['root']) for d in affixation_list]
        if all_algo or not accepted:

            # get uniq root
            #~ accepted = list(set(filter(.is_root, roots)))
            # avoid non 3-4 letters roots
            roots_tmp =  self.filter_root_length_valid(roots)
            # lookup for real roots
            accepted = filter( self.is_root, roots_tmp)
            self.debug_algo(debug, word, 1 , "default", roots, roots, roots_tmp, accepted)
            # to handle all accepted together
            all_accepted.extend(accepted)

        # Stems as roots
        if all_algo or not accepted:

            # avoid non 3-4 letters roots
            roots_tmp =  self.filter_root_length_valid(stems)
            # lookup for real roots
            accepted = filter( self.is_root, roots_tmp)
            all_accepted.extend(accepted)            
            self.debug_algo(debug, word, 2 , "default as stem", stems, stems, roots_tmp, accepted)

        # Virtual roots
        if all_algo or not accepted :#and False:
            # try to virtualize roots
            virtual_roots = []
            #~ for x in roots:
            candidat_stems =  [x for x in stems if len(x) >= 3 and len(x)<=4]
            # virtual roots will be applied on roots also
            candidat_stems.extend(roots)
            for x in stems:
                if x not in self.cache['virtual']:
                    self.cache['virtual'][x] = self.is_virtual_root(x) 
                virtual_roots.extend(self.cache['virtual'][x])
                    
            roots_tmp =  self.filter_root_length_valid(virtual_roots)
            # lookup for real roots
            #~ accepted = filter(is_root, roots_tmp)
            accepted = roots_tmp
            all_accepted.extend(accepted)
            self.debug_algo(debug, word, 3, "virtual roots", candidat_stems, virtual_roots, roots_tmp, accepted)


        # Tiny Scheme extraction
        if all_algo or not accepted:
            # try to extract roots from stems

            wazn_roots = []
            for x in stems:
                #~ wazn_roots.extend(self.valid_starstem(x))
                if x not in self.cache['rhyzome']:
                    self.cache['rhyzome'][x] = self.valid_starstem(x)               

                wazn_roots.extend(self.cache['rhyzome'][x])
            #~ accepted = filter(.is_root, ampted_roots )
            roots_tmp =  self.filter_root_length_valid(wazn_roots)
            # lookup for real roots
            accepted = filter( self.is_root, roots_tmp)
            all_accepted.extend(accepted)
            #~ accepted = roots_tmp
            self.debug_algo(debug, word, 4, "Rhyzome roots", stems, wazn_roots, roots_tmp, accepted)



        # Extending roots
        if all_algo or not accepted:
        #~ if False :#not accepted:
            # try to extend roots
            extended_roots = []
            for x in roots:
                #~ extended_roots.extend( self.extend_root(x))
                if x not in self.cache['extend']:
                    self.cache['extend'][x] = self.extend_root(x)                
                extended_roots.extend(self.cache['extend'][x])
            roots_tmp =  self.filter_root_length_valid(extended_roots)
            # lookup for real roots
            accepted = filter( self.is_root, roots_tmp)
            all_accepted.extend(accepted)            
            self.debug_algo(debug, word, 5, "extended roots", roots, extended_roots, roots_tmp, accepted)

        # stamped roots
        if all_algo or not accepted:
        #~ if False :#not accepted:
            # try to extend roots
            stamped_roots = []
            #~ for x in roots:
            for x in stems:
                #~ stamped_roots.extend(self.is_stamped_root(x))
                if x not in self.cache['stamped']:
                    self.cache['stamped'][x] = self.is_stamped_root(x)
                stamped_roots.extend(self.cache['stamped'][x])

            #~ accepted = filter(is_root, sampted_roots )
            roots_tmp =  self.filter_root_length_valid(stamped_roots)
            #don't need to filter roots because stamps do it
            # lookup for real roots
            #~ accepted = filter(is_root, roots_tmp)
            accepted = roots_tmp
            all_accepted.extend(accepted)            
            self.debug_algo(debug, word, 6, "stamped roots", stems, stamped_roots, roots_tmp, accepted)

        if all_algo and all_accepted: 
            return  self.most_common(all_accepted)
        elif accepted:
            #select tri-letter before selecting 4 letters
            return  self.most_common(accepted)
        else:
            return ''
    def choose_wazn_root(self, affixation_list, debug=False):
        """
        Choose root according to wazns 
        """
        accepted = []
        #roots
        stems = [ self.normalize_root(d['stem']) for d in affixation_list]
        #~ roots = [ self.normalize_root(d['root']) for d in affixation_list]
        # Tiny Scheme extraction
        wazn_roots = []
        for x in stems:
            wazn_roots.extend( self.valid_starstem(x))
        #~ accepted = filter(.is_root, ampted_roots )
        roots_tmp =  self.filter_root_length_valid(wazn_roots)
        # lookup for real roots
        accepted = filter( self.is_root, roots_tmp)
        #~ accepted = roots_tmp
        self.debug_algo(debug, 2, "stem scheme roots", stems,wazn_roots, roots_tmp, accepted)    

        return accepted
def test1(args):
    word = u"لعلهم"
    print(is_root(word))
    word = u"علم"
    print(is_root(word))
    
    #test with tashaphyne
    from tashaphyne.stemming import ArabicLightStemmer
    asl = ArabicLightStemmer()        
    words = [u'أفتضاربانني',
    u'بأبأ',
    u'يريدون',
    u'يستطعن',
    u'كتاب',
    u"بالميدان",
    u"بالأسيهم",
    
    ]
    ext = extend_root(u"رم")
    print ("extende")
    print(repr(ext).decode('unicode-escape').encode('utf8'))

    for word in words:
        print(u"**********%s*********"%word)
        asl.light_stem(word)
        asl.segment(word)
        print(asl.get_segment_list())  
        seg_list = asl.get_segment_list()  
        starstem_list =[]
        for seg in seg_list:
            left, right = seg
            starstem_list.append(asl.get_starstem(left, right))
        print("star stems")
        
        print (u"\t".join(starstem_list)).encode('utf8')
        filtered_starstem_list =filter(valid_starstem, starstem_list)
        print("filtred star stem")
        print (u"\t".join(filtered_starstem_list)).encode('utf8')
        for st in starstem_list:
            print(st, u"\t".join(valid_starstem(st)).encode('utf8'))
        affixation_list= asl.get_affix_list()
        stems = [d['stem'] for d in affixation_list]
        print ("Candidats stems%s"%u'\t'.join(stems))
        for st in stems:
            print( st, u"\t".join(valid_starstem(st)).encode('utf8') )       
        
        print( repr(affixation_list).replace('},','},\n').decode('unicode-escape').encode('utf8'))
        print("reduce")
        #~ affixation_list = filter(verify_affix, affixation_list)
        print(repr(affixation_list).replace('},','},\n').decode('unicode-escape').encode('utf8'))

        roots = [normalize_root(d['root']) for d in affixation_list]
        print ("Candidats %s"%u'\t'.join(roots))
        # get uniq root
        accepted = set(filter(is_root, roots))
        print ("accepted %s"%u'\t'.join(accepted))
        if not accepted:
            # try to extend roots
            
            extended_roots = []
            for x in roots:
                extended_roots.extend(extend_root(x))
            print ("Candidats extended %s"%u'\t'.join(extended_roots))
            accepted = set(filter(is_root, extended_roots ))
            print ("accepted level2 %s"%u'\t'.join(accepted))            
        print('root %s'%asl.get_root())
    #~ print repr(STAMP_DICT).replace('},','},\n').decode('unicode-escape').encode('utf8')
    return 0

def test2():
    #test with tashaphyne
    from tashaphyne.stemming import ArabicLightStemmer
    asl = ArabicLightStemmer()        
    words = [(u'أفتضاربانني',u'ضرب'),
    (u'بأبأ',u'بءبء'),
    (u'يريدون',u'ريد'),
    (u'يستطعن', u'ريد'),
    (u'كتاب',u'كتب'),
    (u"بالميدان",u'ميد'),
    (u"بالأسيهم",u'سهم'),
    (u"آخرين",u'ءخر'),
    (u"بالأخرة",u'ءخر'),
    
    ]
    for word, root in words:
        print(u"**********%s*********"%word)
        asl.light_stem(word)
        asl.segment(word)
        print(asl.get_segment_list())  
        seg_list = asl.get_segment_list()  
        seg_list = asl.get_segment_list()  
        starstem_list =[]
        affixa_list = asl.get_affix_list()
        #~ root_result = choose_root(affixa_list, debug=True)
        root_result = choose_root(word, affixa_list, debug=True)
        print(root_result, root_result == root)
    return 0

def diff(first, second):
    """
    """
    second = set(second)
    return [item for item in first if item not in second]
    
def test3():
    from pyarabic.arabrepr import arepr
    #test with tashaphyne
    from tashaphyne.stemming import ArabicLightStemmer
    asl = ArabicLightStemmer() 
    rooter = rootDict()       
    words = [(u'أفتضاربانني',u'ضرب'),
    #~ (u'بأبأ',u'بءبء'),
    #~ (u'يسعى',u'سعى'),
    #~ (u'يريدون',u'ريد'),
    #~ (u'يستطعن', u'ريد'),
    #~ (u'كتاب',u'كتب'),
    #~ (u"بالميدان",u'ميد'),
    #~ (u"بالأسيهم",u'سهم'),
    #~ (u"آخرين",u'ءخر'),
    #~ (u"بالأخرة",u'ءخر'),
    #~ ('ويرمي',u'رمي'),
#~ (u'ويرمي',u'رمي'),
#~ (u'يرمون',u'رمي'),
#~ (u'راميات',u'رمي'),
#~ (u'وترمون',u'رمي'),
#~ (u'ويرمين',u'رمي'),
#~ (u'وترميان',u'رمي'),
#~ (u'ورامون',u'رمي'),
#~ (u'وليرميان',u'رمي'),
#~ (u'لترميان',u'رمي'),
#~ (u'لترمين',u'رمي'),
#~ (u'رامي',u'رمي'),
#~ (u'ورامي',u'رمي'),
#~ (u'رماية',u'رمي'),
#~ (u'رمايه',u'رمي'),
#~ (u'الراميات',u'رمي'),
#~ (u'المرميات',u'رمي'),
#~ (u'المتراميات',u'رمي'),
#~ (u'مترامية',u'رمي'),
#~ (u'مترامي',u'رمي'),
#~ (u'الرامون',u'رمي'),
#~ (u'والراميات',u'رمي'),
#~ (u'وسيقولون',u'قول'),
#~ (u'وسيقال',u'قول'),
#~ (u'وسيقيلوهم',u'قول'),
#~ (u'وتقال',u'قول'),
#~ (u'وتقولوا',u'قول'),
#~ (u'وتقول',u'قول'),
#~ (u'ومقاول',u'قول'),
#~ (u'وقالوا',u'قول'),
#~ (u'ومقال',u'قول'),

(u'وتقل', u'قول'),
(u'وتقلن', u'قول'),
(u'وليقل', u'قول'),
(u'ولتقلنا', u'قول'),
(u'لتقل', u'قول'),
(u'تقل', u'قول'),
(u'ونقل', u'قول'),
(u'ولنقل', u'قول'),
(u'فتقل', u'قول'),
(u'ستقل', u'قول'),
(u'ستقلن', u'قول'),
(u'وستقلن', u'قول'),
(u'فستقل', u'قول'),

(u'وقالوا', u'قول'),
(u'قالوا', u'قول'),
(u'وقالا', u'قول'),
(u'قالا', u'قول'),
(u'وقالت', u'قول'),
(u'قالت', u'قول'),
(u'ويقال', u'قول'),
(u'يقال', u'قول'),
(u'وسيقال', u'قول'),
(u'سيقال', u'قول'),
(u'ويقلن', u'قول'),
(u'يقلن', u'قول'),
(u'ويقلنا', u'قول'),
(u'يقلنا', u'قول'),
(u'وتقال', u'قول'),
(u'تقال', u'قول'),
(u'وقال', u'قول'),
(u'قال', u'قول'),
(u'وسأقول', u'قول'),
(u'سأقول', u'قول'),
(u'وقائل', u'قول'),
(u'قائل', u'قول'),
(u'وقائلان', u'قول'),
(u'قائلان', u'قول'),
(u'وقائلون', u'قول'),
(u'قائلون', u'قول'),
(u'وقائلا', u'قول'),
(u'قائلا', u'قول'),
(u'ومقال', u'قول'),
(u'مقال', u'قول'),
(u'وقائلتان', u'قول'),
(u'قائلتان', u'قول'),
(u'يعد', u'وعد'),
(u'تعد', u'عدد'),
(u'نعدهم', u'عدد'),
(u'وتعدهم',u'وعد'),
(u'تعدهم',u'وعد'),
(u'وستعدهم',u'وعد'),
(u'ستعدهم',u'وعد'),
(u'وتعدهما',u'وعد'),
(u'تعدهما',u'وعد'),
(u'ويعدهم',u'وعد'),
(u'يعدهم',u'وعد'),
(u'ويعدهما',u'وعد'),
(u'يعدهما',u'وعد'),
(u'وسيعدهم',u'وعد'),
(u'سيعدهم',u'وعد'),
(u'وسيعدهما',u'وعد'),
(u'سيعدهما',u'وعد'),
(u'ولنعدهم',u'وعد'),
(u'لنعدهم',u'وعد'),
(u'ولنعدهما',u'وعد'),
(u'لنعدهما',u'وعد'),
(u'ولتعدهم',u'وعد'),
(u'لتعدهم',u'وعد'),
(u'ولتعدهما',u'وعد'),
(u'لتعدهما',u'وعد'),
(u'ولتعدها',u'وعد'),
(u'لتعدها',u'وعد'),
(u'وستعدها',u'وعد'),
(u'ستعدها',u'وعد'),
(u'ووعدها',u'وعد'),
(u'وعدها',u'وعد'),
(u'ووعدهم',u'وعد'),
(u'وعدهم',u'وعد'),
(u'ووعدهما',u'وعد'),
(u'وعدهما',u'وعد'),
(u'وتعد',u'وعد'),
(u'تعد',u'وعد'),
(u'وتعدني',u'وعد'),
(u'تعدني',u'وعد'),
(u'وتعدنا',u'وعد'),
(u'تعدنا',u'وعد'),
(u'وتعده',u'وعد'),
(u'تعده',u'وعد'),
(u'وواعدناهم',u'وعد'),
(u'واعدناهم',u'وعد'),
(u'ووعدناهم',u'وعد'),
(u'وعدناهم',u'وعد'),
(u'وتعدوهم',u'وعد'),
(u'تعدوهم',u'وعد'),
(u'يعتاد',u'عود'),
(u'أحست',u'حسس'),
(u'يحسون',u'حسس'),
(u'ثقة',u'وثق'),
(u'ثقات',u'وثق'),
(u'بثقات',u'وثق'),
(u'صفات',u'وصف'),
(u'صلاته',u'وصل'),

    ]
    for word, root in words:
        print((u"**********%s*********"%word).encode('utf8'))
        asl.light_stem(word)
        asl.segment(word)
        print(asl.get_segment_list()  )
        seg_list = asl.get_segment_list()  
        starstem_list =[]
        affixa_list = asl.get_affix_list()
        stems = [ d['stem'] for d in affixa_list]
        print(u' '.join(stems).encode('utf8'))
        #~ root_result = rooter.choose_wazn_root(affixa_list, debug=True)
        root_result = rooter.choose_root(word, affixa_list, debug=True)
        print("Test root",root_result.encode('utf8'), "found root",root_result.encode('utf8'), root_result == root)
    # test root_extension
    roots=[u"قل",
    u"دع",
    ]
    for rt in roots:
        extended = rooter.extend_root(rt)
        print(u"\t".join([rt, u";".join(extended)]).encode('utf8'))
    print('stamped roots', len(rooter.STAMP_DICT ))
    print('stamped roots diff new', len(diff(rooter.STAMP_DICT,roots_const.ROOTS )))
    print('stamped roots removed', len(diff(roots_const.ROOTS, rooter.STAMP_DICT )))
    print('stamped roots max length', max((len(v), k, v) for k,v in rooter.STAMP_DICT.iteritems()))
    print('virtual roots', len(rooter.VIRTUAL_DICT))
    print('virtual roots diff', len(diff(rooter.VIRTUAL_DICT,roots_const.ROOTS )))
    print('virtual roots removed ', len(diff(roots_const.ROOTS, rooter.VIRTUAL_DICT )))
    print('virtual roots max length', max((len(v),k, v) for k,v in rooter.VIRTUAL_DICT.iteritems()))
    
    print('all roots', len(roots_const.ROOTS))

        
    return 0
if __name__ == '__main__':
    test3()
