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
import numpy as np
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
    
def get_stem_farasa(word):
    """
    get stems from farasa output
    Farasa data is not hogoenous in output, forthis reason, we have modified the code
    to output partition,
    we support that the stem is the lengest part in segentation, because Farasa use 
    compound prefixes and suffixes separated by '+'
    """
    if word:
        #~ word = unicode(word)
        l= re.split("[;\+]", word)
        return max(l, key=len)
    return word  
    
def test_stemmers(data_path2):
    """
    """
    try:
        df2 = pd.read_csv(data_path2, delimiter='\t',
              names=['farasa'], 
              skiprows=1,
              encoding = "utf-8")

    except:
        print("Can't open file %s"%data_path2)
        return False
    #~ df2 = df2.replace(np.nan, '', regex=True)
    
    df2['farasa'] = df2['farasa'].apply(get_stem_farasa)            
    df2['farasa_stem'] = df2['farasa']    
    return df2
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
    df2 = test_stemmers(filename)
    # save file on csv
    df2.to_csv(outfile, sep='\t', encoding='utf-8')



