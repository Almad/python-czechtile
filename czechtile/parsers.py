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

class Book(Parser):
    start = None
    macro = macros.Book
    end = ''

    def resolve_argument_string(self):
        self.content = self.stream
        self.stream = ''
        self.argument_string = self.content

class Article(Parser):
    start = None
    macro = macros.Article

    def resolve_argument_string(self):
        self.content = self.stream
        self.stream = ''
        self.argument_string = self.content

class Sekce(Parser):
    start = None
    macro = macros.Sekce

### End of "global content" hodlers ###

### "Block" elements, which should be top-level ###

class Odstavec(Parser):
    start = None
    end = None
    macro = macros.Odstavec

    def resolve_argument_string(self):
        """ Odstavec parser is called only and only on unbound TextNodes; thus,
        all content of TextNode is Paragraph
        """
        self.content = self.stream
        self.stream = ''
        self.argument_string = self.content

class NeformatovanyText(Parser):
    start = ['(\n§§\n){1}']
    end = '(\n§§\n){1}'
    macro = macros.NeformatovanyText

    def resolve_argument_string(self):
        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback

        self.argument_string = self.stream[0:endMatch.start()]
        self.stream = self.stream[endMatch.end():]

class Nadpis(Parser):
    start = ['(\n)?(=){1,5}(\ )?']
    #end same as start match
    macro = macros.Nadpis

    def resolve_argument_string(self):
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

        self.argument_string = ''.join([str(self.level), ' ', self.content])

### End of "block" elements ###

### Inline elements, mostly in Paragraphs ####

class Silne(Parser):
    start = ['("){3}']
    end = '("){3}'
    macro = macros.Silne

    def resolve_argument_string(self):
        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback
        self.argument_string = self.stream[0:endMatch.start()]
        self.chunk_end = self.stream[endMatch.start():endMatch.end()]
        self.stream = self.stream[endMatch.end():]

class Zvyraznene(Parser):
    start = ['("){2}']
    end = '("){2}'
    macro = macros.Zvyraznene

    def resolve_argument_string(self):
        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback
        self.argument_string = self.stream[0:endMatch.start()]
        self.chunk_end = self.stream[endMatch.start():endMatch.end()]
        self.stream = self.stream[endMatch.end():]

class Hyperlink(Parser):
    start = ['http:\/\/\w+([-_\.]?\w)*\.[a-zA-Z]{2,4}(\/{1}[-_~&=\?\.a-z0-9]*)*', '\(http:\/\/\w+([-_\.]?\w)*\.[a-zA-Z]{2,4}(\/{1}[-_~&=\?\.a-z0-9]*)*']
    end = '(\))'
    macro = macros.Hyperlink

    def resolve_argument_string(self):
        if not self.chunk.startswith('('):
            # Easy substitution of http://link
            self.link = self.chunk
            self.argument_string = ''.join([self.chunk, ' ', self.chunk])
        else:
            endMatch = re.search(self.__class__.end, self.stream)
            if not endMatch:
                raise ParserRollback
            self.link = self.chunk[1:]
            text = re.sub("^(\s)*", '', self.stream[0:endMatch.start()])
            # empty text, we should avoid this because of hyperlink in parenthesis,
            # see bug #39
            if text == '':
                raise ParserRollback
            self.argument_string = ''.join([self.link, ' ', text])

            self.chunk_end = self.stream[endMatch.start():endMatch.end()]
            self.stream = self.stream[endMatch.end():]

### Typographic parsers - transfer text to czech typographic customs ###

class TriTecky(Parser):
    start = ['(\.){3}']
    end = None
    macro = macros.TriTecky

    def resolve_argument_string(self):
        pass

    def call_macro(self):
        return self.macro(self.register, self.register_map).expand()

### End of typographic parsers ###

### End of inline elements ###

types = {
    ' - ' : 'itemized',
    ' 1. ' : '1-ordered',
    ' a. ' : 'A-ordered',
    ' i. ' : 'I-ordered'
}

class List(Parser):
    # the '\n\n' start and end is only for now, later it can be removed
    # (when it'll be all right)
    start = ['(\n\n\ ){1}(-|(a\.)|(i\.)|(1\.)){1}(\ ){1}']
    end = '(\n){2}'
    macro = macros.List

    def resolve_argument_string(self):

        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback
        self.content = self.chunk[2:] + self.stream[0:endMatch.start()]
        self.stream = self.stream[endMatch.end():]
        self.content = '\n' + self.content + '\n'

        for i in types.keys():
            if re.search(i, self.chunk[self.chunk.count(' ') - 2:]):
                self.type_ = types[i]

        self.argument_string = ''.join([self.type_, '!::', self.content])

class ListItem(Parser):
    start = ['(\n){1}(\ )*(\ ){1}(-|(a\.)|(i\.)|(1\.)){1}(\ ){1}']
    end = '(\n){1}'
    macro = macros.ListItem

    def resolve_argument_string(self):
        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback

        self.level = self.chunk.count(' ') - 2
        for i in types.keys():
            if re.search(i, self.chunk[self.level:]):
                self.type_ = types[i]
        self.content = self.stream[0:endMatch.start()]
        self.argument_string = ''.join([str(self.level), ' ', self.type_, ' ', self.content])
        

parsers = [Article, Book, Hyperlink, List, ListItem, Nadpis, NeformatovanyText, Odstavec, Sekce, Silne, TriTecky, Zvyraznene]
