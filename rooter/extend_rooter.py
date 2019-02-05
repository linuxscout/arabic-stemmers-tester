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
        
class extendRooter(abstractRooter):
    def __init__(self,):
        abstractRooter.__init__(self)

    @staticmethod
    #~ def extend_root(psudoroot, wazn =""):
    def extract(psudoroot):
        """ extend a psudo root"""
        extended = []
        # convert ALEF to WAW or YEH
        if araby.ALEF in psudoroot:
            extended.append(psudoroot.replace(araby.ALEF, araby.WAW))
            extended.append(psudoroot.replace(araby.ALEF, araby.YEH))
        #~ if len(psudoroot) == 3 and araby.YEH in psudoroot:
            #~ extended.append(psudoroot.replace(araby.YEH, araby.WAW))
        #~ if len(psudoroot) == 3 and araby.WAW in psudoroot:
            #~ extended.append(psudoroot.replace(araby.WAW, araby.YEH))
            #~ extended.append(psudoroot.replace(araby.ALEF, araby.YEH))
        # extend root according to length,
        # if wazn (rooton) is given we can know where to add missed letter
        if psudoroot in (u'خذ',u'مر',u'كل'):
            extended.append(araby.HAMZA + psudoroot)
        if len(psudoroot) == 2:
            # add Yeh or waw at begin
            extended.append(araby.WAW + psudoroot)
            #~ extended.append(araby.YEH + psudoroot)
            #~ extended.append(araby.HAMZA + psudoroot)
            # add Yeh or waw at middle
            extended.append("".join([psudoroot[0],araby.WAW, psudoroot[1]]))
            extended.append("".join([psudoroot[0],araby.YEH, psudoroot[1]]))
            # add Yeh or waw at end
            extended.append(psudoroot+araby.WAW)
            extended.append(psudoroot+araby.YEH)
            # add double letter جد =>جدد
            extended.append(psudoroot + psudoroot[-1:])

        return extended


