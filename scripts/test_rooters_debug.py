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
import pyarabic.araby as araby
from stopwords.arabicstopwords import is_stop, stop_stem, stop_root
import read_config
STEMMERS_CONFIG = "stemmers_debug.conf"
import test_stemmers_rooters
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
    df = dataframe_result
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
    rooter = rootslibclass.rootDict(algos=['rhyzome']) 
    # debug in rhyzome rooter
    rooter.rhyzome_rooter.debug = True     
    #~ rooter = rootslibclass.rootDict()       
    df = dataframe_result
    # avoid null roots
    
    #~ total = df.size
    total = len(df.index)
    cpt = 0
    for word, root in zip(df["word"], df["root"]):
        root_list = root.split(';')
        print((u"**********%s*********"%word).encode('utf8'))
        asl.light_stem(word)
        print((u"Start Word : %s"%asl.get_starword()).encode('utf8'))        
        
        word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)

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
    print("***** Percent %.2f%% [%d/%d]"%(cpt*100.0/total, cpt, total))

def test_rooter2(dataframe_result):
    """
    """
    from pyarabic.arabrepr import arepr
    #test with tashaphyne
    asl = abstractstemmer.customStemmer_roots_rhyzome() 
    # debug in rhyzome rooter
    asl.rootdict.rhyzome_rooter.debug = True
    rooter =  asl.rootdict    
    df = dataframe_result
    # avoid null roots
    
    total = len(df.index)
    cpt = 0
    for word, root in zip(df["word"], df["root"]):
        root_list = root.split(';')
        print((u"**********%s*********"%word).encode('utf8'))
        asl.light_stem(word)
        print((u"Start Word : %s"%asl.get_starword()).encode('utf8'))        
        
        word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)

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
    print("***** Percent %.2f%% [%d/%d]"%(cpt*100.0/total, cpt, total))

def test_rooter3(dataframe_result):
    """
    """
    from pyarabic.arabrepr import arepr
    #test with tashaphyne
    asl = abstractstemmer.customStemmer_roots_rhyzome() 
    # debug in rhyzome rooter
    asl.rootdict.rhyzome_rooter.debug = True
    df = dataframe_result
    # avoid null roots
    
    total = len(df.index)
    cpt = 0
    for word, root in zip(df["word"], df["root"]):
        root_list = root.split(';')
        if not is_stop(word):
            word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
            asl.light_stem(word)
            default_root  = asl.get_root()
            starword = asl.get_starword()
            asl.segment(word)
            affixa_list = asl.get_affix_list()
            # filter valid affixes
            affixa_list = filter(asl.verify_affix, affixa_list)
            #~ root_result = rootslib.choose_root(affixation_list)
            if True:
                stems = [ d['stem'] for d in affixa_list]
                roots = [ d['root'] for d in affixa_list]
                print((u"**********%s*********"%word).encode('utf8'))
                print((u"Start Word : %s"%starword).encode('utf8'))        
                print("Stems: "+u' '.join(stems).encode('utf8'))   
                print((u"Dafault roots: [%s] a %s"%(default_root,u' '.join(roots))).encode('utf8'))        
                print(arepr(affixa_list))   
            
            root_result = asl.rootdict.choose_root(word, affixa_list,debug = True)
        else:
            root_result = stop_root(word)            
            roots = []
            stems = []
            startword =""
            default_root = ""
            affixa_list = []            
        if root_result in  root_list:
            cpt += 1
        if True:
            print((u" ".join([u"Test root", root, u"found root",
            root_result, str(root_result in root_list)])).encode('utf8'))

    print("***** Percent %.2f%% [%d/%d]"%(cpt*100.0/total, cpt, total))



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
    # prepare stemmers
    names = read_config.read_stemmers(STEMMERS_CONFIG)
    if not names:
        print ("Error on reading config file %s"%STEMMERS_CONFIG)
        sys.exit()
    rooters = False
    # add some stemmers to be controled under csv file 
    # show conditions
    if rooters:
        test_rooter3(df)
    
    else:
        df2 = test_stemmers(df, names)
        df2.to_csv(outfile, sep="\t", encoding='utf8')
        # to control on excel
        df3 = df2[["word", "lemma", "multi_stem", "lemmatizer_stem"]]
        df3.loc[:, "normalized"] = df3["lemma"].apply(test_stemmers_rooters.normalize_stem)
        df3.loc[:, 'compare'] = df3.apply(lambda row: test_stemmers_rooters.equal_stem(row['lemmatizer_stem'], row["lemma"]), axis=1)
        df3.loc[:, 'compare_norm'] = df3.apply(lambda row: test_stemmers_rooters.equal_stem(row['lemmatizer_stem'], row["normalized"], normalize_full=True), axis=1)
        
        df3.to_csv(outfile+".ctrl.csv", sep="\t", encoding='utf8')
        
        dstats = test_stemmers_rooters.calcul_stats(df2, names, stem_flag = True)
        dstats.to_csv(outfile+".stats", sep='\t', encoding='utf-8')    
        print(dstats)
if __name__ == '__main__':
    
    test2()
