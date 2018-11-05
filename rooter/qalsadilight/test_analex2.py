#!/usr/bin/python
# -*- coding = utf-8 -*-


import analex
#~ from __future__ import absolute_import
#~ from ..qalsadi import analex


filename="../tests/samples/text.txt"

myfile=open(filename)
text=(myfile.read()).decode('utf8');

try:
    myfile=open(filename)
    text=(myfile.read()).decode('utf8');

    if text == None:
        text=u"السلام عليكم يستعملونهم"
except:
    text=u"السلام عليكم يستعملونهم"
    print(" given text")

debug=False;
limit=500
analyzer=analex.Analex(cache_path="cache/")
#ianalyzer.disable_allow_cache_use()
analyzer.set_debug(debug);
result = analyzer.check_text(text);

import pandas as pd
adapted_result = []

for i, analyzed_list in enumerate(result):
    for analyzed in analyzed_list:
        adapted_result.append(analyzed.__dict__)


df = pd.DataFrame(adapted_result)
print(df.columns.values)
print(df.head(12))
display = df[['word','stem','type','root']]
display = display.drop_duplicates()
print(display.head(10))
#~ print(display)
print("root exists ", ('root' in df.columns))
display.to_csv('../tests/output/test2.csv',sep='\t', encoding="utf8")
