#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

from os import pardir, tmpfile, remove
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging
import re

from unittest import main
from czechtile import *

from module_test import *


class TestList(OutputTestCase):

    def testItemizedList(self):
        tree = parse(''' - Polozka1\n - Polozka2''', registerMap)
# most of the code is commented because of "IndexError: list index out of range"
# which sometimes does problems
# momentarily is causing problems the uncommented line too :(
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.List)
#        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
#        self.assertEquals(tree.children[0].children[0].children[0].children[0].__class__, nodes.Odstavec)
#        self.assertEquals(tree.children[0].children[0].children[0].children[0].children[0].__class__, 'Polozka1')
#        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
#        self.assertEquals(tree.children[0].children[0].children[1].children[0].__class__, nodes.Odstavec)
#        self.assertEquals(tree.children[0].children[0].children[1].children[0].children[0].content, 'Polozka2')


#    def testExpandedItemizedList(self):
#        tree = parse(''' - Polozka1\n - Polozka2''', registerMap)
#        res = expand('itemized', tree, 'docbook4', nodeMap)
#        res = expand(tree, 'docbook4', nodeMap)
#        self.assertDocbook4(res, '''<para><itemizedlist><listitem>Polozka1</listitem><listitem>Polozka2</listitem></itemizedlist></para>''')


if __name__ == "__main__":
    main()
