from czechtile import nodes
from czechtile.expanders import entities
from czechtile.expanders.base import CzechtileExpander, ExpanderMap, TextNodeExpander, ListExpander, ListItemExpander

from html5lib.sanitizer import HTMLSanitizerMixin


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

class HorniIndex(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<sup>', u'</sup>')

class DolniIndex(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<sub>', u'</sub>')

class List(ListExpander):
    tag_map = {
        '-': {'tag': u'ul', 'attrs': u''},
        '1.': {'tag': u'ol', 'attrs': u' type="1"'},
        'a.': {'tag': u'ol', 'attrs': u' type="a"'},
        'i.': {'tag': u'ol', 'attrs': u' type="i"'}
    }

class ListItem(ListItemExpander):
    tag_map = {'tag': u'li', 'attrs': u''}

class Preskrtnute(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map,
          u'<strike>', u'</strike>')

class Obrazek(CzechtileExpander):

    def expand(self, node, format, node_map):
        # sanitize picture content
        src = u""
        sanitizer = HTMLSanitizerMixin()
        tokens = sanitizer.sanitize_token({"type":"StartTag", "name":"img", "data":[("src", node.source)]})['data']
        if len(tokens) > 0:
            for attribute, value in tokens:
                if attribute == "src":
                    src = value
        return u''.join([u'<img src="', src, '" />'])

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
    nodes.HorniIndex: HorniIndex,
    nodes.DolniIndex: DolniIndex,
    nodes.TriTecky: entities.TriTecky,
    nodes.Pomlcka: entities.Pomlcka,
    nodes.Trademark: entities.Trademark,
    nodes.Copyright: entities.Copyright,
    nodes.RightsReserved: entities.RightsReserved,
    nodes.Hyperlink: Hyperlink,
    nodes.List: List,
    nodes.ListItem: ListItem,
    nodes.Uvozovky: entities.Uvozovky,
    nodes.PevnaMedzera: entities.PevnaMedzera,
    nodes.Preskrtnute: Preskrtnute,
    nodes.Obrazek: Obrazek
})