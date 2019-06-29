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
import numpy as np
import matplotlib.pyplot as plt


def grabargs():
    parser = argparse.ArgumentParser(description='Convert Quran Corpus into CSV format.')
    # add file name to import and filename to export
    
    parser.add_argument("-f", dest="filename", required=True,
    help="input file to convert", metavar="FILE")
    
    parser.add_argument("-o", dest="outdir", required=True,
    help="Output directory to use", metavar="OUT_DIR")
    
    parser.add_argument("--all", type=bool, nargs='?',
                        const=True, 
                        help="Test all stemmers.")
    args = parser.parse_args()
    return args

class abstractVisualizer:
    def __init(self, method='root'):
        pass;
    def pivot(self,method="root"):
        pass
    def global_stats(self, method="root"):
        pass
    def display(self,):
        pass
    def save(self,):
        pass
    
class csvVisualizer(abstractVisualizer):
    def __init(self, method='root'):
        abstractVisualizer.__init(self, method)

class latexVisualizer():
    def __init__(self, method='root'):
        #~ abstractVisualizer.__init(self, method)
        self.tex = u""
       
    def save(self, outfile):
        """ convert data into latex table """
        tex_doc =u"""\\documentclass[12pt]{report}
\\usepackage[utf8]{inputenc}
\\usepackage{amsmath}
\\usepackage{amsfonts}
\\usepackage{amssymb}
\\usepackage{graphicx}
\\usepackage{booktabs}
\\author{Taha Zerrouki}
\\begin{document}
%s
\\end{document}"""%self.tex

        try:
            outputfile = open(outfile+".tex","w")
        except:
            print ("Can't open file %s"%outfile)
            sys.exit()

        outputfile.write(tex_doc)
        outputfile.close()
        
        
        
    def latex_string(self,dtf , caption="", label=""):
        """ convert data into latex table """
        tex = """\\begin{table} 
    %s
    \\caption{%s}
    \\label{%s:table}
    \\end{table}""" %(dtf.to_latex(bold_rows= True, encoding='utf8'),
        caption, label,
        )

        tex+='\n'
        self.tex += tex    
        return tex
       
    def figure_latex_string(self, caption="", label=""):
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
        tex+='\n'
        self.tex += tex    
        return tex        
    

    
def generate_pivots(df_global, method, field):

        dfg= df_global[(df_global['method']==method)]

        # pivoting table
        df_pivot = dfg.pivot(index='name', columns='dataset', values=field)
        # the latex code in not ordered to get homogenous tables
        # order by best max, in order to get a readable chart
        df_pivot.sort_values(by='gold', ascending = True, inplace=True)        

        # pivot global
        df_pivot_global = dfg.pivot(index='name', columns='dataset',)
        
        return df_pivot_global, df_pivot
        
def plot_latex(latexer, method, field, df_pivot, df_pivot_global, outdir):
        """ display a plot and latex """
        caption =   "%s for %s Extraction evaluation"%(field, method)        
        label = "%s-%s"%(method, field.replace(' ','-'))
        # generate the plot
        plt.figure()
        df_pivot.plot(rot=15)
        plt.savefig(os.path.join(outdir, "images/%s.png"%label))  
        df_pivot.to_csv(os.path.join(outdir,"pivots/%s.csv"%label), sep='\t',encoding='utf8')

        df_pivot_global.to_csv(os.path.join(outdir,"pivots/global-%s.csv"%method), sep='\t',encoding='utf8')
        # generate data to latex
        latexer.latex_string(df_pivot, caption=caption, label=label)
        # generate the latex figure code
        latexer.figure_latex_string(caption=caption, label=label)
        # generate data to latex
        latexer.latex_string(df_pivot_global, caption="Global pivot", label="globle pivot")
        # save
        #~ latexer.save(outputfile)

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
    outdir = args.outdir
    outfile = os.path.join(outdir,"visualize.tex")
    detailed_tables = False
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

    #~ names ={"qindex":{'filename':'output/stats/quran_word_v0.5.2.csv.stats', 'desc':'Quran word index'},
    names ={"qindex":{'filename':'output/stats/klm.csv.stats', 'desc':'Quran word index'},
    
        "gold":{'filename':'output/stats/gold.csv.stats',  'desc':"Arabic Golden Corpus"},
        "nafis":{'filename':'output/stats/nafis.unq.stats', 'desc':"NAFIS"},
        "qcorpus":{'filename': 'output/stats/qc.unq.stats', 'desc':"Quranic Arabic Corpus"},
        "qwc":{'filename': 'output/stats/qwc.csv.stats', 'desc':"Mushaf Corpus"},
        "kb":{'filename': 'output/stats/kabi.v2.csv.stats', 'desc':"Kabi Corpus"},
        "qlb":{'filename': 'output/stats/qlbstem.unq.csv.stats', 'desc':"QLB Corpus"},
    }
    pd.options.display.float_format = '{:,.2f}'.format

    frames = []
    latexer = latexVisualizer()
    dataframes ={"root":None, "stem":None, "lemma":None}

    for method in ('root','stem'):
        for key in names:
            filename = names[key]["filename"]+"."+method
            df = pd.read_csv(filename, delimiter='\t', 
                  encoding = "utf-8",
                  dtype = columns_type, 
                  )
            #add a new columns
            df['dataset'] = key
            # add frame to list in order to merge all data
            frames.append(df)
            #~ print df.head(2)
        # merge all data to build a pivot table
        dataframes[method] = pd.concat(frames)
    #  CHarts to generate 
    mycharts=[
    {'method':'root', 'field':'Accuracy'},
    {'method':'root', 'field':'F1 score'},
    {'method':'stem', 'field':'F1 score'},
    {'method':'stem', 'field':'Accuracy'},
    ]
    for mych in mycharts:
        field = mych.get('field','')
        method =  mych.get('method','') 
        df_global = dataframes[method]
        df_pivot_global, df_pivot = generate_pivots(df_global, method, field) 
        plot_latex(latexer, method, field, df_pivot, df_pivot_global, outdir)
    latexer.save(outfile)

    df_global.to_csv(os.path.join(outdir,"global.stats.csv"), sep='\t', encoding='utf8')
    print("Global Stats are stored in output/global.stats.csv")
    print("Pivots tables Stats are stored in output/pivots/*.csv")
    #~ print df_global
if __name__ == '__main__':
    main()
