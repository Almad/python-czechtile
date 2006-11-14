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
        return self.expand_with_content(node,format, node_map, '<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><book>', '</book>')

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
        return '&#8230'
        
class ListDocbook4(Expander):
    def expand(self, type_, node, format, node_map):
        return ''.join(['<itemizedlist>'] + [expand(child, format, node_map) for child in node.children] + ['</itemizedList>'])

class ListItemDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<listitem>'] + [expand(child, format, node_map) for child in node.children] + ['</listitem>'])
