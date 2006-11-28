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

#logging.basicConfig(level=logging.DEBUG)

class TestList(OutputTestCase):

    def testItemizedList(self):
        tree = parse('''\n\n - Polozka1\n - Polozka2\n\n''', registerMap)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'itemized')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')


    def testExpandedItemizedList(self):
        tree = parse('''\n\n - Polozka1\n - Polozka2\n\n''', registerMap)
        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('<itemizedlist><listitem>Polozka1</listitem><listitem>Polozka2</listitem></itemizedlist>', res)
        

    def testNumberOrderedList(self):
        tree = parse('''\n\n 1. Polozka1\n 1. Polozka2\n\n''', registerMap)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, '1-ordered')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')


    def testExpandedNumberOrderedList(self):
        tree = parse('''\n\n 1. Polozka1\n 1. Polozka2\n\n''', registerMap)
        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('<orderedlist numeration="arabic"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

        
    def testAlphaOrderedList(self):
        tree = parse('''\n\n a. Polozka1\n a. Polozka2\n\n''', registerMap)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'A-ordered')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')


    def testExpandedAlphaOrderedList(self):
        tree = parse('''\n\n a. Polozka1\n a. Polozka2\n\n''', registerMap)
        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('<orderedlist numeration="loweralpha"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

    def testRomanOrderedList(self):
        tree = parse('''\n\n i. Polozka1\n i. Polozka2\n\n''', registerMap)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'I-ordered')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')


    def testExpandedRomanOrderedList(self):
        tree = parse('''\n\n i. Polozka1\n i. Polozka2\n\n''', registerMap)
        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('<orderedlist numeration="lowerroman"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

if __name__ == "__main__":
    main()
