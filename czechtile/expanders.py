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

    def expand_with_content(self, node, format, node_map, prefix='', suffix=''):
        return ''.join([str(prefix)] + [expand(child, format, node_map) for child in node.children] + [str(suffix)])

class DocumentDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<?xml version="1.0" encoding="UTF-8"?>\n')

class DocumentXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="cs" lang="cs">', '</html>')

class BookDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><book>', '</book>')

class BookXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<body class="book">', '</body>')

class ArticleDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><article>', '</article>')

class ArticleXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<body class="article">', '</body>')

class SekceDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<section>', '</section>')

class SekceXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map)

class NadpisDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<title>', '</title>')

class NadpisXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, ''.join(['<h', str(node.level), '>']), ''.join(['</h', str(node.level), '>']))

class OdstavecDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<para>', '</para>')

class OdstavecXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<p>', '</p>')

class NeformatovanyTextDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<literallayout>', '</literallayout>')

class NeformatovanyTextXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<pre>', '</pre>')

#TODO: zesilene vs. silne v docbook

class SilneDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<emphasis role="bold">', '</emphasis>')

class SilneXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<strong>', '</strong>')

class ZvyrazneneDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<emphasis>', '</emphasis>')

class ZvyrazneneXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, '<em>', '</em>')

class HyperlinkDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, ''.join(['<ulink url="', node.link, '">']), '</ulink>')

class HyperlinkXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, ''.join(['<a href="', node.link, '">']), '</a>')

class TriTeckyEntity(CzechtileExpander):
    def expand(self, node, format, node_map):
        return '&#8230;'


last_level = 0
list_levels = [0]
last_type = ''
list_types = []

class ListDocbook4(CzechtileExpander):
    types = {
        'itemized' : ['itemizedlist', ''],
        '1-ordered' : ['orderedlist', ' numeration="arabic"'],
        'A-ordered' : ['orderedlist', ' numeration="loweralpha"'],
        'I-ordered' : ['orderedlist', ' numeration="lowerroman"']
    }
    def expand(self, node, format, node_map):
        global list_levels
        global last_level
        global list_types
        if list_levels != [0]:
            list_levels = [0]
        if last_level != 0:
            last_level = 0
        res = ''.join(['<', self.types[node.type_][0], self.types[node.type_][1], '>'])
        for child in node.children:
            res = res + expand(child, format, node_map)
        if last_level != 0:
            for type_ in list_types[len(list_types)-last_level:]:
                res = res + ''.join(['</', self.types[type_][0], '>'])
        res = res + ''.join(['</', self.types[node.type_][0], '>'])
        return res

class ListItemDocbook4(CzechtileExpander):
    def expand(self, node, format, node_map):
        global last_level
        global list_levels
        global last_type
        global list_types
        if list_levels != [0] and last_level == 0:
            list_levels = [0]
        if list_levels.count(node.level) == 0:
            list_levels.append(node.level)
            outer_list = ''.join(['<', ListDocbook4.types[node.type_][0], ListDocbook4.types[node.type_][1], '>'])
        else:
            outer_list = ''
        if list_levels.count(node.level + 1) != 0:
            outer_list = ''.join(['</', ListDocbook4.types[last_type][0], '>']) + outer_list
        if node.level == 0 and list_levels != [0] and last_level > 1:
            outer_list = ''.join(['</', ListDocbook4.types[last_type][0], '>']) + outer_list
        last_level = node.level
        last_type = node.type_
        list_types.append(node.type_)
        return self.expand_with_content(node, format, node_map, outer_list + '<listitem>', '</listitem>')

class ListXhtml11(CzechtileExpander):
    types = {
        'itemized' : ['ul', ''],
        '1-ordered' : ['ol', ' type="1"'],
        'A-ordered' : ['ol', ' type="a"'],
        'I-ordered' : ['ol', ' type="i"']
    }
    def expand(self, node, format, node_map):
        global list_levels
        global last_level
        global list_types
        if list_levels != [0]:
            list_levels = [0]
        if last_level != 0:
            last_level = 0
        if list_types != []:
            list_types = []
        res = ''.join(['<', self.types[node.type_][0], self.types[node.type_][1], '>'])
        for child in node.children:
            res = res + expand(child, format, node_map)
        if last_level != 0:
            for type_ in list_types[len(list_types)-last_level:]:
                res = res + ''.join(['</', self.types[type_][0], '>'])
        res = res + ''.join(['</', self.types[node.type_][0], '>'])
        return res

class ListItemXhtml11(CzechtileExpander):
    def expand(self, node, format, node_map):
        global last_level
        global list_levels
        global last_type
        global list_types
        if list_levels != [0] and last_level == 0:
            list_levels = [0]
        if list_levels.count(node.level) == 0:
            list_levels.append(node.level)
            outer_list = ''.join(['<', ListXhtml11.types[node.type_][0], ListXhtml11.types[node.type_][1], '>'])
        else:
            outer_list = ''
        if list_levels.count(node.level + 1) != 0:
            outer_list = ''.join(['</', ListXhtml11.types[last_type][0], '>']) + outer_list
        if node.level == 0 and list_levels != [0] and last_level > 1:
            outer_list = ''.join(['</', ListXhtml11.types[last_type][0], '>']) + outer_list
        last_level = node.level
        last_type = node.type_
        list_types.append(node.type_)
        return self.expand_with_content(node, format, node_map, outer_list + '<li>', '</li>')
