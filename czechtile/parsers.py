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


### "Global content" holders ###

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

### End of "global content" hodlers ###

### "Block" elements, which should be top-level ###

class Odstavec(Parser):
    start = None
    end = None
    macro = macros.Odstavec

    def resolveContent(self):
        """ Odstavec parser is called only and only on unbound TextNodes; thus,
        all content of TextNode is Paragraph
        """
        self.content = self.stream
        self.stream = ''
        self.args = self.content

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

### End of "block" elements ###

### Inline elements, mostly in Paragraphs ####

class Silne(Parser):
    start = ['^("){3}$']
    end = '^("){3}$'
    macro = macros.Silne

    def resolveContent(self):
        endMatch = re.search(self.__class__.end[1:-1], self.stream)
        if not endMatch:
            raise ParserRollback
        self.content = self.stream[0:endMatch.start()]
        self.chunk_end = self.stream[endMatch.start():endMatch.end()]
        self.stream = self.stream[endMatch.end():]

    def callMacro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.registerMap).expand(self.content)

class Zvyraznene(Parser):
    start = ['^("){2}$']
    end = '^("){2}$'
    macro = macros.Zvyraznene

    def resolveContent(self):
        endMatch = re.search(self.__class__.end[1:-1], self.stream)
        if not endMatch:
            raise ParserRollback
        self.content = self.stream[0:endMatch.start()]
        self.chunk_end = self.stream[endMatch.start():endMatch.end()]
        self.stream = self.stream[endMatch.end():]

    def callMacro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.registerMap).expand(self.content)

class Hyperlink(Parser):
    start = ['^http:\/\/\w+([-_\.]?\w)*\.[a-zA-Z]{2,4}(\/{1}[-_~&=\?\.a-z0-9]*)*$', '^\(http:\/\/\w+([-_\.]?\w)*\.[a-zA-Z]{2,4}(\/{1}[-_~&=\?\.a-z0-9]*)*$']
    end = '^(\))$'
    macro = macros.Hyperlink

    def resolveContent(self):
        if not self.chunk.startswith('('):
            # Easy substitution of http://link
            self.link = self.chunk
            self.content = self.chunk
        else:
            # Substitution with arguments, (http://link link text)
            endMatch = re.search(self.__class__.end[1:-1], self.stream)
            if not endMatch:
                raise ParserRollback
            self.link = self.chunk[1:]
            self.content = re.sub("^(\s)*", '', self.stream[0:endMatch.start()])
            self.chunk_end = self.stream[endMatch.start():endMatch.end()]
            self.stream = self.stream[endMatch.end():]

    def callMacro(self):
        """ Do proper call to related macro(s) """
        return self.macro(self.register, self.registerMap).expand(self.link, self.content)

### Typographic parsers - transfer text to czech typographic customs ###

class TriTecky(Parser):
    start = ['^(\.){3}$']
    end = None
    macro = macros.TriTecky

    def resolveContent(self):
        pass

    def callMacro(self):
        return self.macro(self.register, self.registerMap).expand()

### End of typographic parsers ###

### End of inline elements ###


class List(Parser):
    start = None
    end = None
    macro = macros.List

    def resolveContent(self):
        self.content = self.stream
        self.stream = ''
        self.args = self.content

class ListItem(Parser):
    start = ['^(\ -\ ){1}$']
    end = '^(\n)$'
    macro = macros.ListItem

    def resolveContent(self):
        # Almad: This is not true, because self.strem is contains REST of whole stream,
        # not only until newline (or generally, self.__class__.end, so you must identify it
        self.content = self.stream
# commented because of small problems with type_
#        if re.search(self.chunk, '^ - '):
#            self.type_ = 'itemized'

    def callMacro(self):
        """ Do proper call to related macro(s) """
        self.macro(self.register, self.registerMap).expand(self.content)
#        return self.macro(self.register, self.registerMap).expand(self.type_, self.content)
