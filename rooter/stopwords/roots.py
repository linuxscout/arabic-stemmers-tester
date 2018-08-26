#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  stopclass.py
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

import pyarabic.araby as araby
import roots_const

def is_root(word):
    """ test if word is a root"""
    return word in roots_const.ROOTS

def is_stamped_root(stamp):
    """ test if word is a stop"""
    pass
def stamp_root(word):
    """ stamp root"""
    return word

def main(args):
    word = u"لعلهم"
    word = u"علم"
    print is_root(word)
    return 0
    
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
