#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  read_config.py
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
import sys
import os.path
import configparser
import ast
class read_config:
    def __init__(self,):
        pass
    
def read_stemmers2(filename):


    newpath = os.path.join(sys.path[0], filename)
    try:
        fi = open(newpath,"r")
    except:
        print("can't open the specified file %s"%newpath)
        return False;
    lines=fi.readlines();
    lines = [l.strip() for l in lines]
    lines = [l for l in lines if l and not l.startswith("#")]
    # lines contains stemmers names
    return lines
    
def read_stemmers(filename, select = "all"):
    config = configparser.ConfigParser()
    newpath = os.path.join(sys.path[0], filename)
    config.read(newpath)
    try:
        config.read(newpath)
    except:
        print("can't open the specified file %s"%newpath)
        return False;    
    our = ast.literal_eval(config.get('Stemmers','our'))
    #~ print(our)
    others = ast.literal_eval(config.get('Stemmers','others'))
    assem = ast.literal_eval(config.get('Stemmers','assem'))
    #~ print(others)
    if select in ("our", "tashaphyne"):
        return our
    elif select == "others":
        return others
    elif select == "assem":
        return assem
    else:
        return others + our

def main(args):
    stemmers = read_stemmers("stemmers.conf")
    print(stemmers)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
