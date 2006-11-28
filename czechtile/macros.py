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

class CzechtileMacro(Macro):

    def _macroCallWithoutRequiredQuotes(self, *args):
        content = ''.join([''.join([arg, ' ']) for arg in args])[:-1]
        return self.expand(content)

    def macroCall(self, *args):
        """ This call is used when macro is triggered by macro syntax.
        Spec is ((macroname arg arg "space separated arg" arg)),
        but usually macros accept ((macroname space separated arg)); thus,
        overwrite this method and call either self._macroCallWithRequiredQuotes or
        self._macroCallWithotRequiredQuotes; default is second case.
        MUST be overwrited if call is different then expand(self.content) (another
        argument required)"""
        return self._macroCallWithoutRequiredQuotes(*args)

class Macro(CzechtileMacro):
    name = 'macro'
    help = 'nepouziva se'
    def __init__(self, *args, **kwargs):
        raise NotImplementedError, 'Macro macro should be never used'

class Document(CzechtileMacro):
    name = 'document'
    help = '<toto makro se nikdy nepouziva explicitne>'

    def expand(self, content, parser):
        doc = nodes.Document()
        doc.addChild(parser.parse())
        return doc

class Book(CzechtileMacro):
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

class Article(CzechtileMacro):
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

class Nadpis(CzechtileMacro):
    name = 'nadpis'
    help = '((nadpis cislo_urovne text nadpisu))'

    def expand(self, level, content):
        node = nodes.Nadpis()
        node.level = level
        tn = TextNode()
        tn.content = content
        node.addChild(tn)
        return node

class Odstavec(CzechtileMacro):
    name = 'odstavec'
    help = '((odstavec text odstavce))'

    def expand(self, content):
        node = nodes.Odstavec()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            node.addChild(n)
        return node

class NeformatovanyText(CzechtileMacro):
    name = 'neformatovany-text'
    help = '((neformatovany-text nenaformatovany obsah textu))'

    def expand(self, content):
        node = nodes.NeformatovanyText()
        tn = TextNode()
        tn.content = content
        node.addChild(tn)
        return node

class Zvyraznene(CzechtileMacro):
    name = 'zvyraznene'
    help = '((zvyraznene zesilneny text))'

    def expand(self, content):
        node = nodes.Zvyraznene()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            node.addChild(n)
        return node

class Silne(CzechtileMacro):
    name = 'silne'
    help = '((silne zesilneny text))'

    def expand(self, content):
        node = nodes.Silne()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            node.addChild(n)
        return node

class Hyperlink(CzechtileMacro):
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


class TriTecky(CzechtileMacro):
    name = 'tri_tecky'
    help = '((tri_tecky))'

    def expand(self):
        return nodes.TriTecky()

class ListItem(CzechtileMacro):
    name = 'listitem'
    help = '((listitem text polozky))'

    def expand(self, content):
        node = nodes.ListItem()
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            node.addChild(n)
        return node


class List(CzechtileMacro):
    name = 'list'
    help = '((list typ obsah seznamu))'

    def expand(self, type_, content):
        node = nodes.List()
        node.type_ = type_
        child_nodes = parse(content, self.registerMap, self.register)
        for n in child_nodes:
            if isinstance(n, nodes.ListItem):
            # this if statement is necessary because without it there
            # i-dont-know-why will occur textnodes
                node.addChild(n)
        return node
