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

import pandas as pd
import sys
import re
import pyarabic.araby as araby
from pyarabic.arabrepr import arepr
ROOTONS = []
WAZNS = set([u'عاءل',
         u'فوعل',
         u'علل',
         u'علول',
         u'ضطعل',
         u'فتال',
         u'عليل',
         u'عاعل',
         u'فعال',
         u'فعاءل',
         u'فاءل',
         u'ل',
         u'عالل',
         u'عال',
         u'فتعيل',
         u'فيعل',
         u'فال',
         u'عل',
         u'علالل',
         u'زدعل',
         u'ع',
         u'عايل',
         u'عاليل',
         u'فعوعل',
         u'فل',
         u'فتعل',
         u'عولل',
         u'فعلال',
         u'فوعال',
         u'عع',
         u'فع',
         u'عللول',
         u'فاع',
         u'عيل',
         u'فيل',
         u'فاعيل',
         u'فتعال',
         u'فاعول',
         u'فعاع',
         u'فول',
         u'فعل',
         u'فعيل',
         u'عول',
         u'فطعل',
         u'فعول',
         u'فيال',
         u'علال',
         u'فتل',
         u'فعلل',
         u'فاعل'])
         
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
    
def generate_rooton_list(wazns_lines):
    global ROOTONS
    for l in wazns_lines:
        fields = l.split(';')
        wazn = fields[0]
        # extract rooton
        left = wazn.find(u'ف',1)
        if left <0:
            left = wazn.find(u'ع',1)
        right = wazn.find(u'ل',-1)
        if right <0:
            right = wazn.find(u'ع',-1)

        rooton = wazn[left:right+1]
        print u"\t".join([wazn, rooton])

    ROOTONS = set(ROOTONS)
    print 'ROOTONS'
    print repr(ROOTONS).decode('unicode-escape').encode('utf8')

    
def extract_rooton(s):
    """
    """
    return s[s.find('.',1):s.find('.',-1)+1]
    
def make_weak_rhyzome(rhyzome):
    """
    reduce a rhyzome to generate a reduced one
    """
    new_rhyz = []
    r2 = re.sub(u'[^فعل]','', rhyzome)
    #~ if araby.HEH in rhyzome or araby.MEEM in rhyzome:
        #~ return [] 
    if len(r2) <= 3:
        # remove Feh
        for c in (araby.FEH, araby.AIN, araby.LAM):
            rhyz = rhyzome.replace(c,'')
            # remove non Original letters
            rhyz = extract_rhyzome(rhyz)
            new_rhyz.append(rhyz)
    return new_rhyz
    

def test():
    # readfile
    filename = "samples/majdi-patterns.csv"
    outfile = "output/majdi-patterns.csv"
    try:
        df = pd.read_csv(filename, delimiter='\t',
          #~ names=['word', 'root', 'lemma', 'type','non'], 
          encoding = "utf-8",
          #~ skiprows=1,
          )
    except:
        print " Can't Open the given File ", filename;
        sys.exit();
    print(df.head())
    df['rhyzome'] = df['Pattern'].apply(extract_rhyzome)
    print('**********after rhyzome******')
    print(df.head())
    print(df.head(100))
        # save file on csv
    df.to_csv(outfile, sep='\t', encoding='utf-8')
    rhyzomes = list(df['rhyzome'].unique())
    # filter some rhyzomes
    # avoid some patterns
    rhyzomes = [r for r in rhyzomes if not( araby.HEH in r or araby.MEEM in r or araby.NOON in r)]

    print(u"****rhyzomes****")
    print(u"\n".join(rhyzomes).encode('utf8'))
    print(len(rhyzomes))
    reduced = []
    for r in rhyzomes:
        reduced.extend(make_weak_rhyzome(r))
    reduced = list(set(reduced))
    reduced = [x for x in reduced if x not in rhyzomes]
    print(u"****reduced****")
    print(u"\n".join(reduced).encode('utf8'))
    print(len(reduced))
    rhyzomes.extend(reduced)
    print('In wazns not in Rhyzomes')
    diff2 = [x for x in WAZNS if x not in rhyzomes]    
    print(arepr(diff2))    
    print('RHYZOMES=')
    print(arepr(rhyzomes))
    
def main(args):


    #~ generate_rooton_list()
    test()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
