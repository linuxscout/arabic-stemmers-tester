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
import re

import pyarabic.araby as araby
import tashaphyne.stemming
import abstractstemmer
#~ import rootslib
import rootslibclass


def test2():

    #test with tashaphyne
    #~ rootslib.create_stamped_roots()
    #~ rootslib.create_virtual_roots()
    #~ print repr(rootslib.VIRTUAL_DICT).replace('],','],\n').decode('unicode-escape').encode('utf8')
    from tashaphyne.stemming import ArabicLightStemmer
    asl = ArabicLightStemmer()
    asl_custom = abstractstemmer.customStemmer_roots()
    words = [(u'أفتضاربانني',u'ضرب'),
    (u'بأبأ',u'بءبء'),
    (u'يريدون',u'ريد'),
    (u'يستطعن', u'طوع'),
    (u'يستطيعون', u'طوع'),
    (u'الصيام', u'صوم'),
    (u'يخاف', u'خوف'),
    (u'كتاب',u'كتب'),
    (u"بالميدان",u'ميد'),
    (u"بالأسيهم",u'سهم'),
    (u"آخرين",u'ءخر'),
    (u"بالآخرة",u'ءخر'),    
    (u"لارتاب",u'ريب'),    
    (u"وسائل",u'وسل'),    
    (u"وصائل",u'وصل'),    
    (u"أخاه",u'ءخو'),    
    (u"أخوه",u'ءخو'),    
    (u"أخاهم",u'ءخو'),    
    (u"أخانا",u'ءخو'),  
    (u"بإذن",u'ءذن'), 
    (u"للأبرار",u"برر"),
    (u'واتبعوا', u'تبع'),
    (u'والكاظمين', u'كظم'),
    (u'عد', u'عود'),


  
    
    ]
    # load root dictionary with features
    rootdict = rootslibclass.rootDict()
    for word, root in words:
        print(u"**********%s*********"%word).encode('utf8')
        word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)

        asl.light_stem(word)
        asl.segment(word)
        print asl.get_segment_list()  
        seg_list = asl.get_segment_list()  
        starstem_list =[]
        affixa_list = asl.get_affix_list()
        print repr(affixa_list).replace('},','},\n').decode('unicode-escape').encode('utf8')
        #~ root_result = rootslib.choose_root(affixa_list, debug=True)
        root_result = rootdict.choose_root(affixa_list, debug=True)
        #~ root_result2 = rootdict.choose_root(affixa_list, debug=True)
        #~ print root_result.encode('utf8'),root_result2.encode('utf8'), asl_custom.getroot(word).encode('utf8'), root_result == root, root_result == root_result2
        print root_result.encode('utf8'), asl_custom.getroot(word).encode('utf8'), root_result == root
        
    return 0
if __name__ == '__main__':
    test2()
