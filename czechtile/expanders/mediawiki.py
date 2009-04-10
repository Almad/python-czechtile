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
from .base import CzechtileExpander, EmptyExpander, ExpanderMap, \
                  TextNodeExpander

class Document(EmptyExpander): pass
class Book(EmptyExpander): pass
class Article(EmptyExpander): pass
class Sekce(EmptyExpander): pass

class Nadpis(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, \
            u'=' * node.level + u' ', u' ' + u'=' * node.level)

class Odstavec(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'', u'\n\n')

class NeformatovanyText(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<pre>', u'</pre>')

class Silne(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u"'''", u"'''")

class Zvyraznene(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u"''", u"''")

class Hyperlink(CzechtileExpander):
    prefix = u'[%s '
    sufix = u']'

    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, \
          self.prefix % unicode(node.link), self.sufix)

class List(CzechtileExpander):
    def expand(self, node, format, node_map):
        if node.token == '-':
            token = u'*'
        else:
            token = u'#'
        res = self.expand_with_content(node, format, node_map)
        res = u''.join([token + r + u'\n' for r in res.split('\n') if r])
        if not isinstance(node.parent, nodes.List):
            res = '\n\n' + res
        return res

class ListItem(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u' ', u'\n')

class Preskrtnute(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map,
          u'<s>', u'</s>')

class Obrazek(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'[[Image:%s]]' % node.source

# FIXME: nasledujuce expandery su dost divne
class PevnaMedzera(CzechtileExpander):
    def expand(self, *args, **kwargs):
        return ' '

class Pomlcka(CzechtileExpander):
    def expand(self, *args, **kwargs):
        return '-'

class TriTecky(CzechtileExpander):
    def expand(self, *args, **kwargs):
        return '...'

class Uvozovky(CzechtileExpander):
    def expand(self, *args, **kwargs):
        return '"'

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
    nodes.Hyperlink: Hyperlink,
    nodes.List: List,
    nodes.ListItem: ListItem,
    nodes.Preskrtnute: Preskrtnute,
    nodes.Obrazek: Obrazek,

    nodes.PevnaMedzera: PevnaMedzera,
    nodes.Pomlcka: Pomlcka,
    nodes.TriTecky: TriTecky,
    nodes.Uvozovky: Uvozovky
})
