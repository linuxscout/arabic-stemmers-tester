#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  specialwords.py
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

SPECIAL_WORDS= {
u"الله":{"stem":"الله", "root":"الله",
u'يوسف':{'stem':u'يوسف', 'root':u'يوسف'},
u'يعقوب':{'stem':u'يعقوب', 'root':u'يعقوب'},
u'يعوق':{'stem':u'يعوق', 'root':u'يعوق'},
u'يغوث':{'stem':u'يغوث', 'root':u'يغوث'},
u'يونس':{'stem':u'يونس', 'root':u'يونس'},
u'يحيى':{'stem':u'يحيى', 'root':u'يحيى'},
u'يأجوج':{'stem':u'يأجوج', 'root':u'يأجوج'},
u'ياقوت':{'stem':u'ياقوت', 'root':u'ياقوت'},
u'يثرب':{'stem':u'يثرب', 'root':u'يثرب'},
u'فرعون':{'stem':u'فرعون', 'root':u'فرعون'},
u'بين':{'stem':u'بين', 'root':u'بين'},
u'مسكين':{'stem':u'مسكين', 'root':u'مسكين'},
u'دين':{'stem':u'دين', 'root':u'دين'},
u'دون':{'stem':u'دون', 'root':u'دون'},
u'قارون':{'stem':u'قارون', 'root':u'قارون'},
u'يم':{'stem':u'يم', 'root':u'يم'},
u'يقين':{'stem':u'يقين', 'root':u'يقين'},
u'يقطين':{'stem':u'يقطين', 'root':u'يقطين'},
u'لون':{'stem':u'لون', 'root':u'لون'},
u'هارون':{'stem':u'هارون', 'root':u'هارون'},
u'يم':{'stem':u'يم', 'root':u'يم'},
u'يوم':{'stem':u'يوم', 'root':u'يوم'},
u'يد':{'stem':u'يد', 'root':u'يد'},
u'يذر':{'stem':u'وذر', 'root':u'يذر'}

}
def is_special(word):
    return word in SPECIAL_WORDS
def stem_special(word):
    """ return stem for special word"""
    return SPECIAL_WORDS.get(word, {}).get('stem','')
    
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
