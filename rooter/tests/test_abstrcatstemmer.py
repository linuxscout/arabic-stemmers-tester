#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test_abstrcatstemmer.py
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
import abstractstemmer
def main(args):
    word = u"يستعملونهم"
    
    for name in ('default', 'custom_tag', 'isri', 'assem'):
    #~ for name in ('default', 'custom'):
        asl = abstractstemmer.factory_stemmer.create_stemmer(name);
        print("%s Stemmer"%name)
        print asl.getstem(word)
        print asl.getroot(word)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))


def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
