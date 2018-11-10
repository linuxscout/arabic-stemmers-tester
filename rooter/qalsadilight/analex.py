#!/usr/bin/python
# -*- coding=utf-8 -*-
#-----------------------------------------------------------------------
# Name:        analex
# Purpose:     Arabic lexical analyser, provides feature to stem arabic
# words as noun, verb, stopword
#
# Author:      Taha Zerrouki (taha.zerrouki[at]gmail.com)
#
# Created:     31-10-2011
# Copyright:   (c) Taha Zerrouki 2011
# Licence:     GPL
#-----------------------------------------------------------------------
"""
    Arabic text morphological analyzer.
    Provides routins  to alanyze text.
    Can treat text as verbs or as nouns.
"""

if __name__ == "__main__":
    import sys
    sys.path.append('..')

import re
import pyarabic.araby as araby  # basic arabic text functions

#~ import arramooz.wordfreqdictionaryclass as wordfreqdictionaryclass
import naftawayh.wordtag  # word tagger
import analex_const  # special constant for analex
import stem_noun  # noun stemming
import stem_verb  # verb stemming
#~ import stem_unknown  # unknown word stemming
import stem_stop as stem_stopwords  # stopwords word stemming
import stem_pounct_const  # pounctaution constants
import disambig  # disambiguation const
import wordcase
#~ import stemmedword  # the result object for stemming
import cache

class Analex:
    """
        Arabic text morphological analyzer.
        Provides routins  to alanyze text.
        Can treat text as verbs or as nouns.
    """

    def __init__(self, cache_path=False ,allow_tag_guessing=True, allow_disambiguation=True):
        """
        Create Analex instance.
        """

        self.nounstemmer = stem_noun.NounStemmer()  # to stem nouns
        self.verbstemmer = stem_verb.VerbStemmer()  # to stem verbs
        #~ self.unknownstemmer = stem_unknown.UnknownStemmer()
        # to stem unknown
        self.stopwordsstemmer = stem_stopwords.StopWordStemmer()
        # to stem stopwords

        self.allow_tag_guessing = allow_tag_guessing
        # allow gueesing tags by naftawayh before analyis
        # if taggin is disabled, the disambiguation is also disabled
        self.allow_disambiguation = allow_disambiguation and allow_tag_guessing
        # allow disambiguation before analyis
        # enable the last mark (Harakat Al-I3rab)
        self.allow_syntax_lastmark = True
        if self.allow_tag_guessing:
            self.tagger = naftawayh.wordtag.WordTagger()
        if self.allow_disambiguation:
            self.disambiguator = disambig.Disambiguator()
        self.debug = False  # to allow to print internal data
        self.limit = 10000  # limit words in the text
        self.wordcounter = 0
        # the words contain arabic letters and harakat.
        # the unicode considers arabic harakats as marks not letters,
        # then we add harakat to the regluar expression to tokenize
        marks = u"".join(araby.TASHKEEL)
        # contains [FATHA, DAMMA, KASRA, SUKUN, DAMMATAN, KASRATAN,
        #  FATHATAN, SHADDA])
        # used to tokenize arabic text
        #decprecated, we use araby.tokenize
        #~ self.token_pat = re.compile(ur"([\w%s]+)" % marks, re.UNICODE)
        #used to split text into clauses
        self.clause_pattern = re.compile(
            "([\w%s\s]+)" % (u"".join(araby.TASHKEEL), ), re.UNICODE)

        # allow partial vocalization support,
        #~The text is analyzed as partial or fully vocalized.
        self.partial_vocalization_support = True

        #word frequency dictionary
        #~ self.wordfreq = wordfreqdictionaryclass.WordFreqDictionary(
            #~ 'wordfreq', wordfreqdictionaryclass.WORDFREQ_DICTIONARY_INDEX)

        # added to avoid duplicated search in the word frequency database
        # used as cache to reduce database access
        #added as a global variable to avoid duplucated search
        #in mutliple call of analex
        # cache used to avoid duplicata
        self.allow_cache_use = True
        #~ self.allow_cache_use = False
        self.cache = cache.Cache(cache_path)
        
        # In case of training and vocalized text analysis, 
        # we propose to respect Shadda in the given word
        self.fully_vocalized_input = False

    def __del__(self):
        """
        Delete instance and clear cache
        """
        self.wordfreq = None
        self.nounstemmer = None
        self.verbstemmer = None
        #~ self.unknownstemmer = None
        self.stopwordsstemmer = None
        self.tagger = None
        self.disambiguator = None
    def count_word(self, ):
        """ count input words. Used just for profiling and tests.
        @return: counter.
        @rtype: integer.
        """
        self.wordcounter += 1
        return self.wordcounter

    def tokenize(self, text=u""):
        """
        Tokenize text into words
        @param text: the input text.
        @type text: unicode.
        @return: list of words.
        @rtype: list.
        """
        return araby.tokenize(text)

    def split_into_phrases(self, text):
        """
        Split Text into clauses
        @param text: input text
        @type text: unicode
        @return: list of clauses
        @rtype: list of unicode
        """
        if text:
            list_phrase = self.clause_pattern.split(text)
            if list_phrase:
                j = -1
                newlist = []
                for phr in list_phrase:
                    if not self.clause_pattern.match(phr):
                        #is pounctuation or symboles
                        #print 'not match', ph.encode('utf8')
                        if j < 0:
                            # the symbols are in the begining
                            newlist.append(phr)
                            j = 0
                        else:
                            # the symbols are after a phrases
                            newlist[j] += phr
                    else:
                        newlist.append(phr)
                        j += 1
                return newlist
            else:
                return []
        return []

    def text_tokenize(self, text):
        """
        Tokenize text into words, after treatement.
        @param text: the input text.
        @type text: unicode.
        @return: list of words.
        @rtype: list.
        """
        #~text = self.text_treat(text)
        list_word = self.tokenize(text)
        #print "text_tokenize", u" ".join(list_word).encode('utf8')
        return list_word

    def set_debug(self, debug):
        """
        Set the debug attribute to allow printing internal analysis results.
        @param debug: the debug value.
        @type debug: True/False.
        """
        self.debug = debug
        self.nounstemmer.set_debug(debug)  # to set debug on noun stemming
        self.verbstemmer.set_debug(debug)  # to set debug on verb stemming

    def enable_syntax_lastmark(self):
        """
        Enable the syntaxic last mark attribute to allow use of I'rab harakat.
        """
        self.allow_syntax_lastmark = True
        self.nounstemmer.enable_syntax_lastmark()
        # to allow syntax last mark on noun stemming
        self.verbstemmer.enable_syntax_lastmark()
        # to allow syntax last mark  on verb stemming
        
    def enable_fully_vocalized_input(self):
        """
        Enable fully vocalized  input in case of vocalized text analysis.
        """
        self.fully_vocalized_input = True

    def disable_syntax_lastmark(self):
        """
        Disable the syntaxic last mark attribute to allow use of I'rab harakat.
        """
        self.allow_syntax_lastmark = False
        self.nounstemmer.disable_syntax_lastmark()
        # to allow syntax last mark on noun stemming
        self.verbstemmer.disable_syntax_lastmark()
        # to allow syntax last mark  on verb stemming

    def set_limit(self, limit):
        """
        Set the number of word treated in text.
        @param limit: the word number limit.
        @type limit: integer.
        """
        self.limit = limit

    def enable_allow_cache_use(self):
        """
        Allow the analex to use Cache to reduce calcul.
        """
        self.allow_cache_use = True

    def disable_allow_cache_use(self):
        """
        Not allow the analex to use Cache to reduce calcul.
        """
        self.allow_cache_use = False

    def check_text(self, text, mode='all'):
        """
        Analyze text morphologically.
        @param text: the input text.
        @type text: unicode.
        @param mode: the mode of analysis as 'verbs', 'nouns', or 'all'.
        @type mode: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        #print "ok", text.encode('utf8')
        list_word = self.text_tokenize(text)
        #print "ok", u"\t".join(list_word).encode('utf8')
        if self.allow_tag_guessing:
            list_guessed_tag = self.tagger.word_tagging(list_word)
            # avoid errors
            if len(list_guessed_tag) != len(list_word):
                #if the two lists have'nt the same length,
                # we construct a empty list for tags with the same length
                # print "error on guess tags"
                # sys.exit()
                list_guessed_tag = ['nv'] * len(list_word)
        # disambiguate  some words to speed up the analysis
        if self.allow_disambiguation:
            newwordlist = self.disambiguator.disambiguate_words(
                list_word, list_guessed_tag)
            # avoid the incomplete list
            if len(newwordlist) == len(list_word):
                list_word = newwordlist
                # print u" ".join(list_word).encode('utf8')
                # print u" ".join(list_guessed_tag).encode('utf8')

        #~ resulted_text = u""
        resulted_data = []

        #checkedWords = {} #global
        if mode == 'all':

            for i in range(len(list_word[:self.limit])):
                word = list_word[i]
                self.count_word(
                )  # a ghost function to count words check function calls
                guessedtag = list_guessed_tag[i]
                one_data_list = self.check_word(word, guessedtag)
                #~ stemmed_one_data_list = [
                    #~ stemmedword.StemmedWord(w) for w in one_data_list
                #~ ]
                #~ resulted_data.append(stemmed_one_data_list)
                resulted_data.append(one_data_list)
        elif mode == 'nouns':

            for word in list_word[:self.limit]:
                one_data_list = self.check_word_as_noun(word)
                #~ stemmed_one_data_list = [stemmedword.StemmedWord(w) \
                #~ for w in one_data_list]
                #~ resulted_data.append(stemmed_one_data_list)
                resulted_data.append(one_data_list)
        elif mode == 'verbs':
            for word in list_word[:self.limit]:
                one_data_list = self.check_word_as_verb(word)
                #~ stemmed_one_data_list = [stemmedword.StemmedWord(w) \
                #~ for w in one_data_list]
                #~ resulted_data.append(stemmed_one_data_list)
                resulted_data.append(one_data_list)
        return resulted_data

    def check_word(self, word, guessedtag=""):
        """
        Analyze one word morphologically as verbs
        @param word: the input word.
        @type word: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """

        word = araby.strip_tatweel(word)
        word_vocalised = word
        word_nm = araby.strip_tashkeel(word)
        # get analysed details from cache if used
        if self.allow_cache_use and self.cache.is_already_checked(word_nm):
            #~ print (u"'%s'"%word).encode('utf8'), 'found'
            resulted_data = self.cache.get_checked(word_nm)
        else:
            resulted_data = []
            # if word is a pounctuation
            resulted_data += self.check_word_as_pounct(word_nm)
            # Done: if the word is a stop word we have  some problems,
            # the stop word can also be another normal word (verb or noun),
            # we must consider it in future works
            # if word is stopword allow stop words analysis
            resulted_data += self.check_word_as_stopword(word_nm)

            #if word is verb
            # مشكلة بعض الكلمات المستبعدة تعتبر أفعلا أو اسماء
            #~if  self.tagger.has_verb_tag(guessedtag) or \
            #~self.tagger.is_stopword_tag(guessedtag):
            #~resulted_data += self.check_word_as_verb(word_nm)
            resulted_data += self.check_word_as_verb(word_nm)
            #print "is verb", rabti, len(resulted_data)
            #if word is noun
            #~if self.tagger.has_noun_tag(guessedtag) or \
            #~self.tagger.is_stopword_tag(guessedtag):
            #~resulted_data += self.check_word_as_noun(word_nm)
            resulted_data += self.check_word_as_noun(word_nm)
            #~ if len(resulted_data) == 0:
                #~ #print (u"1 _unknown %s-%s"%(word, word_nm)).encode('utf8')
                #~ #check the word as unkonwn
                #~ resulted_data += self.check_word_as_unknown(word_nm)
                #~ #check if the word is nomralized and solution are equivalent
            resulted_data = self.check_normalized(word_vocalised, resulted_data)
            #check if the word is shadda like
            
            resulted_data = self.check_shadda(word_vocalised, resulted_data, self.fully_vocalized_input)

            # add word frequency information in tags
            #~ resulted_data = self.add_word_frequency(resulted_data)

            # add the stemmed words details into Cache
            data_list_to_serialize = [w.__dict__ for w in resulted_data]
            if self.allow_cache_use:
                self.cache.add_checked(word_nm, data_list_to_serialize)

        #check if the word is vocalized like results
        if self.partial_vocalization_support:
            resulted_data = self.check_partial_vocalized(word_vocalised,
                                                    resulted_data)

        if len(resulted_data) == 0:
            resulted_data.append(
                wordcase.WordCase({
                    'word':
                    word,
                    'affix': ('', '', '', ''),
                    'stem':
                    word,
                    'original':
                    word,
                    'vocalized':
                    word,
                    'semivocalized':
                    word,
                    'tags':
                    u'',
                    'type':
                    'unknown',
                    'root':
                    '',
                    'template':
                    '',
                    #~ 'freq':
                    #~ self.wordfreq.get_freq(word, 'unknown'),
                    'syntax':
                    '',
                }))
        return resulted_data

    def check_text_as_nouns(self, text):
        """
        Analyze text morphologically as nouns
        @param text: the input text.
        @type text: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        return self.check_text(text, "nouns")

    def check_text_as_verbs(self, text):
        """
        Analyze text morphologically as verbs
        @param text: the input text.
        @type text: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        return self.check_text(text, "verbs")


    def check_word_as_stopword(self, word):
        """
        Check if the word is a stopword,
        @param word: the input word.
        @type word: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        return self.stopwordsstemmer.stemming_stopword(word)

    def check_word_as_pounct(self, word):
        """
        Check if the word is a pounctuation,
        @param word: the input word.
        @type word: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        detailed_result = []
        if not word:
            return detailed_result
        # ToDo : fix it to isdigit, by moatz saad
        if word.isnumeric():
            detailed_result.append(
                wordcase.WordCase({
                    'word': word,
                    'affix': ('', '', '', ''),
                    'stem': '',
                    'original': word,
                    'vocalized': word,
                    'tags': u"عدد",
                    'type': 'NUMBER',
                    #~ 'freq': 0,
                    'syntax': '',
                    'root':'',
                }))
        # test if all chars in word are punctuation
        for char in word:
            # if one char is not a pounct, break
            if char not in stem_pounct_const.POUNCTUATION:
                break
        else:
            # if all chars are pounct, the word take tags of the first char
            detailed_result.append(
                wordcase.WordCase({
                    'word':
                    word,
                    'affix': ('', '', '', ''),
                    'stem':
                    '',
                    'original':
                    word,
                    'vocalized':
                    word,
                    'tags':
                    stem_pounct_const.POUNCTUATION[word[0]]['tags'],
                    'type':
                    'POUNCT',
                    #~ 'freq':
                    #~ 0,
                    'syntax':
                    '',
                    'root':'',
                }))

        return detailed_result

    def check_word_as_verb(self, verb):
        """
        Analyze the word as verb.
        @param verb: the input word.
        @type verb: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        return self.verbstemmer.stemming_verb(verb)

    def check_word_as_noun(self, noun):
        """
        Analyze the word as noun.
        @param noun: the input word.
        @type noun: unicode.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        return self.nounstemmer.stemming_noun(noun)

    #~ def check_word_as_unknown(self, noun):
        #~ """
        #~ Analyze the word as unknown.
        #~ @param noun: the input word.
        #~ @type noun: unicode.
        #~ @return: list of dictionaries of analyzed words with tags.
        #~ @rtype: list.
        #~ """
        #~ return self.unknownstemmer.stemming_noun(noun)

    @staticmethod
    def check_shadda(word_vocalised, resulted_data, fully_vocalized_input=False):
        """
        if the entred word is like the found word in dictionary,
        to treat some normalized cases,
        the analyzer return the vocalized like words.
        This function treat the Shadda case.
        @param word_vocalised: the input word.
        @type word_vocalised: unicode.
        @param resulted_data: the founded resulat from dictionary.
        @type resulted_data: list of dict.
        @param fully_vocalized_input: if the two words must resect the shadda and vocalized.
        @type fully_vocalized_input: Boolean, default is False.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        #~return filter(lambda item: araby.shaddalike(word_vocalised,
        #~item.__dict__.get('vocalized', '')), resulted_data)
        #~x for x in [1, 1, 2] if x == 1
        #~ return [
        #~ x for x in resulted_data
        #~ if araby.shaddalike(word_vocalised, x.__dict__.get('vocalized', '')) ]
        if fully_vocalized_input:
            return [x for x in resulted_data if araby.strip_harakat(word_vocalised) == 
        araby.strip_harakat(x.__dict__.get('vocalized', ''))]
        else:
            return [
            x for x in resulted_data
            if araby.shaddalike(word_vocalised, x.__dict__.get('vocalized', ''))
        ]
        

    @staticmethod
    def check_normalized(word_vocalised, resulted_data):
        """
        If the entred word is like the found word in dictionary,
        to treat some normalized cases,
        the analyzer return the vocalized like words
        ُIf the word is ذئب, the normalized form is ذءب,
        which can give from dictionary ذئبـ ذؤب.
        this function filter normalized resulted word according
        the given word, and give ذئب.
        @param word_vocalised: the input word.
        @type word_vocalised: unicode.
        @param resulted_data: the founded resulat from dictionary.
        @type resulted_data: list of dict.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        #print word_vocalised.encode('utf8')
        filtred_data = []
        inputword = araby.strip_tashkeel(word_vocalised)
        for item in resulted_data:
            if 'vocalized' in item.__dict__:  #.has_key('vocalized') :
                #~ if 'vocalized' in item :
                #~ outputword = araby.strip_tashkeel(item['vocalized'])
                outputword = araby.strip_tashkeel(item.__dict__['vocalized'])
                #~ print u'\t'.join([inputword, outputword]).encode('utf8')
                if inputword == outputword:
                    #item['tags'] += ':a'
                    filtred_data.append(item)
                #~ filtred_data.append(item)
        return filtred_data

    @staticmethod
    def check_partial_vocalized(word_vocalised, resulted_data):
        """
        if the entred word is vocalized fully or partially,
        the analyzer return the vocalized like words
        This function treat the partial vocalized case.
        @param word_vocalised: the input word.
        @type word_vocalised: unicode.
        @param resulted_data: the founded resulat from dictionary.
        @type resulted_data: list of dict.
        @return: list of dictionaries of analyzed words with tags.
        @rtype: list.
        """
        filtred_data = []
        if not araby.is_vocalized(word_vocalised):
            return resulted_data
        else:
            #compare the vocalized output with the vocalized input
            #print ' is vocalized'
            for item in resulted_data:
                if 'vocalized' in item and araby.vocalizedlike(
                        word_vocalised, item['vocalized']):
                    item['tags'] += ':' + analex_const.PARTIAL_VOCALIZED_TAG
                    filtred_data.append(item)
        return filtred_data