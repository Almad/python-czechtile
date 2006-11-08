# -*- coding: utf-8 -*-

""" Expanders
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

class DocumentDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<?xml version="1.0" encoding="UTF-8"?>\n'] + [expand(child, format, node_map) for child in node.children])

class BookDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['''<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN"
    "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><book>'''] + [expand(child, format, node_map) for child in node.children] + ['</book>'])

class ArticleDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['''<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN"
    "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><article>'''] + [expand(child, format, node_map) for child in node.children] + ['</article>'])

class SekceDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<section>'] + [expand(child, format, node_map) for child in node.children] + ['</section>'])

class NadpisDocbook4(Expander):
    def expand(self, level, node, format, node_map):
        return ''.join(['<title>'] + [expand(child, format, node_map) for child in node.children] + ['</title>'])

class OdstavecDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<para>'] + [expand(child, format, node_map) for child in node.children] + ['</para>'])

#TODO: zesilene vs. silne v docbook

class SilneDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<emphasis role="bold">'] + [expand(child, format, node_map) for child in node.children] + ['</emphasis>'])

class ZvyrazneneDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<emphasis>'] + [expand(child, format, node_map) for child in node.children] + ['</emphasis>'])

class HyperlinkDocbook4(Expander):
    def expand(self, node, format, node_map):
        return ''.join(['<ulink url="', node.link, '">'] + [expand(child, format, node_map) for child in node.children] + ['</ulink>'])

class TriTeckyDocbook4(Expander):
    def expand(self, node, format, node_map):
        return '&#8230'