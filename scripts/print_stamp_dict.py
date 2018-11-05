#!/usr/bin/python
# -*- coding=utf-8 -*-
#-----------------------------------------------------------------------
# Name:        light stemmer
# Purpose:     build an advanced stemmer for Information retreival 
#  
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     2018-08-14
# Copyright:   (c) Taha Zerrouki 2018
# Licence:     GPL
#-----------------------------------------------------------------------
"""
    Arabic text stemmer.
    Provides routins  to analyze text.
    Can treat text as verbs or as nouns.
"""

import sys
sys.path.append('../rooter')
sys.path.append('rooter')
sys.path.append('../')
import rootslibclass
def test2():
    
    rooter = rootslibclass.rootDict()
    for k in rooter.STAMP_DICT:
        print((u"%s\t%s"%(k, u", ".join(rooter.STAMP_DICT[k]))).encode('utf8'))

if __name__ == '__main__':
    
    test2()
