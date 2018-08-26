#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_isri.py
#  

#  
#  

from nltk.stem.isri import ISRIStemmer
stemmer = ISRIStemmer()
word = u"بمكتباتنا"
stem = stemmer.stem(word)
print stem.encode('utf8')

