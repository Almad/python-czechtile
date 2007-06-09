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
    macro = macros.Nadpis


    def get_stripped_line(self, line, level):
        chunk_end = ''

        while line.endswith(' '):
            chunk_end += line[:-1]
            line = line[:-1]

        if line.endswith('='*level):
            chunk_end += '='*level
            line = line[:-level]

        while line.endswith(' '):
            chunk_end += line[:-1]
            line = line[:-1]

        return line, chunk_end


    def resolve_argument_string(self):
        # we're interested only in this line


        line = self.stream.split('\n')[0]
        eqls = re.search('(=)+', self.chunk)
        level = len(eqls.group())

        content, chunk_end = self.get_stripped_line(line, level)

        # heading must either be after newline \n, or have the right side, otherwise
        # they're found inside any line with two =, lik in hyperlinks
        if not self.chunk.startswith('\n') and chunk_end == '':
            raise ParserRollback

        self.level = level
        self.content = content
        self.chunk_end = chunk_end

        # TODO: Eat also newline by len(line+'\n')
        # this is confusing lists after headings now
        self.stream = self.stream[len(line):]
        self.argument_string = ''.join([str(self.level), ' ', self.content])

### End of "block" elements ###

### Inline elements, mostly in Paragraphs ####

class InlineParserEndingWithBegin(Parser):
    def resolve_argument_string(self):
        endMatch = re.search(re.escape(self.chunk), self.stream)
        if not endMatch:
            raise ParserRollback
        self.argument_string = self.stream[0:endMatch.start()]
        self.chunk_end = self.stream[endMatch.start():endMatch.end()]
        self.stream = self.stream[endMatch.end():]

class Silne(InlineParserEndingWithBegin):
    start = ['("){3}', '(\*){1}']
    macro = macros.Silne

class Zvyraznene(InlineParserEndingWithBegin):
    start = ['("){2}', '(/){2}']
    macro = macros.Zvyraznene

class Hyperlink(Parser):
    hyperlink_pattern = 'http:\/\/\w+([-_\.]?\w)*\.[a-zA-Z]{2,4}(\/{1}[-_~&=\?\.\w%]*)*(#{1}[-_~&=\?\.\w%]*)?'
    start = [hyperlink_pattern, '\('+hyperlink_pattern]
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
    end = '(\n){2}|$'
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
