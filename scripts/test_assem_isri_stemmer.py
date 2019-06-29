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
import pyarabic.araby as araby
import read_config
STEMMERS_CONFIG = "stemmers.conf"
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
    args = parser.parse_args()
    return args
    

    
def test_stemmers(dataframe_result, data_path, names):
    """
    """
    for name in names:
        asl = abstractstemmer.factory_stemmer.create_stemmer(name);
        df[name] = df["word"].apply(asl.getroot)
        df[name+"_stem"] = df["word"].apply(asl.getstem)
    return df
if __name__ == '__main__':
    
    args = grabargs()
    filename = args.filename
    outfile = args.outfile
    all_stemmers = args.all
    data_dir = args.data_directory
    if data_dir:
        data_path = os.path.join(data_dir, os.path.basename(filename))
    else:
        data_path = filename
    try:
        df = pd.read_csv(filename, delimiter='\t',
          names=['word', 'root', 'lemma', 'type','non'], 
          encoding = "utf-8",
          skiprows=1)
    except:
        print " Can't Open the given File ", filename;
        sys.exit();
    # prepare stemmers
    # assem is a rooter
    names = ["assem", "assem-stemmer","isri", "arlstem"]
    if not names:
        print ("Error on reading config file %s"%STEMMERS_CONFIG)
        sys.exit()
    # show conditions
    df2 = test_stemmers(df, data_path, names)
    # save file on csv
    df2.to_csv(outfile, sep='\t', encoding='utf-8')



