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

from .. import nodes
from . import entities
from .base import CzechtileExpander, ExpanderMap, TextNodeExpander, \
                  ListExpander, ListItemExpander

class Document(CzechtileExpander):
    def expand(self, node, format, node_map):
        if getattr(node, "wrap_document", True):
            header = u'<?xml version="1.0" encoding="UTF-8"?>\n'
        else:
            header = u''
        return self.expand_with_content(node, format, node_map, header)

class Book(CzechtileExpander):
    def expand(self, node, format, node_map):
        if getattr(node.parent, "wrap_document", True):
            header = u'<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><book>'
            footer = u'</book>'
        else:
            header = u''
            footer = u''
        return self.expand_with_content(node, format, node_map, header, footer)

class Article(CzechtileExpander):
    def expand(self, node, format, node_map):
        if getattr(node.parent, "wrap_document", True):
            header = u'<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><article>'
            footer = u'</article>'
        else:
            header = u''
            footer = u''
        return self.expand_with_content(node, format, node_map, header, footer)

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
    tag_map = {
        '-': {'tag': u'itemizedlist', 'attrs': u''},
        '1.': {'tag': u'orderedlist', 'attrs': u' numeration="arabic"'},
        'a.': {'tag': u'orderedlist', 'attrs': u' numeration="loweralpha"'},
        'i.': {'tag': u'orderedlist', 'attrs': u' numeration="lowerroman"'}
    }

class ListItem(ListItemExpander):
    tag_map = {'tag': u'listitem', 'attrs': u''}


map = ExpanderMap({
    nodes.DocumentNode: Document,
    nodes.TextNode: TextNodeExpander,

    nodes.Book: Book,
    nodes.Article: Article,
    nodes.Sekce: Sekce,
    nodes.Nadpis: Nadpis,
    nodes.Odstavec: Odstavec,
    nodes.NeformatovanyText: NeformatovanyText,
    nodes.ZdrojovyKod: NeformatovanyText,
    nodes.Silne: Silne,
    nodes.Zvyraznene: Zvyraznene,
    nodes.TriTecky: entities.TriTecky,
    nodes.Pomlcka: entities.Pomlcka,
    nodes.Hyperlink: Hyperlink,
    nodes.List: List,
    nodes.ListItem: ListItem,
    nodes.Uvozovky: entities.Uvozovky,
    nodes.FootNote: FootNote,
    nodes.PevnaMedzera: entities.PevnaMedzera,
    nodes.Preskrtnute: Preskrtnute,
    nodes.Obrazek: Obrazek
})