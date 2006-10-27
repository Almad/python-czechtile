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

from sneakylang import Macro, parse, TextNode

import nodes

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
            doc.addChild(n)
        return doc

class Article(Macro):
    name = 'clanek'
    help = '((clanek text clanku))'

    def expand(self, content):
        doc = nodes.Article()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
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
            node.addChild(n)
        return node

class Zvyraznene(Macro):
    name = 'zvyraznene'
    help = '((zvyraznene zesilneny text))'

class Silne(Macro):
    name = 'silne'
    help = '((silne zesilneny text))'