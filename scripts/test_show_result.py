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
import pandas as pd
import numpy as np

def grabargs():
    parser = argparse.ArgumentParser(description='Convert Quran Corpus into CSV format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    args = parser.parse_args()
    return args
    
   
if __name__ == '__main__':
    
    args = grabargs()
    filename = args.filename
    outfile = args.outfile
    try:
        df = pd.read_csv(filename, delimiter='\t',
          #~ names=['word', 'root', 'lemma', 'type','non'], 
          encoding = "utf-8",
          #~ skiprows=1
          )
    except:
        print " Can't Open the given File ", filename;
        sys.exit();
    df2 = df[['word','root','rhyzome', 'rhyzomeroot eval']]

    df2.to_csv(outfile, sep='\t', encoding='utf-8')
