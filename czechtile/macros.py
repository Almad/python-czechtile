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

from sneakylang import Macro, parse, TextNode, Document
import nodes

def _wrap_text(text_node, register, register_map):
    """ Wrap unbound TextNode to Paragraph """
    #FIXME: This is considered to be a hack, overwrite register_map
    from parsers import Odstavec as OdstavecParser
    para = Odstavec.argument_call(re.sub("^(\s)*", "", re.sub("(\s)*$", "", text_node.content)), register)
    return para.expand()

class CzechtileMacro(Macro):

    def _macroCallWithoutRequiredQuotes(self, *args):
        content = ''.join([''.join([arg, ' ']) for arg in args])[:-1]
        return self.expand(content)

    def parse_argument_string(self, argument_string):
        self.arguments = [argument_string]

class Book(CzechtileMacro):
    name = 'kniha'
    help = '((kniha text knihy))'

    def expand_to_nodes(self, content):
        doc = nodes.Book()
        child_nodes = parse(content, self.register_map)
        for n in child_nodes:
            if isinstance(n, TextNode):
                doc.add_child(_wrap_text(n, self.register, self.register_map))
            else:
                doc.add_child(n)
        return doc

class Article(CzechtileMacro):
    name = 'clanek'
    help = '((clanek text clanku))'

    def expand_to_nodes(self, content):
        doc = nodes.Article()
        child_nodes = parse(content, self.register_map, self.register)
        for n in child_nodes:
            if isinstance(n, TextNode):
                doc.add_child(_wrap_text(n, self.register, self.register_map))
            else:
                doc.add_child(n)

        return doc


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
        tn = TextNode()
        tn.content = content
        node.add_child(tn)
        return node

class Odstavec(CzechtileMacro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'

    def expand_to_nodes(self, content):
        node = nodes.Odstavec()
        child_nodes = parse(content, self.register_map, self.register)
        for n in child_nodes:
            node.add_child(n)
        return node

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
    name = 'link'
    help = '((link http://adresa/linku text linku))'

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

    def expand_to_nodes(self, content):
        node = nodes.ListItem()
        child_nodes = parse(content, self.register_map, self.register)
        for n in child_nodes:
            node.add_child(n)
        return node


class List(CzechtileMacro):
    name = 'list'
    help = '((list typ obsah seznamu))'

    def expand_to_nodes(self, type_, content):
        node = nodes.List()
        node.type_ = type_
        child_nodes = parse(content, self.register_map, self.register)
        print self.register.parser_name_map
        for n in child_nodes:
            if isinstance(n, nodes.ListItem) or isinstance(n, nodes.List):                                                                                                                                                                                                 # this if statement is necessary because without it there
            # i-dont-know-why will occur textnodes
                node.add_child(n)
        return node
