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

#~ import re
import argparse
import pandas as pd
#~ from eval_functions import calcul_stats
import abstracttester
import read_config
STEMMERS_CONFIG = "conf/stemmers.conf"

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
    # avoid stopwords and invalid words
    #~ df['valid']= df['word'].apply(is_valid_word)
    #~ df = df[df['valid'] == True]
    
    # prepare stemmers
    names = read_config.read_stemmers(STEMMERS_CONFIG)
    if not names:
        print ("Error on reading config file %s"%STEMMERS_CONFIG)
        sys.exit()    
     
    # root
    tester = abstracttester.factory_tester.create_tester("root")
    dstats = tester.calcul_stats(df, names)
    dstats.to_csv(outfile+".root", sep='\t', encoding='utf-8')    
    # stem
    tester = abstracttester.factory_tester.create_tester("stem")
    dstats = tester.calcul_stats(df, names)
    dstats.to_csv(outfile+".stem", sep='\t', encoding='utf-8')    
    print(dstats)
    
if __name__ == '__main__':
    main()
