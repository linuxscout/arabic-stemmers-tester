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
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
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
from sklearn.metrics import precision_score, recall_score,  accuracy_score, f1_score, confusion_matrix
import pyarabic.araby as araby
import read_config
STEMMERS_CONFIG = "conf/stemmers.conf"
def grabargs():
    parser = argparse.ArgumentParser(description='Convert Quran Corpus into CSV format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    parser.add_argument("--dir", dest="data_directory", nargs='?', 
    help="Data directory for other external stemmers results", metavar="data_directory")
    
    parser.add_argument("--all", type=bool, nargs='?',
                        const=True, 
                        help="Test all stemmers.")
    parser.add_argument("--config", type=str, nargs='?',
                        const="", 
                        help="Test some stemmers cited in config file .")
    args = parser.parse_args()
    return args
    

            

def get_stem_farasa(word):
    """
    get stems from farasa output
    Farasa data is not hogoenous in output, forthis reason, we have modified the code
    to output partition,
    we support that the stem is the lengest part in segentation, because Farasa use 
    compound prefixes and suffixes separated by '+'
    """
    if word:
        l= re.split("[;\+]", word)
        return max(l, key=len)
    return word    

  

    
def test_stemmers(dataframe_result, data_path, names, names_to_control):
    """
    """
    df = dataframe_result
    # add normalized columns
    for name in names:
        if name == "khoja":
            #read khoja stemming
            try:
                df2 = pd.read_csv(data_path+".khoja", delimiter='\t',
                      names=['word','root'], 
                      skiprows=1,
                      encoding = "utf-8")
                df2 = df2.replace(np.nan, '', regex=True)
                df['khoja'] = df2['root']            
                df['khoja_stem'] = df2['root']            
            except:
                pass
        elif name == "farasa":
            #read farasa stemming
            try:
                df2 = pd.read_csv(data_path+".farasa", delimiter='\t',
                      names=['word','root'], 
                      skiprows=1,
                      encoding = "utf-8")
                df2 = df2.replace(np.nan, '', regex=True)
                df['farasa'] = df2['root'].apply(get_stem_farasa)            
                df['farasa_stem'] = df['farasa']            

            except:
                pass
        if name == "moataz":
            #read moataz stemming
            try:
                df2 = pd.read_csv(data_path+".moataz", delimiter='\t',
                      names=['word','root'], 
                      skiprows=1,
                      encoding = "utf-8")
                df2 = df2.replace(np.nan, '', regex=True)
                df['moataz'] = df2['root']            
                df['moataz_stem'] = df2['root']            
            except:
                pass                
        elif name == "farasa+rooter":
            #read farasa stemming
            df2 = pd.read_csv(data_path+".farasa", delimiter='\t',
                  names=['word','root'], 
                  skiprows=1,
                  encoding = "utf-8")
            df2 = df2.replace(np.nan, '', regex=True)
            asl = abstractstemmer.factory_stemmer.create_stemmer(name);
            df2['farasa'] = df2['root'].apply(get_stem_farasa)
            df[name] = df2['farasa'].apply(asl.getroot)
            df[name+"_stem"] = df2['farasa']
        elif name == "khoja+rooter":
            #read khoja stemming
            df2 = pd.read_csv(data_path+".khoja", delimiter='\t',
                  names=['word','root'], 
                  skiprows=1,
                  encoding = "utf-8")
            df2 = df2.replace(np.nan, '', regex=True)
            asl = abstractstemmer.factory_stemmer.create_stemmer(name);
            df[name]         = df2['root'].apply(asl.getroot)
            df[name+"_stem"] = df2['root'].apply(asl.getstem)

        else:
            
            asl = abstractstemmer.factory_stemmer.create_stemmer(name);
            df[name] = df["word"].apply(asl.getroot)
            df[name+"_stem"] = df["word"].apply(asl.getstem)
        if name in names_to_control:
            df[name+'root eval'] = df["root"] == df[name]            
            df[name+' stem eval'] = df["lemma"] == df[name+'_stem']            
    #~ print  df[df.root != df["custom_roots"]][['word','root',"custom_roots",]]                
    return df

if __name__ == '__main__':
    
    args = grabargs()
    filename = args.filename
    outfile = args.outfile
    stemmers_class_config = args.config
    #~ print stemmers_class_config

    #~ data_directory = args.data_directory
    all_stemmers = args.all
    data_dir = args.data_directory
    #~ input_file_base = os.path.basename(filename)
    if data_dir:
        data_path = os.path.join(data_dir, os.path.basename(filename))
    else:
        data_path = filename
    #~ print(data_dir)
    #~ sys.exit()
    try:
        df = pd.read_csv(filename, delimiter='\t',
          names=['word', 'root', 'lemma', 'type','non'], 
          encoding = "utf-8",
          skiprows=1)
    except:
        print(" Can't Open the given File ", filename)
        sys.exit();

    # used to choose between stemmers classes, in order to avoid re-runing
    if not stemmers_class_config:
        # here we test only tahasphyne derived stemmers
        stemmers_class_config = "tashaphyne"
    # prepare stemmers
    names = read_config.read_stemmers(STEMMERS_CONFIG,stemmers_class_config)
    if not names:
        print ("Error on reading config file %s"%STEMMERS_CONFIG)
        sys.exit()
    #~ print(names)
    #~ sys.exit()
    # add some stemmers to be controled under csv file 
    # show conditions
    #~ names_to_control =["rhyzome","default","custom-root"]
    names_to_control =[]
    # add features
    df2 = test_stemmers(df, data_path, names, names_to_control)

    # save file on csv
    df2.to_csv(outfile, sep='\t', encoding='utf-8')
    



