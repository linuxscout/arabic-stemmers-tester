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
def display_node(node, level):
    print "  "*level, "Type", node.nodeType, "Name:", node.nodeName , "nodevalue", node.nodeValue, 
    #~ print node.toxml()
    if node.nodeType == node.TEXT_NODE:
        #~ print node.toxml()
        print  "Value:",node.data, "nodevalue", node.nodeValue
    else :
        print ;

                  

def display_word_seg(xmldoc):
    # get the annuaire list
    words = xmldoc.getElementsByTagName('w')
    #~ print words
    cpt = 0
    list_segments=[]
    # display a word
    for word  in words:
        # every word contains choices
        word_value = word.getAttribute("rend")
        choices = word.getElementsByTagName('choice')
        for choice in choices:
            #~ print choice.toxml()
            segs = choice.getElementsByTagName('seg')
            for seg in segs:
                #~ print seg.toxml()
                members = choice.getElementsByTagName('m')
                segment={"word":word_value,'root':[],'stem':[], 'prefix':[],'suffix':[], }
                for mmbr in members:
                    mmbr_type = mmbr.getAttribute('type')
                    try:
                        mmbr_value = mmbr.firstChild.data
                    except:
                        mmbr_value = ""
                    if mmbr_value:
                        segment[mmbr_type].append(mmbr_value)
                #~ print (repr(segment)).decode('unicode-escape');
                list_segments.append(segment)
    return list_segments

def display_word(xmldoc):
    # get the annuaire list
    words = xmldoc.getElementsByTagName('w')
    #~ print words
    cpt = 0
    # display a word
    for word  in words:
        # every word contains choices
        word_value = word.getAttribute("rend")
        print word_value.encode('utf-8');
                    
        cpt += 1

def treat_doc(xmldoc):
    # get the annuaire list
    text = xmldoc.getElementsByTagName('text')[0]
    print text
    cpt = 0
    # display phrase
    for phrase  in text.childNodes:
        print "-"*40
        print "Phrase", cpt
        print "'%s'"%phrase.toxml()
        cpt += 1

def main():
    DATA_FILE = 'samples/NAFIS_gold_standard.xml'
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
        #~ seg['stem'] = [x for x in seg['stem'] if x]
        #~ seg['root'] = [x for x in seg['root'] if x]
        stems = u';'.join(set(seg['stem']))
        stems_unvoc = u';'.join(set([araby.strip_tashkeel(x) for x in seg['stem']]))
        roots = u';'.join(set(seg['root']))
        print (u"\t".join([seg['word'], roots, stems_unvoc, stems ]).encode('utf8'));

    
    return 0
if __name__ == '__main__':
    main()

