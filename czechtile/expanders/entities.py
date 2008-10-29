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

from czechtile.expanders.base import CzechtileExpander

class TriTecky(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'&#8230;'

class Pomlcka(CzechtileExpander):
    def expand(self, node, format, node_map):
        if node.spojovnik:
            return u'-'
        else:
            return u'&#8211;'

class PevnaMedzera(CzechtileExpander):
    def expand(self, node, format, node_map):
        return u'&nbsp;'

class Uvodzovky(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map, u'&#8222;', u'&#8220;')

