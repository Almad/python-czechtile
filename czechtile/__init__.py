# -*- coding: utf-8 -*-

""" Czechtile: WikiHezky Cesky
Set of rules for SneakyLang [http://projects.almad.net/sneakylang]
"""

__version__ = [0.2, "alpha", 3]
__versionstr__ = 'czechtile-'+str(__version__[0])

if not (__version__[1] == "stable" and __version__[2] == 0):
    __versionstr__ = __versionstr__+"_"+__version__[1]+str(__version__[2])


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

from sneakylang import Register, RegisterMap, TreeBuilder

from czechtile import expanders
from czechtile import nodes
from czechtile import macros
from czechtile import parsers

common_inline_macros = [macros.Zvyraznene, macros.Silne,
      macros.Hyperlink, macros.TriTecky, macros.Pomlcka,
      macros.Uvozovky, macros.FootNote, macros.Preskrtnute
]

# map parsers to registers with nodes allowed
register_map = RegisterMap({
    macros.Document : Register([macros.Book, macros.Article], parsers.parsers),
    macros.Book : Register([macros.Sekce, macros.Odstavec, macros.Nadpis, macros.NeformatovanyText, macros.List, macros.Obrazek], parsers.parsers),
    macros.Sekce : Register([macros.Odstavec, macros.Nadpis, macros.NeformatovanyText, macros.List, macros.Obrazek], parsers.parsers),
    macros.Odstavec : Register(common_inline_macros, parsers.parsers),
    macros.Hyperlink : Register(common_inline_macros, parsers.parsers),
    macros.Nadpis : Register([macros.Hyperlink, macros.Uvozovky, macros.FootNote, macros.Pomlcka], parsers.parsers),
    macros.Zvyraznene : Register([macros.Hyperlink, macros.Uvozovky, macros.FootNote, macros.Pomlcka], parsers.parsers),
    macros.Silne : Register([macros.Hyperlink, macros.Uvozovky, macros.FootNote, macros.Pomlcka], parsers.parsers),
    macros.NeformatovanyText : Register([], parsers.parsers),
    macros.List : Register([macros.List, macros.ListItem], parsers.parsers),
    macros.ListItem : Register(common_inline_macros, parsers.parsers),
    macros.Uvozovky : Register(common_inline_macros, parsers.parsers),

})
register_map[macros.Article] = register_map[macros.Book]
register_map[macros.FootNote] = register_map[macros.Odstavec]

# map nodes to expanders
expander_map = expanders.ExpanderMap()
expander_map.update({
    'docbook4': expanders.docbook4.map,
    'docbook5': expanders.docbook5.map,
    'xhtml11': expanders.xhtml11.map,
    'bbcode': expanders.bbcode.map,
    'mediawiki': expanders.mediawiki.map
})

expand = expanders.expand

### overwrite SneakyLang's parse method, we want everything to be wrapped in document_type
def parse(stream, register_map, document_type=macros.Article, state=None):
    builder = TreeBuilder()
    builder.set_root(nodes.DocumentNode())
    #dtype = document_type(stream, None, '', register_map[document_type.macro])
    dtype = document_type(register_map, builder, state)
    dtype.arguments = [stream]
    dtype.expand()

    return builder.root
