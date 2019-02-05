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
from __future__ import (
    absolute_import,
    print_function,
    unicode_literals,
    division,
    )
import pyarabic.araby as araby
from pyarabic import stack
from pyarabic.araby import FEH, LAM, AIN, HARAKAT
from pyarabic.arabrepr import arepr
import roots_const
import re
import itertools

class abstractRooter:
    """
    """
    def __init__(self,):
        self.debug = False
        #~ self.debug = True

    @staticmethod    
    def debug_algo(debug, word,  level, name, candidats, roots, roots_tmp, accepted):
        if debug:
            print((u"*** Level %d: [%s] %s "%(level,name, word)).encode('utf8'))
            print("   Candidats    :", u"\t".join(candidats).encode('utf8'))
            print("   roots    :", u"\t".join(roots).encode('utf8'))
            print("   roots tmp:", u"\t".join(roots_tmp).encode('utf8'))
            print("   accepted :", u"\t".join(accepted).encode('utf8'))        
    def extract(self, stem):
        """ extract roots """
        pass
