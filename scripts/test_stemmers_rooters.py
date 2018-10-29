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
        l= re.split("[;\+]", word)
        return max(l, key=len)
    return word    

def calcul_stats_old(dataframe, names, root_flag = True, stem_flag = False,lemma_flag = False, ):
    """
    Calculer 
    """
    df = dataframe
    #~ # display= data stats
    print('********* ROOT ****************')
    total = df.shape[0]
    stats_list={}
    for name in names:
        
        cpt = df[df.root == df[name]][name].count()
        stats_list[name]={
        #~ "name":name,
        "count":cpt,
        "total":total,
        "linguistics accuracy": cpt *100.0 / total,
        'micro Accuracy': accuracy_score(df["root"],df[name])*100,
        'micro F1 score': f1_score(df["root"],df[name], average='micro')*100,
        'micro Recall':recall_score(df["root"],df[name], average='micro')*100,
        'micro Precision': precision_score(df["root"],df[name], average='micro')*100,

        'macro Accuracy': accuracy_score(df["root"],df[name])*100,
        'macro F1 score': f1_score(df["root"],df[name], average='macro') *100,
        'macro Recall':recall_score(df["root"],df[name], average='macro')*100,
        'macro Precision': precision_score(df["root"],df[name], average='macro')*100,
        
        # stem
        #~ "linguistics accuracy": cpt *100.0 / total,
        'Stem micro Accuracy': accuracy_score(df["lemma"],df[name+"_stem"])*100,
        'Stem micro F1 score': f1_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        'Stem micro Recall':recall_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        'Stem micro Precision': precision_score(df["lemma"],df[name+"_stem"], average='micro')*100,

        'Stem macro Accuracy': accuracy_score(df["lemma"],df[name+"_stem"])*100,
        'Stem macro F1 score': f1_score(df["lemma"],df[name+"_stem"], average='macro')*100,
        'Stem macro Recall':recall_score(df["lemma"],df[name+"_stem"], average='macro')*100,
        'Stem macro Precision': precision_score(df["lemma"],df[name+"_stem"], average='macro')*100,

        }
        #~ print "%s Stemmer [%d / %d] %.2f%%"%(name,cpt,total,  cpt *100.0 / total)
        #~ stats_list.append(stats)
    if stem_flag:
        print('********* STEMS ****************')
        for name in names:
            
            cpt = df[df.lemma == df[name+"_stem"]][name].count()
            print "%s Stemmer [%d / %d] %.2f%%"%(name,cpt,total,  cpt *100.0 / total)
    if lemma_flag:
        print('********* LEMMA ****************')
        for name in names:
            cpt = df[df.lemma == df[name+"_stem"]][name].count()
            print "%s Stemmer [%d / %d] %.2f%%"%(name,cpt,total,  cpt *100.0 / total)

    dstats = pd.DataFrame.from_dict(stats_list, orient='index')
    
    return dstats
    

def calcul_stats(dataframe, names, root_flag=True, stem_flag=False, lemma_flag=False, ):
    """
    Calculer 
    """
    df = dataframe
    #~ # display= data stats
    print('********* ROOT ****************')
    total = df.shape[0] # row number
    #~ stats_list={}
    stats_list = []
    for name in names:
        cpt_stem = df[df.lemma == df[name+"_stem"]][name].count()
        cpt = df[df.root == df[name]][name].count()
        stats_list.append({
        "name":name,
        "method":"root",
        "average":'micro',
        "count":cpt,
        "total":total,
        #~ "linguistics accuracy": cpt *100.0 / total,
        'Accuracy': accuracy_score(df["root"],df[name])*100,
        'F1 score': f1_score(df["root"],df[name], average='micro')*100,
        'Recall':recall_score(df["root"],df[name], average='micro')*100,
        'Precision': precision_score(df["root"],df[name], average='micro')*100,
        })
        stats_list.append({        
        "name":name,
        "method":"root",
        "average":'macro',
        "count":cpt,
        "total":total,
        'Accuracy': accuracy_score(df["root"],df[name])*100,
        'F1 score': f1_score(df["root"],df[name], average='macro') *100,
        'Recall':recall_score(df["root"],df[name], average='macro')*100,
        'Precision': precision_score(df["root"],df[name], average='macro')*100,
        })
        # stem
        #~ "linguistics accuracy": cpt *100.0 / total,
        stats_list.append({        
        "name":name,
        "method":"stem",
        "average":'micro',
        "count":cpt_stem,
        "total":total,
        'Accuracy': accuracy_score(df["lemma"],df[name+"_stem"])*100,
        'F1 score': f1_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        'Recall':recall_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        'Precision': precision_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        })
        stats_list.append({        
        "name":name,
        "method":"stem",
        "average":'macro',
        "count":cpt_stem,
        "total":total,
        'Accuracy': accuracy_score(df["lemma"],df[name+"_stem"])*100,
        'F1 score': f1_score(df["lemma"],df[name+"_stem"], average='macro')*100,
        'Recall':recall_score(df["lemma"],df[name+"_stem"], average='macro')*100,
        'Precision': precision_score(df["lemma"],df[name+"_stem"], average='macro')*100,

        })
        #~ print "%s Stemmer [%d / %d] %.2f%%"%(name,cpt,total,  cpt *100.0 / total)
        #~ stats_list.append(stats)

    if stem_flag:
        print('********* STEMS ****************')
        for name in names:
            
            cpt = df[df.lemma == df[name+"_stem"]][name].count()
            print "%s Stemmer [%d / %d] %.2f%%"%(name,cpt,total,  cpt *100.0 / total)
    if lemma_flag:
        print('********* LEMMA ****************')
        for name in names:
            cpt = df[df.lemma == df[name+"_stem"]][name].count()
            print "%s Stemmer [%d / %d] %.2f%%"%(name,cpt,total,  cpt *100.0 / total)

    #~ dstats = pd.DataFrame.from_dict(stats_list, orient='index')
    dstats = pd.DataFrame(stats_list)
    #~ decimals = pd.Series([2, 2, 2,2,2], index=['average', 'Accuracy', 'F1 score','Recall', 'Precision' ])        
    #~ dstats.round(decimals)
    
    return dstats
    
    
def test_stemmers(dataframe_result, data_path, names, names_to_control):
    """
    """
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
        print " Can't Open the given File ", filename;
        sys.exit();
    #~ if not options['limit'] : 
        #~ limit =  100000000
    #~ else: limit =0;
    df = df.replace(np.nan, '', regex=True)
    # prepare stemmers
    if all_stemmers:
        names = abstractstemmer.factory_stemmer.get_stemmers();
        names.extend(['khoja','farasa'])
        #~ names = ('default', 'custom',  'isri',"assem", "khoja","farasa", 'custom_stp', 'custom_roots')
    else:
        names = ("khoja", "khoja+rooter", "farasa+rooter", 'farasa')
    # add some stemmers to be controled under csv file 
    # show conditions
    names_to_control =["assem_stemmer","default","custom-affix"]
    # add features
    df = test_stemmers(df, data_path, names, names_to_control)

    # save file on csv
    df.to_csv(outfile, sep='\t', encoding='utf-8')
    
    dstats = calcul_stats(df, names, stem_flag = True)

    dstats.to_csv(outfile+".stats", sep='\t', encoding='utf-8')    
    print(dstats)
