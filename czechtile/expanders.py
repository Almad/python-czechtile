# -*- coding: utf-8 -*-

""" Expanders: Transform object tree into desired format
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

from sneakylang import Expander, expand

class ExpanderMap(dict):
    """Just wraps expander map into object """

class CzechtileExpander:
    """ Expander wrapper."""

    def expand_with_content(self, node, format, node_map, prefix=u'', suffix=u''):
        return u''.join([prefix] + [expand(child, format, node_map) for child in node.children] + [suffix])

class DocumentDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<?xml version="1.0" encoding="UTF-8"?>\n')

class DocumentXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="cs" lang="cs">', u'</html>')

class BookDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><book>', u'</book>')

class BookXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<body class="book">', u'</body>')

class ArticleDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><article>', u'</article>')

class ArticleXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<body class="article">', u'</body>')

class SekceDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<section>', u'</section>')

class SekceXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map)

class NadpisDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<title>', u'</title>')

class NadpisXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u''.join([u'<h', unicode(node.level), u'>']), u''.join([u'</h', unicode(node.level), u'>']))

class OdstavecDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<para>', u'</para>')

class OdstavecXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<p>', u'</p>')

class NeformatovanyTextDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<literallayout>', u'</literallayout>')

class NeformatovanyTextXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<pre>', u'</pre>')

#TODO: zesilene vs. silne v docbook

class SilneDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<emphasis role="bold">', u'</emphasis>')

class SilneXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<strong>', u'</strong>')

class ZvyrazneneDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<emphasis>', u'</emphasis>')

class ZvyrazneneXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<em>', u'</em>')

class HyperlinkDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u''.join([u'<ulink url="', unicode(node.link), u'">']), u'</ulink>')

class HyperlinkXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u''.join([u'<a href="', unicode(node.link), u'">']), u'</a>')

class TriTeckyEntity(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'&#8230;'

class PomlckaEntity(CzechtileExpander):
    def expand(self, node, format, node_map):
        if node.spojovnik:
            return u'&#173;'
        else:
            return u'&#8211;'

class UvodzovkyEntity(CzechtileExpander):
    def expand(self, node, format, node_map):
	    return self.expand_with_content(node, format, node_map, u'&#8222;', u'&#8220;')

class FootNoteDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'<footnote><para>', u'</para></footnote>')


class ListDocbook4(CzechtileExpander):

    types = {
        'itemized' : [u'itemizedlist', u''],
        '1-ordered' : [u'orderedlist', u' numeration="arabic"'],
        'A-ordered' : [u'orderedlist', u' numeration="loweralpha"'],
        'I-ordered' : [u'orderedlist', u' numeration="lowerroman"']
    }
    last_level = 0
    list_levels = [0]
    last_type = ''
    list_types = []

    def __init__(self):
        """Recover default values of some vars with new instance creating
        """
        self.__class__.list_levels = [0]


    def expand(self, node, format, node_map):

        res = u''.join([u'<', self.types[node.type_][0], self.types[node.type_][1], u'>'])
        for child in node.children:
            res = res + expand(child, format, node_map)

        if self.__class__.last_level != 0:
            for type_ in self.__class__.list_types[len(self.__class__.list_types) - self.__class__.last_level:]:
                res = u''.join([res, u'</', self.types[type_][0], u'>'])
        res = u''.join([res, u'</', self.types[node.type_][0], u'>'])
        return res

class ListItemDocbook4(CzechtileExpander):

    def expand(self, node, format, node_map):

        if ListDocbook4.list_levels != [0] and ListDocbook4.last_level == 0:
            ListDocbook4.list_levels = [0]

        if ListDocbook4.list_levels.count(node.level) == 0:
            ListDocbook4.list_levels.append(node.level)
            outer_list = u''.join([u'<', ListDocbook4.types[node.type_][0], ListDocbook4.types[node.type_][1], u'>'])
        else:
            outer_list = u''

        if ListDocbook4.list_levels.count(node.level + 1) != 0:
            outer_list = u''.join([u'</', ListDocbook4.types[ListDocbook4.last_type][0], u'>', outer_list])
        if node.level == 0 and ListDocbook4.list_levels != [0] and ListDocbook4.last_level > 1:
            outer_list = u''.join([u'</', ListDocbook4.types[ListDocbook4.last_type][0], u'>', outer_list])

        ListDocbook4.last_level = node.level
        ListDocbook4.last_type = node.type_
        ListDocbook4.list_types.append(node.type_)
        return self.expand_with_content(node, format, node_map, outer_list + u'<listitem>', u'</listitem>')

class ListXhtml11(ListDocbook4):
# inheriting __init__ function and last_*, list_* variables

    types = {
        'itemized' : ['ul', ''],
        '1-ordered' : ['ol', ' type="1"'],
        'A-ordered' : ['ol', ' type="a"'],
        'I-ordered' : ['ol', ' type="i"']
    }

    def expand(self, node, format, node_map):

        res = u''.join([u'<', self.types[node.type_][0], self.types[node.type_][1], u'>'])

        for child in node.children:
            res = res + expand(child, format, node_map)

        if self.__class__.last_level != 0:
            for type_ in self.__class__.list_types[len(self.__class__.list_types) - self.__class__.last_level:]:
                res = u''.join([res, u'</', self.types[type_][0], u'>'])
        res = u''.join([res, u'</', self.types[node.type_][0], u'>'])

        return res

class ListItemXhtml11(CzechtileExpander):

    def expand(self, node, format, node_map):
        if ListXhtml11.list_levels != [0] and ListXhtml11.last_level == 0:
            ListXhtml11.list_levels = [0]
        if ListXhtml11.list_levels.count(node.level) == 0:
            ListXhtml11.list_levels.append(node.level)
            outer_list = u''.join([u'<', ListXhtml11.types[node.type_][0], ListXhtml11.types[node.type_][1], u'>'])
        else:
            outer_list = u''

        if ListXhtml11.list_levels.count(node.level + 1) != 0:
            outer_list = u''.join([u'</', ListXhtml11.types[ListXhtml11.last_type][0], u'>']) + outer_list
        if node.level == 0 and ListXhtml11.list_levels != [0] and ListXhtml11.last_level > 1:
            outer_list = u''.join([u'</', ListXhtml11.types[ListXhtml11.last_type][0], u'>']) + outer_list

        ListXhtml11.last_level = node.level
        ListXhtml11.last_type = node.type_
        ListXhtml11.list_types.append(node.type_)
        return self.expand_with_content(node, format, node_map, outer_list + u'<li>', u'</li>')

class PevnaMedzeraEntity(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'&nbsp;'

