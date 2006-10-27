# -*- coding: utf-8 -*-

""" Parsers
"""

__version__ = 0.1

###
#Czechtile: WikiHezkyCesky
#Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
#
#This library is free software; you can redistribute it and/or
#modify it under the terms of the GNU Lesser General Public
#License as published by the Free Software Foundation; either
#version 2.1 of the License, or (at your option) any later version.
#
#This library is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#Lesser General Public License for more details.
#
#You should have received a copy of the GNU Lesser General Public
#License along with this library; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
###

import re

from sneakylang import Parser, ParserRollback
import macros

class Document(Parser):
    start = None
    macro = macros.Document

    def __init__(self, documentType, *args, **kwargs):
        self.parser = documentType
        Parser.__init__(self, *args, **kwargs)

    def resolveContent(self):
        self.content = self.stream
        self.stream = ''

    def callMacro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.registerMap).expand(self.content, self.parser)

class Book(Parser):
    start = None
    macro = macros.Book
    end = ''

    def resolveContent(self):
        self.content = self.stream
        self.stream = ''
        self.args = self.content

class Article(Parser):
    start = None
    macro = macros.Article

    def resolveContent(self):
        self.content = self.stream
        self.stream = ''
        self.args = self.content

class Sekce(Document):
    start = None
    macro = macros.Sekce

class Odstavec(Parser):
    start = ['^(\n){2}$']
    end = '(\n){2}'
    macro = macros.Odstavec

    def resolveContent(self):
        end = re.search(self.__class__.end, self.stream)
        if end:
            self.args = self.content = self.stream[0:end.start()]
            self.chunk_end = self.stream[end.start():end.end()]
            # we're not eating trailing \ns
            self.stream = self.stream[end.start():]
        else:
            #FIXME: now that is problem
            # either paragraph is until end of document
            # or it was badly resolved
            # invent some algorythm on this...
            raise ParserRollback

class Silne(Parser):
    start = ['^("){3}$']
    end = ['^("){3}$']
    macro = macros.Silne

class Zvyraznene(Parser):
    start = ['^("){2}$']
    end = ['^("){2}$']
    macro = macros.Zvyraznene

class Nadpis(Parser):
    start = ['^(\n)?(=){1,5}(\ ){1}$']
    #end same as start match
    macro = macros.Nadpis

    def resolveContent(self):
        endPattern = self.chunk[:-1]
        if endPattern.startswith('\n'):
            endPattern = endPattern[1:]
        # chunk is \n={n}[whitespace],
        # end is [whitespace]={n}\n
        endMatch = re.search(''.join([' ', endPattern, '\n']), self.stream)
        if not endMatch:
            raise ParserRollback
        self.level = len(endPattern)
        self.content = self.stream[0:endMatch.start()]
        # end()-1 because we won't eat trailing newline
        self.chunk_end = self.stream[endMatch.start():endMatch.end()-1]
        self.stream = self.stream[endMatch.end()-1:]

    def callMacro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.registerMap).expand(self.level, self.content)
