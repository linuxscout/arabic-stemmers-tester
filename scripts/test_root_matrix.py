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

import re
import argparse
import os
import abstractstemmer
import pandas as pd
import numpy as np
import pyarabic.araby as araby
from pyarabic.arabrepr import arepr 
import rootslibclass
import itertools
import logging
#~ logging.basicConfig(level=logging.INFO)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
# create a file handler
handler = logging.FileHandler('root_matrix.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)

#~ from sklearn.metrics import precision_score, recall_score,  accuracy_score, f1_score
AFFIXATION_LETTERS = u"أابةتدسطفكلمنهويءئى"
def most_common(lst):
    if lst:
        return max(set(lst), key=lst.count)
    else: 
        return ""

def grabargs():
    parser = argparse.ArgumentParser(description='Root extraction with debug option.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    args = parser.parse_args()
    return args

def test_matrix(dataframe_result):
    """
    """
    from pyarabic.arabrepr import arepr
    #test with tashaphyne
    from tashaphyne.stemming import ArabicLightStemmer
    import rootslibclass
    asl = ArabicLightStemmer()
    rooter = rootslibclass.rootDict() 
    rooter.debug = True 
    #test with tashaphyne
    df = dataframe_result
    total = df.size
    cpt = 0
    for word, root in zip(df["word"], df["root"]):
        print((u"**********%s*********"%word).encode('utf8'))
        asl.light_stem(word)
        print((u"Start Word : %s"%asl.get_starword()).encode('utf8'))        
        
        asl.segment(word)
        print(asl.get_segment_list()  )
        seg_list = asl.get_segment_list()  
        starstem_list =[]
        affixa_list = asl.get_affix_list()
        # stems prints 
        stems = [ d['stem'] for d in affixa_list]
        roots = []
        for stem in stems:
            temp_list = rooter.matrix_root(stem,u'توطيدا')
            tmp_roots = [d['root'] for d in temp_list]
            roots.extend(tmp_roots)
            #~ tmp_roots = [d['root'] for d in temp_list if rooter.is_root(d['root'])]
        print((u"Candidats " + u"\t".join(roots)).encode('utf8'))
        # lookup only one time by root in dictionary
        set_roots = [x for x in set(roots) if rooter.is_root(x)]
        # remove invalid roots and keep repetition
        roots = [x for x in roots if x in set_roots]
        root_result = most_common(roots)
        print((u"Accepted " + u"\t".join(roots)).encode('utf8'))
        print((u"root " + root_result).encode('utf8'))
        print((u" ".join([u"Test root", root, u"found root",
        root_result, str(root_result == root)])).encode('utf8'))
        if root_result == root:
            cpt += 1
    print("***** Percent %.2f%%"%(cpt*100/total))        
            
def test_rooter_matrix(dataframe_result):
    """
    """
    from pyarabic.arabrepr import arepr
    #test with tashaphyne
    from tashaphyne.stemming import ArabicLightStemmer
    import rootslibclass
    asl = ArabicLightStemmer() 
    rooter = rootslibclass.rootDict()       
    df = dataframe_result
    total = df.size
    cpt = 0
    for word, root in zip(df["word"], df["root"]):
        print((u"**********%s*********"%word).encode('utf8'))
        asl.light_stem(word)
        root_list = root.split(';')        
        print((u"Start Word : %s"%asl.get_starword()).encode('utf8'))        
        
        asl.segment(word)
        print(asl.get_segment_list()  )
        seg_list = asl.get_segment_list()  
        starstem_list =[]
        affixa_list = asl.get_affix_list()
        # stems prints 
        stems = [ d['stem'] for d in affixa_list]
        print("Stems: "+u' '.join(stems).encode('utf8'))        
        roots = [ d['root'] for d in affixa_list]
        print((u"Dafault roots: [%s] a %s"%(asl.get_root(),u' '.join(roots))).encode('utf8'))        
        #~ root_result = rooter.choose_wazn_root(affixa_list, debug=True)
        root_result = rooter.choose_root_matrix(word, affixa_list, debug=True)
        #~ print(u"Test root",root_result.encode('utf8'), u"found root",root_result.encode('utf8'), root_result == root)
        #~ print((u" ".join([u"Test root", root, u"found root",
        #~ root_result, str(root_result == root)])).encode('utf8'))
        #~ if root_result == root:
            #~ cpt += 1
        print((u" ".join([u"Test root", root, u"found root",
        root_result, str(root_result in root_list)])).encode('utf8'))
        if root_result in  root_list:
            cpt += 1            
    print("***** Percent %.2f%%"%(cpt*100/total))            


def test2():
    args = grabargs()
    filename = args.filename
    outfile = args.outfile
    #~ data_directory = args.data_directory

    try:
        df = pd.read_csv(filename, delimiter='\t',
          names=['word', 'root', 'lemma', 'type','non'], 
          #~ names=['word', 'root'], 
          encoding = "utf-8",
          #~ nrows = 100,
          skiprows=1)
    except:
        print " Can't Open the given File ", filename;
        sys.exit();

    df = df.replace(np.nan, '', regex=True)
    # prepare stemmers
    #~ names = abstractstemmer.factory_stemmer.get_stemmers();

    # add some stemmers to be controled under csv file 
    # show conditions
    #~ test_rooter(df)
    #~ test_matrix(df)
    test_rooter_matrix(df)

if __name__ == '__main__':
    
    test2()
