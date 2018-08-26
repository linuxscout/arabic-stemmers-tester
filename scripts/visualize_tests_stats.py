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
        Visualize charts from test stats
"""

import sys
if __name__ == "__main__":

    sys.path.append('../support')
    sys.path.append('../')

import re
import argparse
import os
import pandas as pd
from sklearn.metrics import precision_score, recall_score,  accuracy_score, f1_score
import numpy as np
import matplotlib.pyplot as plt


def grabargs():
    parser = argparse.ArgumentParser(description='Convert Quran Corpus into CSV format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outfile", required=True,
    help="Output file to convert", metavar="OUT_FILE")
    
    parser.add_argument("--all", type=bool, nargs='?',
                        const=True, 
                        help="Test all stemmers.")
    args = parser.parse_args()
    return args
def visualize_latex(dtf , columns, outfile):
    """ convert data into latex table """
    df2 = dtf[columns]
    df2.to_latex(outfile+".tex", bold_rows= True, encoding='utf8')
    print("Data is written in %s"%outfile+".tex")
    
def visualize_latex_string(dtf , caption="", label=""):
    """ convert data into latex table """
    #~ if columns:
        #~ df2 = dtf[df['method']==method, df['average']==metric_class]
    #~ else:
        #~ df2 = dtf
    #~ df2 = dtf[dtf['method']==method & dtf['average']==metric_class]
    df2= dtf
    tex = """
    \\begin{table} 
    %s
    \\caption{%s}
    \\label{%s:table}
    \\end{table}""" %(df2.to_latex(bold_rows= True, encoding='utf8'),
    caption, label,
    )
    return tex+'\n'
    #~ print("Data is written in %s"%outfile+".tex")
    
    
def figure_latex_string(caption="", label=""):
    """ return a figure latex code """
    tex = """
\\begin{figure}
    \\centering
    \\includegraphics[width=0.7\\linewidth]{images/%s}
    \\caption{%s}
    \\label{fig:%s}
\\end{figure}
    """ %(label, caption, label,
    )
    return tex+'\n'
    #~ print("Data is written in %s"%outfile+".tex")
    

def main():
    print("""
This program will generate Latex table codes and somes figures from statistics files from
Input files: are mentioned in the code, you must changes it if you want more files
output file:
    output/images
    tex file: outfile
    output/global.stats.csv: all joined data
    """)
    args =grabargs()
    filename = args.filename
    outfile = args.outfile
    #~ data_directory = args.data_directory
    all_stemmers = args.all
    # column types
    columns=[ 'total',
        'Accuracy',
        'F1 score',
        'Precision',
        'Recall',
        'count',
        ]
    columns_type={
        'count':np.int64,
        'Precision':np.float32,
        'Recall':float,
        'Accuracy':float,
        'F1 score':float,
        'total':np.int64,
        }

    names ={"qindex":{'filename':'output/quran_word_v0.5.2.csv.stats', 'desc':'Quran word index'},
    
        "gold":{'filename':'output/gold.csv.stats',  'desc':"Arabic Golden Corpus"},
        "nafis":{'filename':'output/nafis.unq.stats', 'desc':"NAFIS"},
        "qcorpus":{'filename': 'output/qc.unq.stats', 'desc':"Quranic Arabic Corpus"},
    }
    pd.options.display.float_format = '{:,.2f}'.format
    try:
        outputfile = open(outfile+".tex","w")
    except:
        print ("Can't open file %s"%outfile)
        sys.exit()
    frames = []
    for key in names:
        filename = names[key]["filename"]
        df = pd.read_csv(filename, delimiter='\t',
              encoding = "utf-8",
              dtype = columns_type, 
              )
        # rename first columns
        #~ u'Unnamed: 0'
        #~ df = df.rename(columns={u'Unnamed: 0': 'stemmer', })
        #add a new columns
        df['dataset'] = key
        # add frame to list in order to merge all data
        frames.append(df)

        print df.head(2)
        mytables=[{'caption'   : "Linguistic Accuracy and Micro classification F1-score on %s dataset "%names[key]["desc"],
            'label' : "%s-micro"%key,
            'method':'root', 'average':'micro',
            },
            {
            'caption'   : "Macro classification on %s dataset "%names[key]["desc"],
            'label' : "%s-macro"%key,
            'method':'root', 'average':'macro',
            },
            {
            'caption'   : "Stem Extraction evaluation  Micro classification on %s dataset "%names[key]["desc"],
            'label' : "%s-stmmicro"%key,

            'method':'stem', 'average':'micro',            
            },
            {
            'caption'   : "Stem Extraction evaluation  Macro classification on %s dataset "%names[key]["desc"],
            'label' : "%s-stmmacro"%key,

            'method':'stem', 'average':'macro',
            },
            ]
        for mytab in mytables:
            outputfile.write("%% test of %s\n"%key)    
            caption   = "Linguistic Accuracy and Micro classification F1-score on %s dataset "%names[key]["desc"]
            label = "%s-micro"%key
            df_c = df[(df.method ==mytab['method'])&(df['average'] == mytab['average'])]
            tex = visualize_latex_string( df_c, mytab['caption'], mytab['label'])
            outputfile.write(tex)


    # merge all data to build a pivot table
    df_global = pd.concat(frames)
    #  CHarts to generate 
    mycharts=[
    {'method':'root', 'average':'micro',
    'field':'Accuracy', 'caption':"Root Extraction evaluation,Linguistic accuracy "},
    {'method':'root', 'average':'micro',
    'field':'F1 score', 'caption':"Root Extraction evaluation, Micro classification "},
    {'method':'root', 'average':'macro',
    'field':'F1 score','caption':"Root Extraction evaluation, Macro classification "},
    {'method':'stem', 'average':'micro',
    'field':'F1 score', 'caption':"Stem Extraction evaluation, Macro classification "},
    {'method':'stem', 'average':'macro',
    'field':'F1 score', 'caption':"Stem Extraction evaluation, Micro classification "},
    ]
    for mych in mycharts:
        field = mych.get('field','')
        caption =   mych.get('caption','') 
        method =  mych.get('method','') 
        average =  mych.get('average','') 
        label = "%s-%s-%s"%(method, average, field.replace(' ','-'))
        dfg= df_global[(df_global['method']==method) & (df_global['average']==average )]
        #~ print dfg.head(5)
        #~ continue
        # pivoting table
        df_pivot = dfg.pivot(index='name', columns='dataset', values=field)
        
        
        # generate data to latex
        tex = visualize_latex_string(df_pivot, caption=caption, label=label)
        outputfile.write(tex)

        # the latex code in not ordered to get homogenous tables
        # order by best max, in order to get a readable chart
        df_pivot.sort_values(by='gold', ascending = True, inplace=True)        
        # generate the latex figure code
        tex = figure_latex_string(caption=caption, label=label)
        outputfile.write(tex)

        # generate the plot
        plt.figure()
        df_pivot.plot(rot=15)
        plt.savefig("output/images/%s.png"%label)  
        df_pivot.to_csv("output/pivots/%s.csv"%label, sep='\t',encoding='utf8')

    df_global.to_csv("output/global.stats.csv", sep='\t', encoding='utf8')
    print("Global Stats are stored in output/global.stats.csv")
    print("Pivots tables Stats are stored in output/pivots/*.csv")
    #~ print df_global
if __name__ == '__main__':
    main()
