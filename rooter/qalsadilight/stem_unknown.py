#!/usr/bin/python
# -*- coding=utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        stem_unknown
# Purpose:     Arabic lexical analyser, provides feature for
#  stemming arabic word as unknown word
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-------------------------------------------------------------------------------
"""
    Arabic unknown word stemmer.
    Unkown words are stemmed as nouns with another dictionary
"""
import wordcase


class UnknownStemmer:
    """
        Arabic unknown word stemmer.
        Unkown words are stemmed as nouns with another dictionary
    """

    def __init__(self, debug=False):
        self.debug = debug

    def stemming_noun(self, noun):
        """
        Analyze word morphologically as noun
        @param noun: the input noun.
        @type noun: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        detailed_result = []
        detailed_result.append(wordcase.WordCase({
                    'word':noun,
                    'affix': "",
                    'stem':noun,
                    'original':noun, #original,
                    'type':u'unkonwn',
                    'original':noun,
                }))

        return detailed_result
