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
from sklearn.metrics import precision_score, recall_score,  accuracy_score, f1_score


def grabargs():
    parser = argparse.ArgumentParser(description='Root extraction with debug option.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    args = parser.parse_args()
    return args
    
def test_stemmers(dataframe_result, names):
    """
    """
    for name in names:
        asl = abstractstemmer.factory_stemmer.create_stemmer(name);
        # use debug rooter algorithm
        asl.debug_root = True
        df[name] = df["word"].apply(asl.getroot)
        df[name+"_stem"] = df["word"].apply(asl.getstem)
    return df

def test_rooter(dataframe_result):
    """
    """
    from pyarabic.arabrepr import arepr
    #test with tashaphyne
    from tashaphyne.stemming import ArabicLightStemmer
    import rootslibclass
    asl = ArabicLightStemmer() 
    rooter = rootslibclass.rootDict(algos=['rhyzome','stamp'])       
    df = dataframe_result
    total = df.size
    cpt = 0
    for word, root in zip(df["word"], df["root"]):
        root_list = root.split(';')
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
        print("Stems: "+u' '.join(stems).encode('utf8'))        
        roots = [ d['root'] for d in affixa_list]
        print((u"Dafault roots: [%s] a %s"%(asl.get_root(),u' '.join(roots))).encode('utf8'))        
        #~ root_result = rooter.choose_wazn_root(affixa_list, debug=True)
        root_result = rooter.choose_root(word, affixa_list, debug=True)
        #~ print(u"Test root",root_result.encode('utf8'), u"found root",root_result.encode('utf8'), root_result == root)
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
    names = abstractstemmer.factory_stemmer.get_stemmers();

    # add some stemmers to be controled under csv file 
    # show conditions
    test_rooter(df)

if __name__ == '__main__':
    
    test2()
