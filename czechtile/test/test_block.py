#!/usr/bin/env python
# -*- coding: utf-8 -*-

###
#Czechtile: WikiHezkyCesky
#Copyright (C) 2007 Lukas "Almad" Linhart http://www.almad.net/
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

from unittest import main, TestCase
from czechtile import *

from module_test import *
#logging.basicConfig(level=logging.DEBUG)

class TestParagraphRegression(OutputTestCase):

    def testMultipleParas(self):
        tree = parse('''= Nadpis =
Para 1

Para 2

Para 3

== Heading 2 ==
Para 4
''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'Nadpis')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, 'Para 1')
        self.assertEquals(tree.children[0].children[2].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[2].children[0].content, 'Para 2')
        self.assertEquals(tree.children[0].children[3].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[3].children[0].content, 'Para 3')
        self.assertEquals(tree.children[0].children[4].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[4].children[0].content, 'Heading 2')
        self.assertEquals(tree.children[0].children[5].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[5].children[0].content, 'Para 4')
        self.assertEquals(6, len(tree.children[0].children))

if __name__ == "__main__":
    main()
