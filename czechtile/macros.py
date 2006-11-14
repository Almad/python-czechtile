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

from sneakylang import Macro, parse, TextNode
import nodes

def _wrapText(textNode, register, registerMap):
    """ Wrap unbound TextNode to Paragraph """
    #FIXME: This is considered to be a hack, overwrite registerMap
    from parsers import Odstavec as OdstavecParser
    return Odstavec(registerMap[OdstavecParser], registerMap).expand(re.sub("^(\s)*", "", re.sub("(\s)*$", "", textNode.content)))

class Document(Macro):
    name = 'document'
    help = '<toto makro se nikdy nepouziva explicitne>'

    def expand(self, content, parser):
        doc = nodes.Document()
        doc.addChild(parser.parse())
        return doc

class Book(Macro):
    name = 'kniha'
    help = '((kniha text knihy))'

    def expand(self, content):
        doc = nodes.Book()
        child_nodes = parse(content, self.registerMap)
        for n in child_nodes:
            if isinstance(n, TextNode):
                doc.addChild(_wrapText(n, self.register, self.registerMap))
            else:
                doc.addChild(n)
        return doc

class Article(Macro):
    name = 'clanek'
    help = '((clanek text clanku))'

    def expand(self, content):
        doc = nodes.Article()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            if isinstance(n, TextNode):
                doc.addChild(_wrapText(n, self.register, self.registerMap))
            else:
                doc.addChild(n)

        return doc

class Sekce(Document):
    name = 'sekce'
    help = '((sekce text sekce))'

class Nadpis(Macro):
    name = 'nadpis'
    help = '((nadpis cislo_urovne text nadpisu))'

    def expand(self, level, content):
        node = nodes.Nadpis()
        node.level = level
        tn = TextNode()
        tn.content = content
        node.addChild(tn)
        return node

class Odstavec(Macro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'

    def expand(self, content):
        node = nodes.Odstavec()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            # this is temporary fix - without this
            # parsing of lists won't work properly
            # (if it will work at all)
            if isinstance(n, nodes.ListItem):
                node.children[0] = nodes.List()
                node.children[0].addChild(n)
#            else:
             # commented because of 'None' object in child_nodes
#                node.addChild(n)
        return node

class Zvyraznene(Macro):
    name = 'zvyraznene'
    help = '((zvyraznene zesilneny text))'

    def expand(self, content):
        node = nodes.Zvyraznene()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            node.addChild(n)
        return node

class Silne(Macro):
    name = 'silne'
    help = '((silne zesilneny text))'

    def expand(self, content):
        node = nodes.Silne()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            node.addChild(n)
        return node

class Hyperlink(Macro):
    name = 'link'
    help = '((link http://adresa/linku text linku))'

    def expand(self, link, content):
        node = nodes.Hyperlink()
        node.link = link
        if link == content:
            tn = TextNode()
            tn.content = content
            node.addChild(tn)
        else:
            child_nodes = parse(content, self.registerMap, self.register)
            for n in child_nodes:
                node.addChild(n)
        return node


class TriTecky(Macro):
    name = 'tri_tecky'
    help = '((tri_tecky))'

    def expand(self):
        return nodes.TriTecky()

class ListItem(Macro):
    name = 'listitem'
    help = '((listitem text polozky))'

    def expand(self, content):
        node = nodes.ListItem()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            node.addChild(n)
        return node


class List(Macro):
    name = 'list'
    help = '((list typ_zoznamu))'

    def expand(self, type_):
        node = nodes.List()
        return node
