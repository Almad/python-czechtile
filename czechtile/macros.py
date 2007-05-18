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

from sneakylang import Macro, parse, TextNode, Document, treebuilder
import nodes

def _wrap_text(text_node, register, register_map, builder, state):
    """ Wrap unbound TextNode to Paragraph """
    #FIXME: This is considered to be a hack, overwrite register_map
    text = re.sub("^(\s)*", "", re.sub("(\s)*$", "", text_node.content))
    for para_content in text.split('\n\n'):
        macro = Odstavec.argument_call(para_content, register, builder, state)
        macro.expand()

class CzechtileMacro(Macro):

    def _macroCallWithoutRequiredQuotes(self, *args):
        content = ''.join([''.join([arg, ' ']) for arg in args])[:-1]
        return self.expand(content)

    def parse_argument_string(self, argument_string):
        self.arguments = [argument_string]

class MacroWrappingParagraph(CzechtileMacro):

    def wrap_text_nodes(self, node):
        # we must go with numbers as we must replace textnode with it's tree on same position
        new_children = []
        for child in node.children:
            if isinstance(child, TextNode):
                builder = treebuilder.TreeBuilder()
                # set fake root
                builder.set_root(TextNode())
                _wrap_text(child, self.register, self.register_map, builder, self.state)
                for n in builder.root.children:
                    new_children.append(n)
            else:
                new_children.append(child)
        node.children = new_children


class Book(MacroWrappingParagraph):
    name = 'kniha'
    help = '((kniha text knihy))'

    def expand_to_nodes(self, content):
        node = nodes.Book()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder)
        self.wrap_text_nodes(node)
        self.builder.move_up()

class Article(MacroWrappingParagraph):
    name = 'clanek'
    help = '((clanek text clanku))'

    def expand_to_nodes(self, content):
        node = nodes.Article()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder)
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
        level = int(args[0])
        self.arguments = [level, ''.join([''.join([arg, ' ']) for arg in args[1:]])[:-1]]

    def expand_to_nodes(self, level, content):
        node = nodes.Nadpis()
        node.level = level
        child_nodes = parse(content, self.register_map, self.register)
        for n in child_nodes:
            node.add_child(n)
        return node

class Odstavec(CzechtileMacro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'

    def expand_to_nodes(self, content):
        node = nodes.Odstavec()
        self.builder.append(node, move_actual = True)
        parse(content, self.register_map, self.register, builder=self.builder)
        self.builder.move_up()

class NeformatovanyText(CzechtileMacro):
    name = 'neformatovany-text'
    help = '((neformatovany-text nenaformatovany obsah textu))'

    def expand_to_nodes(self, content):
        node = nodes.NeformatovanyText()
        tn = TextNode()
        tn.content = content
        node.add_child(tn)
        return node

class Zvyraznene(CzechtileMacro):
    name = 'zvyraznene'
    help = '((zvyraznene zesilneny text))'

    def expand_to_nodes(self, content):
        node = nodes.Zvyraznene()
        child_nodes = parse(content, self.register_map, self.register)
        for n in child_nodes:
            node.add_child(n)
        return node

class Silne(CzechtileMacro):
    name = 'silne'
    help = '((silne zesilneny text))'

    def expand_to_nodes(self, content):
        node = nodes.Silne()
        child_nodes = parse(content, self.register_map, self.register)
        for n in child_nodes:
            node.add_child(n)
        return node

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
        if link == content:
            tn = TextNode()
            tn.content = content
            node.add_child(tn)
        else:
            child_nodes = parse(content, self.register_map, self.register)
            for n in child_nodes:
                node.add_child(n)
        return node


class TriTecky(CzechtileMacro):
    name = 'tri_tecky'
    help = '((tri_tecky))'

    def expand_to_nodes(self, *args):
        return nodes.TriTecky()

class ListItem(CzechtileMacro):
    name = 'listitem'
    help = '((listitem text polozky))'

    def parse_argument_string(self, argument_string):
        args = argument_string.split()
        level = int(args[0])
        type_ = args[1]
        self.arguments = [level, type_, ''.join([''.join([arg, ' ']) for arg in args[2:]])[:-1]]

    def expand_to_nodes(self, level, type_, content):
        node = nodes.ListItem()
        node.level = level
        node.type_ = type_
        child_nodes = parse(content, self.register_map, self.register)
        for n in child_nodes:
            node.add_child(n)
        return node


class List(CzechtileMacro):
    name = 'list'
    help = '((list typ obsah seznamu))'

    def parse_argument_string(self, argument_string):
        args = argument_string.split('!::')
        type_ = args[0]
        self.arguments = [type_, ''.join([''.join([arg, ' ']) for arg in args[1:]])[:-1]]

    def expand_to_nodes(self, type_, content):
        node = nodes.List()
        node.type_ = type_
        child_nodes = parse(content, self.register_map, self.register)
        for n in child_nodes:
            if isinstance(n, nodes.ListItem):
            # this if statement is necessary because without it there
            # i-dont-know-why will occur textnodes
            # -- that was before sl upgrade, i don't know if it occur now too
                node.add_child(n)
        return node
