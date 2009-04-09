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

from sneakylang.expanders import expand, Expander, TextNodeExpander

class ExpanderMap(dict):
    """Just wraps expander map into object."""

class CzechtileExpander(Expander):
    """Expander wrapper."""

    def expand_with_content(self, node, format, node_map, prefix=u'', suffix=u''):
        return u''.join([prefix] + [expand(child, format, node_map) for child in node.children] + [suffix])

class EmptyExpander(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map)

class ListExpander(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map,
            u'<%(tag)s%(attrs)s>' % self.tag_map[node.token],
            u'</%(tag)s>' % self.tag_map[node.token])

class ListItemExpander(CzechtileExpander):
    def expand(self, node, format, node_map):
        return self.expand_with_content(node, format, node_map,
            u'<%(tag)s%(attrs)s>' % self.tag_map,
            u'</%(tag)s>' % self.tag_map)