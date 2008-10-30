###
# Czechtile: WikiHezkyCesky
# Copyright (C) 2006 Lukas "Almad" Linhart http://www.almad.net/
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
###

from czechtile import nodes
from czechtile.expanders import entities
from czechtile.expanders.base import CzechtileExpander, ExpanderMap, ListExpander, ListItemExpander, TextNodeExpander

class Document(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<?xml version="1.0" encoding="UTF-8"?>\n')

class Book(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><book>', u'</book>')

class Article(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><article>', u'</article>')

class Sekce(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<section>', u'</section>')

class Nadpis(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<title>', u'</title>')

class Odstavec(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<para>', u'</para>')

class NeformatovanyText(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<literallayout>', u'</literallayout>')

# TODO: zesilene vs. silne v docbook

class Silne(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<emphasis role="bold">', u'</emphasis>')

class Zvyraznene(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<emphasis>', u'</emphasis>')

class Hyperlink(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u''.join([u'<ulink url="', unicode(node.link), u'">']), u'</ulink>')

class FootNote(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<footnote><para>', u'</para></footnote>')


class Preskrtnute(CzechtileExpander):
    def expand(self, node, format, node_map):
        # TODO: overit docbook tag
        return self.expand_with_content(node, format, node_map,
          u'<emphasis role="strikethrough">', u'</emphasis>')

class Obrazek(CzechtileExpander):
    def expand(self, node, format, node_map):
        # TODO: overit docbook tag
        return u''.join([u'<mediaobject><imageobject><imagedata fileref="',
          node.source, '" /></imageobject></mediaobject>'])

class List(ListExpander):
    types = {
        'itemized': (u'itemizedlist',),
        '1-ordered': (u'orderedlist', u'numeration="arabic"'),
        'A-ordered': (u'orderedlist', u'numeration="loweralpha"'),
        'I-ordered': (u'orderedlist', u'numeration="lowerroman"')
    }

class ListItem(ListItemExpander):
    list_expander = List
    tag = (u'listitem',)


map = ExpanderMap({
    nodes.DocumentNode: Document,
    nodes.TextNode: TextNodeExpander,

    nodes.Book: Book,
    nodes.Article: Article,
    nodes.Sekce: Sekce,
    nodes.Nadpis: Nadpis,
    nodes.Odstavec: Odstavec,
    nodes.NeformatovanyText: NeformatovanyText,
    nodes.Silne: Silne,
    nodes.Zvyraznene: Zvyraznene,
    nodes.TriTecky: entities.TriTecky,
    nodes.Pomlcka: entities.Pomlcka,
    nodes.Hyperlink: Hyperlink,
    nodes.List: List,
    nodes.ListItem: ListItem,
    nodes.Uvodzovky: entities.Uvodzovky,
    nodes.FootNote: FootNote,
    nodes.PevnaMedzera: entities.PevnaMedzera,
    nodes.Preskrtnute: Preskrtnute,
    nodes.Obrazek: Obrazek
})
