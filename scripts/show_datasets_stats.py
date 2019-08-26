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
    Provides routines to calcul statistics about datasets
"""

if __name__ == "__main__":
    import sys
    sys.path.append('../support')
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
    

def calcul_stats(dataframe,name):
    """
    Calculer 
    """
    df = dataframe
    #~ # display= data stats
    print('********* ROOT ****************')
    total = df.shape[0]
    stats_list={}
    stats_list[name]={
    #~ "name":name,
    "Count":total,
    "Unique words Count":df['word'].nunique(),
    "Unique lemmas Count ":df['lemma'].nunique(),
    "Unique roots Count":df['root'].nunique(),
    "Mean words by lemma":df[['word','lemma']].groupby('lemma').count().mean(),
    "Mean words by root":df[['word','root']].groupby('root').count().mean(),

    "Max words by root":df[['word','root']].groupby('root').count().max(),
    "Max words by lemma":df[['word','lemma']].groupby('lemma').count().max(),
    #~ "Min words by lemma":df[['word','lemma']].groupby('lemma').count().min(),
    #~ "Min words by root":df[['word','root']].groupby('root').count().min(),

    }

    dstats = pd.DataFrame.from_dict(stats_list, orient='index')
    
    return dstats
    
if __name__ == '__main__':
    
    args =grabargs()
    filename = args.filename
    outfile = args.outfile
    try:
        df = pd.read_csv(filename, delimiter='\t',
          names=['word', 'root', 'lemma', 'type','non'], 
          encoding = "utf-8",
          skiprows=1)
    except:
        print " Can't Open the given File ", filename;
        sys.exit();
    name = os.path.basename(filename)
    #~ df.to_csv(outfile, sep='\t', encoding='utf-8')
    dstats = calcul_stats(df, name)
    dstats.to_csv(outfile+".stats", sep='\t', encoding='utf-8')    
    print(dstats)
