# -*- coding: utf-8 -*-

""" Czechtile: WikiHezky Cesky
Set of rules for SneakyLang [http://projects.almad.net/sneakylang]
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


from sneakylang import *
import sneakylang

import nodes
import macros
import expanders
import parsers

# map parsers to registers with nodes allowed
registerMap = {
    parsers.Document : Register([parsers.Book, parsers.Article]),
    parsers.Book : Register([parsers.Sekce, parsers.Odstavec, parsers.Nadpis, parsers.ListItem]),
    parsers.Sekce : Register([parsers.Odstavec, parsers.Nadpis]),
    parsers.Odstavec : Register([parsers.Zvyraznene, parsers.Silne,
                       parsers.Hyperlink, parsers.TriTecky, parsers.ListItem]),
    parsers.Hyperlink : Register([])

}
registerMap[parsers.Article] = registerMap[parsers.Book]


# map nodes to expanders
nodeMap = {
    'docbook4' : {
        nodes.Document : expanders.DocumentDocbook4,
        nodes.Book : expanders.BookDocbook4,
        nodes.Article : expanders.ArticleDocbook4,
        nodes.Sekce : expanders.SekceDocbook4,
        TextNode : TextNodeExpander,
        nodes.Nadpis : expanders.NadpisDocbook4,
        nodes.Odstavec : expanders.OdstavecDocbook4,
        nodes.Silne : expanders.SilneDocbook4,
        nodes.Zvyraznene : expanders.ZvyrazneneDocbook4,
        nodes.TriTecky : expanders.TriTeckyEntity,
        nodes.Hyperlink : expanders.HyperlinkDocbook4,
        nodes.List : expanders.ListDocbook4,
        nodes.ListItem : expanders.ListDocbook4
    },
    'docbook5' : {
    },
    'xhtml11' : {
        nodes.Document : expanders.DocumentXhtml11,
        nodes.Book : expanders.BookXhtml11,
        nodes.Article : expanders.ArticleXhtml11,
        TextNode : TextNodeExpander,
        nodes.Nadpis : expanders.NadpisXhtml11,
        nodes.Odstavec : expanders.OdstavecXhtml11,
        nodes.Silne : expanders.SilneXhtml11,
        nodes.Zvyraznene : expanders.ZvyrazneneXhtml11,
        nodes.TriTecky : expanders.TriTeckyEntity,
        nodes.Hyperlink : expanders.HyperlinkXhtml11
    }
}

### overwrite SneakyLang's parse method, we wont' everythink to be wrapped in Document
def parse(stream, registerMap, documentType=parsers.Article):
    parser = parsers.Document(documentType(stream, registerMap[documentType], '', registerMap), stream, registerMap[parsers.Document], '', registerMap)
    documentNode = parser.parse()
    return documentNode

