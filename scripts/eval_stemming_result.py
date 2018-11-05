#!/usr/bin/python
# -*- coding=utf-8 -*-
#-----------------------------------------------------------------------
# Name:        light stemmer
# Purpose:     build an advanced stemmer for Information retreival 
#  
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     2016-06-14
# Copyright:   (c) Taha Zerrouki 2016
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
from test_stemmers_rooters import calcul_stats
from sklearn.metrics import precision_score, recall_score,  accuracy_score, f1_score


def grabargs():
    parser = argparse.ArgumentParser(description='Convert Quran Corpus into CSV format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    #~ parser.add_argument("--dir", dest="data_directory",
    #~ help="Data directory for other external stemmers results", metavar="data_directory")
    
    parser.add_argument("--all", type=bool, nargs='?',
                        const=True, 
                        help="Test all stemmers.")
    args = parser.parse_args()
    return args


def main():
        
    args =grabargs()
    filename = args.filename
    outfile = args.outfile
    #~ data_directory = args.data_directory
    all_stemmers = args.all

    try:
        df = pd.read_csv(filename, delimiter='\t',
        #~ names = ['word', 'root', 'lemma', 'type','non'], 
        #~ names = columns,
          encoding = "utf-8",
          #~ skiprows=1,

          )
    except:
        print " Can't Open the given File ", filename;
        sys.exit();

    # prepare stemmers
    import numpy as np
    df = df.replace(np.nan, '', regex=True)
    if all_stemmers:
        names = abstractstemmer.factory_stemmer.get_stemmers();
        names.extend(['khoja','farasa'])
    else:
        names =["default",
        #~ "custom-tag-root",
        #~ "custom-tag",
        "isri",
        "khoja",
        "farasa",
        #~ "isri+rooter",
        "assem",
        #~ "assem-stemmer",
        #~ "assem+rooter",
        #~ "khoja+rooter",
        #~ "farasa+rooter",
        #~ "custom-affix",
        #~ "custom-affix-stp",
        "custom-root",
        "custom-root-matrix",
        #~ "custom-stp",
        #~ "rooter-only",
        #~ "multi",
        #~ "lemmatizer",
        ]

        

    dstats = calcul_stats(df, names, stem_flag = True)
    dstats.to_csv(outfile, sep='\t', encoding='utf-8')    
    print(dstats)
    
if __name__ == '__main__':
    main()
