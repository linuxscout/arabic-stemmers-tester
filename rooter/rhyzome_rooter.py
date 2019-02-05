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
import pyarabic.stack as stack
from pyarabic.araby import FEH, LAM, AIN, HARAKAT
from abstract_rooter import abstractRooter
AFFIXATION_LETTERS = u"أابةتدسطفكلمنهويءئى"
   
WAZNS_old_attia = set([u'عاءل',
         u'فوعل',
         u'علل',
         u'علول',
         u'ضطعل',
         u'فتال',
         u'عليل',
         u'عاعل',
         u'فعال',
         u'فعاءل',
         u'فاءل',
         u'ل',
         u'عالل',
         u'عال',
         u'فتعيل',
         u'فيعل',
         u'فال',
         u'عل',
         u'علالل',
         u'زدعل',
         u'ع',
         u'عايل',
         u'عاليل',
         u'فعوعل',
         u'فل',
         u'فتعل',
         u'عولل',
         u'فعلال',
         u'فوعال',
         u'عع',
         u'فع',
         u'عللول',
         u'فاع',
         u'عيل',
         u'فيل',
         u'فاعيل',
         u'فتعال',
         u'فاعول',
         u'فعاع',
         u'فول',
         u'فعل',
         u'فعيل',
         u'عول',
         u'فطعل',
         u'فعول',
         u'فيال',
         u'علال',
         u'فتل',
         u'فعلل',
         u'فاعل'])
         
         
WAZNS_SAWALHA = [u'فعل', 
u'فاعل', 
u'فتعل', 
u'فعلل', 
u'فعوعل', 
u'فعول', 
u'فعالل', 
u'فعال', 
u'فعللل', 
u'فوعل', 
u'فعولل', 
u'فاعول', 
u'فعيلال', 
u'فعلعل', 
u'فعيل', 
u'فيعل', 
u'فاعيل', 
u'فعاويل', 
u'فعاييل', 
u'فعاليل', 
u'فعلول', 
u'فعلعال', 
u'فعاعيل', 
u'فوعال', 
u'فعفعيل', 
u'فواعيل', 
u'فياعيل', 
u'فأعل', 
u'فعأل', 
u'فيعول', 
u'فاعال', 
u'فيعال', 
u'فوعلل', 
u'فواعل', 
u'فياعل', 
u'فعيعل', 
u'فعاعل', 
u'فعوال', 
u'فعيال', 
u'فعيول', 
u'فعاول', 
u'فعايل', 
u'فعائل', 
u'فعليل', 
u'فعيلل', 
u'فعلال', 
u'فعلالل', 
u'فعلاليل', 
u'فعللول', 
u'فعلليل', 
u'فيعلول', 
u'فعلويل', 
u'فعئل', 
u'فعفل', 
u'فتعئل', 
u'فعألل', 
u'فلعل', 
u'فول', 
u'فيل', 
u'فتعأل', 
u'فتعال', 
u'فعيعال', 
u'', 
u'عاييل', 
u'فال', 
u'عائل', 
u'فتع', 
u'فتأل', 
u'فياع', 
u'ل', 
u'فتال', 
u'فوع', 
u'فائل', 
u'عأل', 
u'فيع', 
u'عال', 
u'فأل', 
u'عاويل', 
u'فاول', 
u'عل', 
u'فواع', 
u'فايل', 
u'فاويل', 
u'فع', 
u'فيايل', 
u'عيول', 
u'عاول', 
u'فل', 
u'فوايل', 
u'عايل', 
u'عيال', 
u'فوال', 
u'فاع', 
u'فتئل', 
u'فأع', 
u'عئل', 
u'فاال', 
u'عيل', 
u'فئل', 
u'فاييل', 
u'عوال', 
u'عول', 
u'فيال', 
u'فيول', 
u'فتل']

WAZNS_SAWALHA_reviewed = [u'فعل', 
u'فاعل', 
u'فتعل', 
u'فطعل', 
u'فعلل', 
u'فعوعل', 
u'فعول', 
u'فعالل', 
u'فعال', 
#~ u'فعللل', 
u'فوعل', 
u'فعولل', 
u'فاعول', 
u'فعيلال', 
#~ u'فعلعل', 
u'فعيل', 
u'فيعل', 
u'فاعيل', 
u'فعاويل', 
u'فعاييل', 
u'فعاليل', 
u'فعلول', 
#~ u'فعلعال', 
u'فعاعيل', 
u'فوعال', 
#~ u'فعفعيل', 
u'فواعيل', 
u'فياعيل', 
#~ u'فأعل', 
#~ u'فعأل', 
u'فيعول', 
u'فاعال', 
u'فيعال', 
u'فوعلل', 
u'فواعل', 
u'فياعل', 
u'فعيعل', 
u'فعاعل', 
u'فعوال', 
u'فعيال', 
u'فعيول', 
u'فعاول', 
u'فعايل', 
u'فعائل', 
u'فعاءل', # normalized
u'فعليل', 
u'فعيلل', 
u'فعلال', 
#~ u'فعلالل', 
#~ u'فعلاليل', 
#~ u'فعللول', 
#~ u'فعلليل', 
u'فيعلول', 
u'فعلويل', 
#~ u'فعئل', 
#~ u'فعفل', 
#~ u'فتعئل', 
#~ u'فعألل', 
#~ u'فلعل', 
u'فول', 
u'فيل', 

#~ u'فتعأل', 
u'فتعال', 
u'فطعال', 
u'فعيعال', 
#~ u'', 
u'عاييل', 
u'فال', 
#~ u'عائل', 
u'فتع', 
u'فطع', 
#~ u'فتأل', 
u'فياع', 
#~ u'ل', 
u'فتال', 
u'فطال', 
u'فوع', 
u'فائل', 
#~ u'عأل', 
u'فيع', 
u'عال', 
#~ u'فأل', 
#~ u'عاويل', 
#~ u'فاول', 
u'عل', 
u'فواع', 
#~ u'فايل', 
#~ u'فاويل', 
u'فع', 
#~ u'فيايل', 
#~ u'عيول', 
#~ u'عاول', 
u'فل', 
#~ u'فوايل', 
#~ u'عايل', 
#~ u'عيال', 
#~ u'فوال', 
u'فاع', 
#~ u'فتئل', 
#~ u'فأع', 
#~ u'عئل', 
#~ u'فاال', 
#~ u'عيل', 
#~ u'فئل', 
#~ u'فاييل', 
#~ u'عوال', 
#~ u'عول', 
#~ u'فيال', 
#~ u'فيول', 
u'فتل', 
u'فطل',
u'فاءل',# normalized
]

WAZNS_old = set([u'فواعل',
 u'فياعل',
 u'فلال',
 u'فعاليل',
 u'فوعل',
 u'فوعلال',
 u'فلاعل',
 u'فعولل',
 u'عال',
 u'فعع',
 u'فتع',
 u'فعال',
 u'فعليل',
 u'فائل',
 u'ل',
 u'فوع',
 u'فيع',
 u'فواعيل',
 u'فيعل',
 u'فعالل',
 u'فال',
 u'عل',
 u'فواع',
 u'فعللول',
 u'فعايل',
 u'فلعليل',
 u'فيلعلال',
 u'فع',
 u'فعوعل',
 u'فيعال',
 u'فلعل',
 u'فل',
 u'فتعل',
 u'فعلال',
 u'ع',
 u'فلل',
 u'فعلول',
 u'فاع',
 u'فاعول',
 u'فطعل',
 u'فيل',
 u'فاعيل',
 u'فتعال',
 u'عيل',
 u'فعاع',
 u'فول',
 u'فعاعل',
 u'فعل',
 u'فعيل',
 u'فعلالل',
 u'فعول',
 u'فيال',
 u'فعائل',
 u'فتال',
 u'فتل',
 u'فعلل',
 u'فاعل'])

WAZNS = set([#u'ع',
 u'عال',
 u'عل',
 u'فائل',
 u'فاءل',
 u'فاع',
 u'فاعل',
 u'فاعول',
 u'فاعيل',
 u'فال',
 u'فتع',
 u'فتعال',
 u'فتعل',
 u'فتل',
 u'فع',
 u'فعائل',
 u'فعاءل', # normalized
 u'فعاع',
 u'فعاعل',
 u'فعال',
 u'فعالل',
 u'فعاليل',
 u'فعايل',
 u'فعع',
 u'فعل',
 u'فعلال',
 u'فعلل',
 #~ u'فعللول',
 u'فعلول',
 u'فعليل',
 u'فعوع',
 u'فعوعل',
 u'فعول',
 u'فعيل',
 u'فل',
# u'فلاعل',
 u'فلال',
 u'فلل',
 u'فواع',
 u'فواعل',
 u'فواعيل',
 u'فوعل',
#u'فوعلال',
 u'فول',
 u'فياعل',
 u'فيال',
 u'فيع',
 u'فيعل',
 u'فيل',
 #~ u'ل'
 
 # added manually
 u'فعاعيل',
 ])

#~ WAZNS = list(WAZNS_old) + list(WAZNS_old_attia)
#~ WAZNS = list(WAZNS_old) + list(WAZNS_SAWALHA)
#~ WAZNS = list(WAZNS_old_attia) + list(WAZNS_SAWALHA)
#~ WAZNS = list(WAZNS_old) + list(WAZNS_old_attia) + list(WAZNS_SAWALHA)
#~ WAZNS = WAZNS_SAWALHA
WAZNS = WAZNS_SAWALHA_reviewed
WAZNS = set(WAZNS)
class rhyzomeRooter(abstractRooter):
    def __init__(self,):
        abstractRooter.__init__(self)
    @staticmethod
    def waznlike2(word1, wazn, extract_root = False):
        u"""If the  word1 is like a wazn (pattern),
        the letters must be equal,
        the wazn has FEH, AIN, LAM letters.
        this are as generic letters.
        The two words can be full vocalized, or partial vocalized

        Example:
            >>> word1 = u"ضارب"
            >>> wazn = u"فَاعِل"
            >>> araby.waznlike(word1, wazn)
            True

        @param word1: input word
        @type word1: unicode
        @param wazn: given word template  وزن
        @type wazn: unicode
        @param extract_root: return the root
        @type extract_root: unicode
        @return: if two words have similar vocalization
        @rtype: Boolean
        """
        stack1 = stack.Stack(word1)
        stack2 = stack.Stack(wazn)
        root = stack.Stack()
        last1 = stack1.pop()
        last2 = stack2.pop()
        vowels = HARAKAT
        already_ain = False # used for double ain wazns
        # if an Ain is already given, the new ain must have the same letter
        while last1 != None and last2 != None:
            if last1 == last2 and last2 not in (FEH, AIN, LAM):
                last1 = stack1.pop()
                last2 = stack2.pop()
            elif last1 not in vowels and last2 in (FEH, LAM):
                
                root.push(last1)
                last1 = stack1.pop()
                last2 = stack2.pop()
            elif last1 not in vowels and last2 == AIN and not already_ain :
                # keep the found letter
                already_ain = last1
                root.push(last1)
                last1 = stack1.pop()
                last2 = stack2.pop()
            elif last1 not in vowels and last2 == AIN and  already_ain and last1 == already_ain:
                # keep the found letter
                # the second ain is not added to root
                last1 = stack1.pop()
                last2 = stack2.pop()
            #~ else:
                #~ # test if the AIN is equal to previous
                #~ if already_ain == last1:
                    #~ root.push(last1)
                    #~ last1 = stack1.pop()
                    #~ last2 = stack2.pop()
                #~ else:
                    #~ break
            elif last1 in vowels and last2 not in vowels:
                last1 = stack1.pop()
            elif last1 not in vowels and last2 in vowels:
                last2 = stack2.pop()
            else:
                break
        # reverse the root letters
        root.items.reverse()
        #~ print " the root is ", root.items#"".join(root.items)
        if not (stack1.is_empty() and stack2.is_empty()):
            return False
        # if one letter is remind after pop in one stack
        elif last1 != None or last2 != None:
            return False
        else:
            #~ print (u"word '%s' , wazn ='%s'"%(u"".join(stack1.items),u"".join(stack2.items))).encode('utf8') 
            if extract_root:
                return "".join(root.items)
            else:
                return True

    #~ def valid_starstem(self, starword):
    def extract(self, starword, prefix, suffix):
        """ validate starwoord agnaist Schemes أوزان"""
        accepted_roots = []
        for wazn in WAZNS:
            #~ if araby.waznlike(starword,wazn):
            if len(wazn) == len(starword):
                root = self.waznlike2(starword, wazn, extract_root = True)
                if root:
                    # the root is added only if the wazn is not weak
                    # the ALEF is not a valid root
                    add_root = not self.is_weak(wazn) and araby.ALEF not in root
                    if add_root:
                        accepted_roots.append(root)
                        #~ accepted_roots.append(root)
                    # extend roots to add removed letters according to wazn              
                    extended = self.extend_root(root, wazn, prefix, suffix)
                    accepted_roots.extend(extended)
                    if self.debug:
                        add_root = 'add' if add_root else 'remove'
                        print((u'rhyzome-rooter.extarct: word [%s-%s-%s]\t wz %s\trt [%s, %s] :ext %s'%(prefix, starword, suffix, wazn,root, add_root, u', '.join(extended))).encode('utf8'))
        return accepted_roots

    @staticmethod
    def is_weak(wazn):
        """ if the wazn is weak """
        if araby.FEH not in wazn:
            return True
        if araby.AIN not in wazn:
            return True
        if araby.LAM not in wazn:
            return True
        return False

    def extend_root(self, psudoroot, wazn, prefix, suffix):
        """ extend a psudo root"""
        extended = []
        removal_end = self.is_removal_end(prefix, suffix)
        removal_begin = self.is_removal_begin(prefix, suffix)
        removal_middle = self.is_removal_middle(prefix, suffix)

        if psudoroot in (u'خذ',u'مر',u'كل'):
            extended.append(araby.HAMZA + psudoroot)
        #قائل سائر
        if len(psudoroot) == 3  and psudoroot[1] ==araby.HAMZA:
            extended.append(psudoroot[0]+araby.WAW +psudoroot[2])
            extended.append(psudoroot[0]+araby.YEH +psudoroot[2])

        # convert ALEF to WAW or YEH
        if araby.ALEF in psudoroot:
            extended.append(psudoroot.replace(araby.ALEF, araby.WAW))
            extended.append(psudoroot.replace(araby.ALEF, araby.YEH))
        if araby.YEH in psudoroot:
            extended.append(psudoroot.replace(araby.YEH, araby.WAW, 1))
            #~ extended.append(psudoroot.replace(araby.YEH, araby.WAW, -1))
        if araby.WAW in psudoroot:
            extended.append(psudoroot.replace(araby.WAW, araby.YEH, 1))
            #~ extended.append(psudoroot.replace(araby.WAW, araby.YEH, -1))

        # given roots are
        if removal_begin and araby.FEH not in wazn:
            # add FEH
            # possible YEH, WAW
            # add Yeh or waw at begin
            extended.append(araby.WAW + psudoroot)
            #~ extended.append(araby.HAMZA + psudoroot)
            #~ extended.append(araby.YEH + psudoroot)
            
        if removal_middle  and araby.AIN not in wazn:
            #add AIN
            # possible َAdjwaf
            # add Yeh or waw at middle
            extended.append("".join([psudoroot[0],araby.WAW, psudoroot[1:]]))
            extended.append("".join([psudoroot[0],araby.YEH, psudoroot[1:]]))

        if removal_end and araby.LAM not in wazn:
            #add LAM
            # possible double مضعف
            # possible maqsur
            # add Yeh or waw at end
            extended.append(psudoroot+araby.WAW)
            extended.append(psudoroot+araby.YEH)
        if araby.LAM not in wazn:
            # add double letter جد =>جدد
            extended.append(psudoroot + psudoroot[-1:])

        return extended

    @staticmethod
    def is_removal_begin(prefix, suffix):
        """ return true if prefix can generate weak letter root remove
        for example Yeh can be removal prefix it can remove the first letter or modify the midle one
        """
        #~ return True

        last = prefix[-1:]
        # The prefix ends with Yeh, Alef_Hamza, TEH, Noon
        if last in (araby.YEH, araby.NOON, araby.ALEF_HAMZA_ABOVE):
            return True
        if last in (araby.TEH) and not prefix[-3:] in (u"يست", u"نست", u"تست", u"است", ):
            return True
        if suffix.endswith(araby.TEH_MARBUTA):
            return True
        return False
    @staticmethod        
    def is_removal_middle(prefix, suffix):
        """ return true if prefix can generate weak letter root remove
        for example Yeh can be removal prefix it can remove the first letter or modify the midle one
        """
        #~ return True
        last = prefix[-1:]
        first = suffix[:1]
        # The prefix ends with Yeh, Alef_Hamza, TEH, Noon
        if not prefix:
            return True
        if not suffix:
            return True
        # The prefix ends with Yeh, Alef_Hamza, TEH, Noon
        if last in (araby.YEH, araby.NOON, araby.ALEF_HAMZA_ABOVE):
            return True
        if last in (araby.TEH) and not prefix[-3:] in (u"يست", u"نست", u"تست", u"است", ):
            return True
        if first in (araby.TEH, araby.NOON, ):
            return True            
        return False
    @staticmethod
    def is_removal_end(prefix, suffix):
        """ return true if suffix can generate weak letter root remove
        for example Yeh can be removal prefix it can remove the first letter or modify the midle one
        """
        #~ return True

        first = suffix[:1]
        if first in (araby.TEH, araby.YEH, ):
            return True
        last = prefix[-1:]
        # The prefix ends with Yeh, Alef_Hamza, TEH, Noon
        if last in (araby.TEH, araby.YEH, araby.NOON, araby.ALEF_HAMZA_ABOVE):
            return True            
        return True
