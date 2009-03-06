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
        if getattr(node, "wrap_document", True):
            header = u'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="cs" lang="cs">'
            footer = u'</html>'
        else:
            header = u''
            footer = u''
        return self.expand_with_content(node, format, node_map, header, footer)

class Book(CzechtileExpander):
    def expand(self, node, format, node_map):
        if getattr(node.parent, "wrap_document", True):
            header = u'<body class="book">'
            footer = u'</body>'
        else:
            header = u''
            footer = u''
        return self.expand_with_content(node, format, node_map, header, footer)

class Article(CzechtileExpander):
    def expand(self, node, format, node_map):
        if getattr(node.parent, "wrap_document", True):
            header = u'<body class="article">'
            footer = u'</body>'
        else:
            header = u''
            footer = u''
        return self.expand_with_content(node, format, node_map, header, footer)

class Sekce(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map)

class Nadpis(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u''.join([u'<h', unicode(node.level), u'>']), u''.join([u'</h', unicode(node.level), u'>']))


class Odstavec(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<p>', u'</p>')

class NeformatovanyText(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<pre>', u'</pre>')


class Silne(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<strong>', u'</strong>')

class Zvyraznene(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<em>', u'</em>')

class Hyperlink(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u''.join([u'<a href="', unicode(node.link), u'">']), u'</a>')

class List(ListExpander):
    types = {
        'itemized': (u'ul',),
        '1-ordered': (u'ol', u'type="1"'),
        'A-ordered': (u'ol', u'type="a"'),
        'I-ordered': (u'ol', u'type="i"')
    }

class ListItem(ListItemExpander):
    list_expander = List
    tag = (u'li',)

class Preskrtnute(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map,
          u'<strike>', u'</strike>')

class Obrazek(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u''.join([u'<img src="', node.source, '" />'])

map = ExpanderMap({
    nodes.DocumentNode: Document,
    nodes.TextNode: TextNodeExpander,

    nodes.Book: Book,
    nodes.Article: Article,
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
    nodes.Uvozovky: entities.Uvozovky,
    nodes.PevnaMedzera: entities.PevnaMedzera,
    nodes.Preskrtnute: Preskrtnute,
    nodes.Obrazek: Obrazek
})
