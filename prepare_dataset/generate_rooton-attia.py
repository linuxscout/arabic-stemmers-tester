#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generate_rooton.py
#  
#  Copyright 2018 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

ROOTONS = []
import pandas as pd
import pyarabic.trans as arabtrans
import pyarabic.araby as araby
from pyarabic.arabrepr import arepr
def classify_rhyzome(rhyzome):
    """ class rhyzome if it's weak or unweak """
    if not araby.FEH in rhyzome:
        return "weak"
    if not araby.AIN in rhyzome:
        return "weak"
    if not araby.LAM in rhyzome:
        return "weak"
    return "unweak"
def extract_rhyzome(wazn):
    """ extract rhuzom from a wazn word """
    # extract rooton
    wazn = araby.strip_tashkeel(wazn)
    left = wazn.find(u'ف')
    if left <0:
        left = wazn.find(u'ع')
    #~ right = wazn.find(u'ل',-1)
    right = wazn.rfind(u'ل')
    if right <0:
        #~ right = wazn.find(u'ع',-1)
        right = wazn.rfind(u'ع')
    rooton = wazn[left:right+1]
    if not rooton:
        print((u"**Debug %s [%d,%d]"%(wazn, left, right)).encode('utf8'))
    return rooton
def generate_rooton_list():
    global ROOTONS
    for l in wazns_lines:
        fields = l.split(';')
        wazn = fields[0]
        # extract rooton
        left = wazn.find(u'ف')
        if left <0:
            left = wazn.find(u'ع')
        right = wazn.rfind(u'ل')
        if right <0:
            right = wazn.rfind(u'ع')
        
        rooton = wazn[left:right+1]
        print u"\t".join([wazn, rooton])
        ROOTONS.append(rooton)
    ROOTONS = set(ROOTONS)
    print 'ROOTONS'
    print repr(ROOTONS).decode('unicode-escape').encode('utf8')

    
def extract_rooton(s):
    """
    """
    return s[s.find('.',1):s.find('.',-1)+1]
    

def preprocess(word):
    """ the string is proceded by a field name"""
    s = word.split(':')
    if len(s)>=2:
        if s[0]== 'examples' and len(s)>2:
            return u', '.join(s[1:])
        else:
            return s[1]
            
    else:
        return word

def main(args):
    df = pd.read_csv("samples/Arabic-patterns/Arabic-patterns-tabbed-v2.txt",
       encoding='utf8',
    delimiter = '\t',
    )
    outfile = "output/Arabic-patterns-tabbed.csv"
    # preprocess columns
    for name in df.columns.values:
        #~ print name
        df[name] = df[name].apply(preprocess)
    # convert trans 
    df["pattern"] = df["pattern"].apply(arabtrans.tim2utf8)
    df.to_csv(outfile+"debug", sep='\t', encoding='utf-8')
    df["singularPattern"] = df["singularPattern"].apply(arabtrans.tim2utf8)
    df['rhyzome'] = df['pattern'].apply(extract_rhyzome)
    df['unvocalized'] = df['pattern'].apply(araby.strip_tashkeel)
    df['weak'] = df['rhyzome'].apply(classify_rhyzome)
    df['weak'] = df['rhyzome'].apply(classify_rhyzome)

    print(df.head())
    #~ generate_rooton_list()
    df.sort_values(by=['rhyzome'], ascending=True, inplace=True)
    df2 = df[[ 'rhyzome','pattern', 'weak', 'examples']]#, 'singularPattern', 'type', 'nType', 'vType', 'isBrokenPlural', 'hasBrokenPlural', 'hasFem', 'subOf','examples']
    df2 = df[[ 'rhyzome','unvocalized', 'pattern', 'weak', 'examples']]#, 'singularPattern', 'type', 'nType', 'vType', 'isBrokenPlural', 'hasBrokenPlural', 'hasFem', 'subOf','examples']
    
    df2.to_csv(outfile, sep='\t', encoding='utf-8')
    rhyzomes = list(df['rhyzome'].unique())
    print(arepr(rhyzomes))
    return 0

if __name__ == '__main__':

    import sys
    sys.exit(main(sys.argv))
