#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  abstracttester.py
#  
#  Copyright 2019 zerrouki <zerrouki@majd4>
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
import re
import pandas as pd

import pyarabic.araby as araby
class abstractTester:
    def __init__(self, method):
        # root, stem, lemma
        self.method = method
        self.target_column = method        
    def is_valid(self, stem):
        """  test if stem is valid """
        return True
    
    def normalize(self, stem):
        """  normalize the stem """
        
        return stem
    
    def my_test(self, origin, output):
        """ exists root """
        choices = origin.split(';')
        return output in choices 
              
    def equal2(self, output, origin):
        """ test if calcuated is equal to origin """
        # test if normalized choices are equal
        # Todo
        if output == origin:
            return True
        elif len(output) == len(origin):
            return self.normalize(output) == self.normalize(origin)
        else:
            #~ if ";" in origin: # multipe choices
            choices = origin.split(';')
            choices = [self.normalize(s) for s in choices]
            return self.normalize(output) in choices
        return False
    def equal(self, output, origin):
        """ test if calcuated is equal to origin """
        # test if normalized choices are equal
        # Todo
        if output == origin:
            return True
        elif len(output) == len(origin):
            return output == self.normalize(origin)
        else:
            #~ if ";" in origin: # multipe choices
            choices = origin.split(';')
            choices = [self.normalize(s) for s in choices]
            return output in choices
        return False

    def metric_test(self,  origin, calculated):
        """  Calculate TP, TN, FP, FN """
        # how to examin metrics
        # TP : calculted   is in _orginal
        # TN : calculted   is null and   _orginal is null
        # FP : calculted   is not null and   _orginal is null
        # FN : calculted   is incorrect and   _orginal is not null
        valid_origin = self.is_valid(origin)
        valid_calculated = self.is_valid(calculated)
        if not valid_origin and not valid_calculated :
                return "TN"
        elif not valid_origin and valid_calculated :
                return "FP"
        elif valid_origin and not valid_calculated:
            return "FN"
        elif valid_origin and valid_calculated:    
            #~ s = origin.split(';')
            if self.equal(calculated, origin):
                return "TP"
            else:
                return "FN"
        else:
            "NON"

    def calcul_stats(self, dataframe, names):
        """ calculat stats """
        df = dataframe
        total = df.shape[0] # row number
        #~ stats_list={}
        stats_list = []
        for name in names:
            # to do remove
            #~ df['Value'] = df.apply(lambda row: self.my_test(row['root'], row[name]), axis=1)
            #~ cpt = df[df.Value == True][name].count()
            if self.method == "stem":
                key = name+'_stem'
            else:
                key = name

            df['metric'] = df.apply(lambda row: self.metric_test(row[self.target_column], row[key]), axis=1)

            TP = df[df.metric == "TP"][name].count()
            TN = df[df.metric == "TN"][name].count()
            FP = df[df.metric == "FP"][name].count()
            FN = df[df.metric == "FN"][name].count()
            
            stats_list.append({
            "name":name,
            "method": self.method,
            #~ "average":'milcro',
            #~ "count":cpt,  # to remove
            "total":total,
            "TN":TN,
            "FN":FN,
            "TP":TP,
            "FP":FP,        
            'Accuracy': (TP+TN)*100.0/(TP+TN+FP+FN),
            'F1 score': 2*TP*100.0/(2*TP+FP+FN),
            'Recall': TP*100.0/(TP+FN),
            'Precision': TP*100.0/(TP+FP),
            })
        dstats = pd.DataFrame(stats_list)
    
        return dstats

class stemmingTester(abstractTester):
    """ Test stemming process"""
    def __init__(self,):
        abstractTester.__init__(self, method="stem")
        #load parent
        self.method = "stem"
        self.target_column = "lemma"
        self.normalize_full = True
        
    def is_valid(self, stem):
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
    
    def normalize(self, word):
        """  normalize the stem """
        if self.normalize_full:
            word = word.replace(araby.ALEF_HAMZA_ABOVE,araby.ALEF)
            word = word.replace(araby.ALEF_HAMZA_BELOW,araby.ALEF)
            word = word.replace(araby.YEH_HAMZA,araby.HAMZA)
            word = word.replace(araby.WAW_HAMZA,araby.HAMZA)
            #~ word = word.replace(araby.YEH_HAMZA,araby.YEH)
            #~ word = word.replace(araby.WAW_HAMZA,araby.WAW)
            word = word.replace(araby.ALEF_MAKSURA, araby.YEH)
            # to choose Teh marbuta as Heh or TEH or remove it
            word = word.replace(araby.TEH_MARBUTA, "")
            #~ word = word.replace(araby.TEH_MARBUTA, araby.TEH)

        word = re.sub(u"[%s]"%(araby.ALEF_MADDA), araby.HAMZA+araby.ALEF, word)
        return word
    

class rootingTester(abstractTester):
    """ Test rooting process"""
    def __init__(self,):
        #load parent
        abstractTester.__init__(self, method="root")        
        self.method = "root"
        self.target_column = "root"
    def is_valid(self, word):
        """ is a valid root"""
        # if word is null
        if not word:
            return False
        # if the word contains latin chars
        if not araby.is_arabicword(word):
            return False
        # if root is more than 4 letters or less than three letters
        return (len(word) >= 3 and len(word)<=4 and araby.ALEF not in word)   
    
    def normalize(self, word):
        """  normalize the root """
        return word

class factory_tester(object):
    """ a factory for tester"""
    @staticmethod
    def get_testers():
        """
        get the name list of exisiting tester
        """
        namelist =["stem",
        "root",
        "lemma",
        ]
        return namelist    
    @staticmethod
    def create_tester(name):
        """
        """
        if name == "root":
            """ no options"""
            asl = rootingTester()
        elif name == "stem":
            """ no options"""
            asl = stemmingTester()
        elif name == "lemma":
            """ no options"""
            asl = lemmatizerTester()
        else:
            """ no options"""
            asl = abstractTester()            
        return asl
            
    def help():
        """ Display help of testers"""
        pass
        print("Available testers are:\n%s"%get_stemmers())
 

def main(args):
    stem_tester = stemmingTest()
    root_tester = rootingTest()
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
