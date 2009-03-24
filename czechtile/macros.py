# -*- coding: utf-8 -*-

""" Macros
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

from sneakylang import parse, Macro, Document
from sneakylang.parser import ParserRollback

from czechtile import nodes

class CzechtileMacro(Macro):

    def _macroCallWithoutRequiredQuotes(self, *args):
        content = ''.join([''.join([arg, ' ']) for arg in args])[:-1]
        return self.expand(content)

    def parse_argument_string(self, argument_string):
        self.arguments = [argument_string]

class MacroWrappingParagraph(CzechtileMacro):

    def wrap_text_nodes(self, node):
        # we must go with numbers as we must replace textnode with it's tree on same position
        for child in node.children:
            if isinstance(child, nodes.TextNode):
                self.builder.set_actual_node(child)
                text = re.sub("^(\s)*", "", re.sub("(\s)*$", "", child.content))
                for para_content in text.split('\n\n'):
                    macro = Odstavec.argument_call(para_content, self.register, self.builder, self.state)
                    macro.expand()

class Book(MacroWrappingParagraph):
    name = 'kniha'
    help = '((kniha text knihy))'

    def expand_to_nodes(self, content):
        node = nodes.Book()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.wrap_text_nodes(node)
        self.builder.move_up()

class Article(MacroWrappingParagraph):
    name = 'clanek'
    help = '((clanek text clanku))'

    def expand_to_nodes(self, content):
        node = nodes.Article()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.wrap_text_nodes(node)
        self.builder.move_up()


class Sekce(Document):
    name = 'sekce'
    help = '((sekce text sekce))'

class Nadpis(CzechtileMacro):
    name = 'nadpis'
    help = '((nadpis cislo_urovne text nadpisu))'

    def parse_argument_string(self, argument_string):
        args = argument_string.split()
        try:
            level = int(args[0])
        except ValueError, err:
            raise ParserRollback(err)

        self.arguments = [level, ''.join([''.join([arg, ' ']) for arg in args[1:]])[:-1]]

    def expand_to_nodes(self, level, content):
        node = nodes.Nadpis()
        node.level = level
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        assert node == self.builder.actual_node
        self.builder.move_up()

class Odstavec(CzechtileMacro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'

    def expand_to_nodes(self, content):
        node = nodes.Odstavec()
        self.builder.append(node, move_actual=False)
        if isinstance(node.parent, nodes.TextNode):
            self.builder.replace(node)
        self.builder.set_actual_node(node)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        assert node == self.builder.actual_node
        self.builder.move_up()

class NeformatovanyText(CzechtileMacro):
    name = 'neformatovany-text'
    help = '((neformatovany-text nenaformatovany obsah textu))'

    def expand_to_nodes(self, content):
        node = nodes.NeformatovanyText()
        self.builder.append(node, move_actual=True)
        tn = nodes.TextNode()
        tn.content = content
        self.builder.append(tn, move_actual=False)
        self.builder.move_up()

class Zvyraznene(CzechtileMacro):
    name = 'zvyraznene'
    help = '((zvyraznene zesilneny text))'

    def expand_to_nodes(self, content):
        node = nodes.Zvyraznene()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()

class FootNote(CzechtileMacro):
    name = 'poznamka'
    help = '((poznamka text pod carou))'

    def expand_to_nodes(self, content):
        node = nodes.FootNote()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()


class Silne(CzechtileMacro):
    name = 'silne'
    help = '((silne zesilneny text))'

    def expand_to_nodes(self, content):
        node = nodes.Silne()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()

class Hyperlink(CzechtileMacro):
    name = 'odkaz'
    help = '((odkaz http://adresa/linku text linku))'

    def parse_argument_string(self, argument_string):
        args = argument_string.split()
        link = args[0]
        self.arguments = [link, ''.join([''.join([arg, ' ']) for arg in args[1:]])[:-1]]

    def expand_to_nodes(self, link, content):
        node = nodes.Hyperlink()
        node.link = link
        self.builder.append(node, move_actual = True)
        if link == content:
            tn = nodes.TextNode()
            tn.content = content
            self.builder.append(tn, move_actual=False)
        else:
            parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()


class TriTecky(CzechtileMacro):
    name = 'tri_tecky'
    help = '((tri_tecky))'

    def expand_to_nodes(self, *args):
        self.builder.append(nodes.TriTecky(), move_actual=False)

class Pomlcka(CzechtileMacro):
    name = 'pomlcka'
    help = '((pomlcka))'

    def expand_to_nodes(self, string):
        node = nodes.Pomlcka()
        signals = [0, 1]
        spaces = []

        if string.startswith(u' '):
            spaces.append(signals[0])
        if string.endswith(u' '):
            spaces.append(signals[1])

        if spaces == []:
            node.spojovnik = True
        else:
            node.spojovnik = False

        if signals[0] in spaces:
            self.builder.append(nodes.PevnaMedzera(), move_actual=False)
        self.builder.append(node, move_actual=False)
        if signals[1] in spaces:
            self.builder.append(nodes.PevnaMedzera(), move_actual=False)

class Uvozovky(CzechtileMacro):
    name = 'uvozovky'
    help = '((uvozovky text v uvozovkach))'

    def expand_to_nodes(self, content):
        node = nodes.Uvozovky()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()

class List(CzechtileMacro):
    name = 'seznam'
    help = '((seznam token obsah))'

    def parse_argument_string(self, argument_string):
        self.arguments = argument_string.split(' ', 1)

    def expand_to_nodes(self, token, content):
        node = nodes.List()
        node.token = token
        self.builder.append(node, move_actual=True)

        prepend = False
        for text in content.split('\n'):
            if text:
                # deal with lists which don't start with space character
                if not text.startswith(' '):
                    prepend = True
                if prepend:
                    text = ' ' + text

                try:
                    parse('\n' + text, self.register_map, self.register, builder=self.builder, state=self.state)
                except ValueError:
                    # handle the `Adding a text node, but one is already present' error
                    assert node.last_added_child.__class__ == nodes.TextNode
                    node.last_added_child.content += '\n' + text

        for child in node.children:
            if child.__class__ == nodes.TextNode:
                new_content = ''
                for text in child.content.split('\n'):
                    if text:
                        new_content += '\n' + text[1:]

                parse('\n' + new_content, self.register_map, self.register, builder=self.builder, state=self.state)
                self.builder.set_actual_node(child)
                self.builder.replace(node.last_added_child)
                node.children.pop()
                #macro = List.argument_call(new_content, self.register, self.builder, self.state)
                #macro.expand()

        self.builder.set_actual_node(node)
        self.builder.move_up()


class ListItem(CzechtileMacro):
    name = 'polozka'
    help = '((polozka text))'

    def expand_to_nodes(self, content):
        node = nodes.ListItem()
        self.builder.append(node, move_actual=True)
        parse(content, self.register_map, self.register, builder=self.builder, state=self.state)
        self.builder.move_up()

class Preskrtnute(CzechtileMacro):
    name = 'preskrtnute'
    help = '((preskrtnute preskrtnuty text))'

    def expand_to_nodes(self, content):
        node = nodes.Preskrtnute()
        self.builder.append(node, move_actual=True)
        parse(content, self.register_map, self.register, \
          builder=self.builder, state=self.state)
        self.builder.move_up()

class Obrazek(CzechtileMacro):
    name = 'obrazek'
    help = '((obrazek lokace))'

    def expand_to_nodes(self, source):
        node = nodes.Obrazek()
        node.source = source
        self.builder.append(node, move_actual=True)
        self.builder.move_up()