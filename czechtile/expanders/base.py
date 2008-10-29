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

class ListExpander(CzechtileExpander):
    last_level = 0
    levels_list = [0]
    last_type = ''
    types_list = []

    tag_formats = {'start': u'<%s>', 'end': u'</%s>'}

    def expand(self, node, format, node_map):
        res = self.tag_formats['start'] % u' '.join(self.types[node.type_])
        for child in node.children:
            res = res + expand(child, format, node_map)

        if self.__class__.last_level != 0:
            for type_ in self.__class__.types_list[len(self.__class__.types_list) - self.__class__.last_level:]:
                res += self.tag_formats['end'] % self.types[type_][:1]

        res += self.tag_formats['end'] % self.types[node.type_][:1]
        return res

class ListItemExpander(CzechtileExpander):
    def __init__(self, *args, **kwargs):
        self.tag_formats = getattr(self, 'tag_formats', self.list_expander.tag_formats)

    def expand(self, node, format, node_map):
        if self.list_expander.levels_list != [0] and self.list_expander.last_level == 0:
            self.list_expander.levels_list = [0]

        outer_list = u''
        if self.list_expander.levels_list.count(node.level) == 0:
            self.list_expander.levels_list.append(node.level)
            outer_list = self.tag_formats['start'] % \
                    u' '.join(self.list_expander.types[node.type_])

        def prepend_list_end_regarding_last_type(list):
            return u''.join([self.tag_formats['end'] % \
                    self.list_expander.types[self.list_expander.last_type][:1], list])

        if self.list_expander.levels_list.count(node.level + 1) != 0:
            outer_list = prepend_list_end_regarding_last_type(outer_list)

        if node.level == 0 and self.list_expander.levels_list != [0] and \
                self.list_expander.last_level > 1:
            outer_list = prepend_list_end_regarding_last_type(outer_list)

        self.list_expander.last_level = node.level
        self.list_expander.last_type = node.type_
        self.list_expander.types_list.append(node.type_)
        return self.expand_with_content(node, format, node_map,
                u''.join([outer_list, self.tag_formats['start'] % self.tag]),
                self.tag_formats['end'] % self.tag[:1])

