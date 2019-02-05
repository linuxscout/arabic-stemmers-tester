#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  testdom2.py
#  
#  

import pyarabic.araby as araby
import xml.dom.minidom as minidom
#~ import xml.dom  as minidom
import sys
                  

def display_word_seg(xmldoc):
    # get the annuaire list
    words = xmldoc.getElementsByTagName('word')
    #~ print words
    cpt = 0
    list_segments=[]
    # display a word
    for word  in words:
        # every word contains choices
        word_value = word.getAttribute("value")
        choices = word.getElementsByTagName('analysis')
        for choice in choices:
            #~ print choice.toxml()
            root = choice.getAttribute('root')
            root = araby.hamza(root)
            stem = choice.getAttribute('stem')
            lemma = choice.getAttribute('lemma')
                #~ <analysis root="ثقل" stem="أثقال" lemma="ثقلان" />
            segment={"word":word_value, 'stem':stem, 'root':root, 'lemma':lemma }
            list_segments.append(segment)
    return list_segments



def main():
    DATA_FILE = 'samples/quranic_stem_corpus.xml'
    try:
        xmldoc = open(DATA_FILE)
    except:
        print "Can't Open the file, first test", DATA_FILE
        sys.exit()
    try:
        xmldoc = minidom.parse(DATA_FILE)
    except:
        print "Can't Open the file", DATA_FILE
        sys.exit()
    #~ treat_doc(xmldoc)
    #~ display_word(xmldoc)
    segments = display_word_seg(xmldoc)
    for seg in segments:
        print (u"\t".join([seg['word'], seg['root'],seg['lemma'], seg['stem'] ])).encode('utf8');

    
    return 0
if __name__ == '__main__':
    main()

