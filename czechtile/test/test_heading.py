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

from unittest import main,TestCase
from czechtile import *

from module_test import *
#logging.basicConfig(level=logging.DEBUG)

class TestHeadings(OutputTestCase):

    def _testTree(self, tree):
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'Nadpis')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, 'Odstavec')

    def testSimplest(self):
        tree = parse('''= Nadpis =\n\nOdstavec\n\n''', register_map)
        self._testTree(tree)

        result = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<title>Nadpis</title><para>Odstavec</para>', result)

        result = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<h1>Nadpis</h1><p>Odstavec</p>', result)

#    def testTight(self):
#        tree = parse('''=Nadpis=\n\nOdstavec\n\n''', register_map)
#        self._testTree(tree)

    def testSimplest(self):
        tree = parse('''= Nadpis =\n\nOdstavec\n\n''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'Nadpis')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, 'Odstavec')

        result = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<title>Nadpis</title><para>Odstavec</para>', result)

        result = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<h1>Nadpis</h1><p>Odstavec</p>', result)

    def testTwolevel(self):
        tree = parse('= Nadpis =\nOdstavec\n== NadpisDva ==\nOdstavec', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'Nadpis')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, 'Odstavec')
 #       self.assertEquals(tree.children[0].children[2].__class__, nodes.Sekce)

        result = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<h1>Nadpis</h1><p>Odstavec</p><h2>NadpisDva</h2><p>Odstavec</p>', result)


if __name__ == "__main__":
    main()