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
from abstract_rooter import abstractRooter
import roots_const
        
class virtualRooter(abstractRooter):
    def __init__(self,):
        abstractRooter.__init__(self)
        self.VIRTUAL_DICT ={}
        self.create_virtual_roots()

    def create_virtual_roots(self, ):
        if  self.VIRTUAL_DICT:
            return

        for root in roots_const.ROOTS:
            vrtl =  self.virtualize_root(root)
            #~ if vrtl != root:
            if vrtl in  self.VIRTUAL_DICT:
                 self.VIRTUAL_DICT[vrtl].append(root)
            else:
                 self.VIRTUAL_DICT[vrtl]= [root,]

    @staticmethod
    def virtualize_root(word):
        """ convert Weak letters into One code """
        word = word.replace(araby.ALEF, "?")
        word = word.replace(araby.YEH, "?")
        word = word.replace(araby.WAW, "?")
        word = word.replace(araby.ALEF_MAKSURA, "?")
        return word
                         
    #~ def is_virtual_root(self, word):
    def extract(self, word):
        """ test if word is a valid virtual root"""
        # calcul the virtual root
        vrtl =  self.virtualize_root(word)
        # lookup for virtual roots
        return  self.VIRTUAL_DICT.get(vrtl, [])
                


