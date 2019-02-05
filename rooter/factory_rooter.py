#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  factory_rooter.py
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
from rhyzome_rooter import rhyzomeRooter
from stamp_rooter import stampRooter
from virtual_rooter import virtualRooter
from extend_rooter import extendRooter
from matrix_rooter import matrixRooter

class factory_rooter(object):
    """ a factory for stemmers"""
    @staticmethod
    def get_rooters():
        """
        get the name list of exisiting rooters
        """
        namelist =["default",
        "rhyzome",
        "virtual",
        "stamp",
        "extend",
        ]
        return namelist
    @staticmethod
    def create_rooter(name):
        """
        """
        if name == "default":
            """ no options"""
            art = abstractRooter()
        elif name == "rhyzome":
            """ no options"""
            art = rhyzomeRooter()
        elif name == "stamp":
            """ no options"""
            art = stampRooter()
        elif name == "virtual":
            """ no options"""
            art = virtualRooter()
        elif name == "extend":
            """ no options"""
            art = extendRooter()
        elif name == "matrix":
            """ no options"""
            art = matrixRooter()
        else:
            """ no options"""
            art = abstractRooter()            
        return art
            
    def help():
        """ Display help of stemmers"""
        pass
        print("Available stemmers are:\n%s"%get_rooters())
        
    
