# -*- coding: utf-8 -*-

""" Parsers
"""

__license__ = """Czechtile: WikiHezkyCesky
Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

import re

from sneakylang.parser import Parser, ParserRollback
import macros

parsers = []   # list of allowed parsers

### "Global content" holders ###

class Book(Parser):
    start = None
    macro = macros.Book
    end = ''

    def resolve_argument_string(self):
        self.content = self.stream
        self.stream = ''
        self.argument_string = self.content
parsers += [Book]   # enable the Book parser

class Article(Parser):
    start = None
    macro = macros.Article

    def resolve_argument_string(self):
        self.content = self.stream
        self.stream = ''
        self.argument_string = self.content
parsers += [Article]

class Sekce(Parser):
    start = None
    macro = macros.Sekce
parsers += [Sekce]

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
parsers += [Odstavec]

class NeformatovanyText(Parser):
    start = [u'(\n§§\n){1}']
    end = u'(\n§§\n){1}'
    macro = macros.NeformatovanyText

    def resolve_argument_string(self):
        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback

        self.argument_string = self.stream[0:endMatch.start()]
        self.stream = self.stream[endMatch.end():]
parsers += [NeformatovanyText]

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
parsers += [Nadpis]

### List-related parsers ###

class List(Parser):
    tokens = ['-', '1.', 'a.', 'i.']

    def start(tokens):
        tokens_re = '|'.join(tokens).replace('.', '\.')
        tokens_re = '(%s){1}' % tokens_re
        start = ['^(\n)*(\ )?%s(\ ){1}' % tokens_re,
            '(\n){1,2}(\ )*%s(\ ){1}' % tokens_re]#,
            #'(\n){1}(\ )*%s(\ ){1}' % tokens_re]
        return start, tokens_re
    start, tokens_re = start(tokens)
    macro = macros.List

    def resolve_argument_string(self):
        # one space is after the token (-1 for it's not interesting for us)
        # and we want the decremented result (another -1)
        self.chunk = self.chunk.replace('\n', '')
        spaces_dec = self.chunk.count(' ') - 2

        end = '(\n){1}(\ ){0,%d}%s(\ ){1}|(\n){2}' % (spaces_dec,
          self.tokens_re)

        end_doc = '(\n)*$|$'

        # two-stage end matching
        endMatch = re.search(end, self.stream)
        if endMatch:
            stream_start = endMatch.start()
        else:
            endMatch = re.search(end_doc, self.stream)
            if not endMatch:
                raise ParserRollback
            stream_start = endMatch.end()

        # extract a token from chunk
        tokens_search = re.search(self.tokens_re, self.chunk)
        token = tokens_search.group(0)

        # generate content for the macro call
        pre = ''
        if not self.chunk.startswith(' '):
            assert spaces_dec < 0
            pre = ' '

        self.content = self.chunk + self.stream[:endMatch.start()]
        self.content = '\n' + \
            ''.join([pre + c[max(spaces_dec, 0):] + '\n'
            for c in self.content.split('\n') if c])[:-1]
        self.stream = self.stream[stream_start:]

        self.argument_string = ' '.join([token, self.content])
parsers += [List]

class ListItem(Parser):
    def start():
        return ['(\n){1}(\ )?%s(\ ){1}' % List.tokens_re]
    start = start()
    end = '(\n){1}(\ )*%s(\ ){1}|$' % List.tokens_re
    macro = macros.ListItem

    priority = 1

    def resolve_argument_string(self):
        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback

        self.content = self.stream[:endMatch.start()]
        self.stream = self.stream[endMatch.start():]
        self.argument_string = self.content
parsers += [ListItem]

### End of list-related parsers ###

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
parsers += [Silne]

class Zvyraznene(InlineParserEndingWithBegin):
    start = ['("){2}', '(/){2}']
    macro = macros.Zvyraznene
parsers += [Zvyraznene]

class Hyperlink(Parser):
    hyperlink_pattern = 'http:\/\/\w+([-_\.]?\w)*\.[a-zA-Z]{2,4}(\/{1}[-_~&=\?\.\w%]*)*(#{1}[-_~&=\?\.\w%]*)?'
    www_pattern = 'w{3}\.{1}\w+([-_\.]?\w)*\.[a-zA-Z]{2,4}(\/{1}[-_~&=\?\.\w%]*)*(#{1}[-_~&=\?\.\w%]*)?'
    start = [hyperlink_pattern, '\('+hyperlink_pattern, www_pattern]
    end = '(\))'
    macro = macros.Hyperlink

    def resolve_argument_string(self):
        if not self.chunk.startswith('('):
            # Easy substitution of http://link
            self.link = self.chunk
            if self.link.startswith('www.'):
                self.link = "http://" + self.link
            self.argument_string = ''.join([self.link, ' ', self.chunk])
        else:
            endMatch = re.search(self.__class__.end, self.stream)
            if not endMatch:
                raise ParserRollback()
            self.link = self.chunk[1:]
            text = re.sub("^(\s)*", '', self.stream[0:endMatch.start()])
            # empty text, we should avoid this because of hyperlink in parenthesis,
            # see bug #39
            if text == '':
                raise ParserRollback
            self.argument_string = ''.join([self.link, ' ', text])

            self.chunk_end = self.stream[endMatch.start():endMatch.end()]
            self.stream = self.stream[endMatch.end():]
parsers += [Hyperlink]

### Typographic parsers - transfer text to czech typographic customs ###

class TypographicParser(Parser):
    def resolve_argument_string(self):
        pass

    def call_macro(self):
        return self.macro(self.register, self.register_map).expand()

class TriTecky(TypographicParser):
    start = ['(\.){3}']
    end = None
    macro = macros.TriTecky

parsers += [TriTecky]

class Pomlcka(Parser):
    start = ['(?!(\n){1,}(\ )*)(\ ){0,1}(\-){1}']  # be aware of that dash can be a list token (check if it isn't!)
    end = '(\ ){0,1}'
    macro = macros.Pomlcka

    def resolve_argument_string(self):
        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback

        self.argument_string = self.chunk + self.stream[0:endMatch.end()]
        self.stream = self.stream[endMatch.end():]
parsers += [Pomlcka]

class Trademark(TypographicParser):
    start = ['(\(TM\)){1}', '(\(tm\)){1}']
    end = None
    macro = macros.Trademark

parsers += [Trademark]

class Copyright(TypographicParser):
    start = ['(\(C\)){1}', '(\(c\)){1}']
    end = None
    macro = macros.Copyright

parsers += [Copyright]

class RightsReserved(TypographicParser):
    start = ['(\(R\)){1}', '(\(r\)){1}']
    end = None
    macro = macros.RightsReserved

parsers += [RightsReserved]

class Uvozovky(Parser):
    start = ['("){1}']
    end = '("){1}'
    macro = macros.Uvozovky

    def resolve_argument_string(self):
        endMatch = re.search(self.__class__.end, self.stream)
        if not endMatch:
            raise ParserRollback()

        self.argument_string = self.stream[0:endMatch.start()]
        self.stream = self.stream[endMatch.end():]

	if self.stream[:2] == '""':
	    raise ParserRollback
parsers += [Uvozovky]

### End of typographic parsers ###

### End of inline elements ###
