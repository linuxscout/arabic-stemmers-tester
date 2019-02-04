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
from sklearn.metrics import precision_score, recall_score,  accuracy_score, f1_score, confusion_matrix
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
        l= re.split("[;\+]", word)
        return max(l, key=len)
    return word    

  
def my_test(root_origin, root_calculated):
    """ exists root """
    roots = root_origin.split(';')
    return root_calculated in roots
def is_valid_root(x):
    """ is a valid root"""
    # if word is null
    if not x:
        return False
    # if the word contains latin chars
    if not araby.is_arabicword(x):
        return False
    # if root is more than 4 letters or less than three letters
    return (len(x) >= 3 and len(x)<=4 and araby.ALEF not in x)    
def is_valid_stem(stem):
    """ is a valid stem"""
    # if word is null
    if not stem:
        return False
    # test multiple stem
    #if all parts are null return False
    if ";" in stem:
        parts = [x for x in stem.split(';') if x]
        if not parts:
            return False
    else:
        # if the word contains latin chars
        if not araby.is_arabicword(stem):
            return False
    return True
    
def normalize_stem(word):
    return re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
    
def equal_stem(stem1, stem2):
    """ compare to stems"""
    # test if normalized stems are equal
    # Todo
    if stem1 == stem2:
        return True
    elif len(stem1) == len(stem2):
        return normalize_stem(stem1) == normalize_stem(stem2)
    else:
        #~ if ";" in stem2: # multipe choices
        stems = stem2.split(';')
        return stem1 in stems
    return False
            
def my_metric_test(root_origin, root_calculated):
    """ exists root """
    # how to examin metrics
    # TP : calculted root  is in root_orginal
    # TN : calculted root  is null and   root_orginal is null
    # FP : calculted root  is not null and   root_orginal is null
    # FN : calculted root  is incorrect and   root_orginal is not null
    if not is_valid_root(root_origin)  and not is_valid_root(root_calculated) :
            return "TN"
    elif not is_valid_root(root_origin)  and is_valid_root(root_calculated) :
            return "FP"
    elif is_valid_root(root_origin) and not is_valid_root(root_calculated):
        return "FN"
    elif is_valid_root(root_origin) and is_valid_root(root_calculated):    
        roots = root_origin.split(';')
        if root_calculated in roots:
            return "TP"
        else:
            return "FN"
    else:
        "NON"
    
def my_metric_stem_test(stem_origin, stem_calculated):
    """ exists stem """
    # how to examin metrics
    # TP : calculted stem  is in stem_orginal
    # TN : calculted stem  is null and   stem_orginal is null
    # FP : calculted stem  is not null and   stem_orginal is null
    # FN : calculted stem  is incorrect and   stem_orginal is not null
    if not is_valid_stem(stem_origin)  and not is_valid_stem(stem_calculated) :
            return "TN"
    elif not is_valid_stem(stem_origin)  and is_valid_stem(stem_calculated) :
            return "FP"
    elif is_valid_stem(stem_origin) and not is_valid_stem(stem_calculated):
        return "FN"
    elif is_valid_stem(stem_origin) and is_valid_stem(stem_calculated):    
        if equal_stem(stem_calculated, stem_origin):
            return "TP"
        else:
            return "FN"
    else:
        "NON"
    
def calcul_stats(dataframe, names, root_flag=True, stem_flag=False, lemma_flag=False, ):
    """
    Calculer 
    """
    df = dataframe
    #~ # display= data stats
    #~ print('********* ROOT ****************')
    total = df.shape[0] # row number
    #~ stats_list={}
    stats_list = []
    for name in names:
        name_stem = name+"_stem"
        cpt_stem = df[df.lemma == df[name+"_stem"]][name].count()
        #~ cpt = df[df.root == df[name]][name].count()
        df['Value'] = df.apply(lambda row: my_test(row['root'], row[name]), axis=1)
        df['metric'] = df.apply(lambda row: my_metric_test(row['root'], row[name]), axis=1)
        #~ cpt = df[df.root  in df[name].split(';')][name].count()
        cpt = df[df.Value == True][name].count()
        TP = df[df.metric == "TP"][name].count()
        TN = df[df.metric == "TN"][name].count()
        FP = df[df.metric == "FP"][name].count()
        FN = df[df.metric == "FN"][name].count()
        # stem_metricx
        df['metric_stem'] = df.apply(lambda row: my_metric_stem_test(row['lemma'], row[name_stem]), axis=1)
        TP_stem = df[df.metric_stem == "TP"][name_stem].count()
        TN_stem = df[df.metric_stem == "TN"][name_stem].count()
        FP_stem = df[df.metric_stem == "FP"][name_stem].count()
        FN_stem = df[df.metric_stem == "FN"][name_stem].count()        
        stats_list.append({
        "name":name,
        "method":"root",
        "average":'micro',
        "count":cpt,
        "total":total,
        "TN":TN,
        "FN":FN,
        "TP":TP,
        "FP":FP,        
        #~ "Accuracy": cpt *100.0 / total,
        #~ 'Accuracy': accuracy_score(df["root"],df[name])*100,
        #~ 'F1 score': f1_score(df["root"],df[name], average='micro')*100,
        #~ 'Recall':recall_score(df["root"],df[name], average='micro')*100,
        #~ 'Precision': precision_score(df["root"],df[name], average='micro')*100,
        'Accuracy': (TP+TN)*100.0/(TP+TN+FP+FN),
        'F1 score': 2*TP*100.0/(2*TP+FP+FN),
        'Recall': TP*100.0/(TP+FN),
        'Precision': TP*100.0/(TP+FP),
        
        })
        #~ stats_list.append({        
        #~ "name":name,
        #~ "method":"root",
        #~ "average":'macro',
        #~ "count":cpt,
        #~ "total":total,
        #~ 'Accuracy': accuracy_score(df["root"],df[name])*100,
        #~ 'F1 score': f1_score(df["root"],df[name], average='macro') *100,
        #~ 'Recall':recall_score(df["root"],df[name], average='macro')*100,
        #~ 'Precision': precision_score(df["root"],df[name], average='macro')*100,
        #~ })
        # stem
        #~ "linguistics accuracy": cpt *100.0 / total,
        stats_list.append({        
        "name":name,
        "method":"stem",
        "average":'micro',
        "count":cpt_stem,
        "total":total,
        "TN":TN_stem,
        "FN":FN_stem,
        "TP":TP_stem,
        "FP":FP_stem,         
        #~ 'Accuracy': accuracy_score(df["lemma"],df[name+"_stem"])*100,
        #~ 'F1 score': f1_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        #~ 'Recall':recall_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        #~ 'Precision': precision_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        'Accuracy': (TP_stem+TN_stem)*100.0/(TP_stem+TN_stem+FP_stem+FN_stem),
        'F1 score': 2*TP_stem*100.0/(2*TP_stem+FP_stem+FN_stem),
        'Recall': TP_stem*100.0/(TP_stem+FN_stem),
        'Precision': TP_stem*100.0/(TP_stem+FP_stem),        
        })
        #~ stats_list.append({        
        #~ "name":name,
        #~ "method":"stem",
        #~ "average":'micro1',
        #~ "count":cpt_stem,
        #~ "total":total,
        #~ 'Accuracy': accuracy_score(df["lemma"],df[name+"_stem"])*100,
        #~ 'F1 score': f1_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        #~ 'Recall':recall_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        #~ 'Precision': precision_score(df["lemma"],df[name+"_stem"], average='micro')*100,
        #~ 'Accuracy': (TP_stem+TN_stem)*100.0/(TP_stem+TN_stem+FP_stem+FN_stem),
        #~ 'F1 score': 2*TP_stem*100.0/(2*TP_stem+FP_stem+FN_stem),
        #~ 'Recall': TP_stem*100.0/(TP_stem+FN_stem),
        #~ 'Precision': TP_stem*100.0/(TP_stem+FP_stem),        
        #~ })
        #~ stats_list.append({        
        #~ "name":name,
        #~ "method":"stem",
        #~ "average":'macro',
        #~ "count":cpt_stem,
        #~ "total":total,
    
        #~ 'Accuracy': accuracy_score(df["lemma"],df[name+"_stem"])*100,
        #~ 'F1 score': f1_score(df["lemma"],df[name+"_stem"], average='macro')*100,
        #~ 'Recall':recall_score(df["lemma"],df[name+"_stem"], average='macro')*100,
        #~ 'Precision': precision_score(df["lemma"],df[name+"_stem"], average='macro')*100,
        #~ })

        

    #~ if stem_flag:
        #~ print('********* STEMS ****************')
        #~ for name in names:
            
            #~ cpt = df[df.lemma == df[name+"_stem"]][name].count()
            #~ print "%s Stemmer [%d / %d] %.2f%%"%(name,cpt,total,  cpt *100.0 / total)
    #~ if lemma_flag:
        #~ print('********* LEMMA ****************')
        #~ for name in names:
            #~ cpt = df[df.lemma == df[name+"_stem"]][name].count()
            #~ print "%s Stemmer [%d / %d] %.2f%%"%(name,cpt,total,  cpt *100.0 / total)

    #~ dstats = pd.DataFrame.from_dict(stats_list, orient='index')
    dstats = pd.DataFrame(stats_list)
    #~ decimals = pd.Series([2, 2, 2,2,2], index=['average', 'Accuracy', 'F1 score','Recall', 'Precision' ])        
    #~ dstats.round(decimals)
    
    return dstats
    
    
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

    # filter stopwords and non arabic words
    
    # prepare stemmers
    names = read_config.read_stemmers(STEMMERS_CONFIG,"tashaphyne")
    if not names:
        print ("Error on reading config file %s"%STEMMERS_CONFIG)
        sys.exit()

    # add some stemmers to be controled under csv file 
    # show conditions
    #~ names_to_control =["rhyzome","default","custom-root"]
    names_to_control =[]
    # add features
    df2 = test_stemmers(df, data_path, names, names_to_control)

    # save file on csv
    df2.to_csv(outfile, sep='\t', encoding='utf-8')
    
    #~ dstats = calcul_stats(df2, names, stem_flag = True)

    #~ dstats.to_csv(outfile+".stats", sep='\t', encoding='utf-8')    
    #~ print(dstats)



