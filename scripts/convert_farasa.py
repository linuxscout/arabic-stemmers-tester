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
    Arabic conversion of FARASA resulta
    Provides routins  to analyze text.
    Can treat text as verbs or as nouns.
"""

import sys
if __name__ == "__main__":

    sys.path.append('../support')
    sys.path.append('../')

import re
import argparse
import os
from sklearn.metrics import precision_score, recall_score,  accuracy_score, f1_score


def grabargs():
    parser = argparse.ArgumentParser(description='Convert Quran Corpus into CSV format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    
    args = parser.parse_args()
    return args
import re
def get_stem_farasa(word):
    """
    get stems from farasa output
    """
    if word:
        l= re.split("[;\+]", word)
        return max(l, key=len)
    return word

def main():
        
    args =grabargs()
    filename = args.filename
    outfile = args.outfile

    try:
        df = pd.read_csv(filename, delimiter='\t', 
        names=['word','root'],
        encoding = "utf-8" )
    except:
        print " Can't Open the given File ", filename;
        sys.exit();

    # prepare stemmers
    import numpy as np
    df = df.replace(np.nan, '', regex=True)
    print (df.head(20))
    df["farasa"] = df["root"].apply(get_stem_farasa)

    df.to_csv(outfile, sep='\t', encoding='utf-8')    
    print(df)
    
if __name__ == '__main__':
    main()
