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
import logging as pylog

from unittest import main
from czechtile import *

from module_test import *

#pylog.basicConfig(level=pylog.DEBUG)

class TestBasicLists(OutputTestCase):

    def testItemizedList(self):
        tree = parse('''\n - Polozka1\n - Polozka2\n\n''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'itemized')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka1</listitem><listitem>Polozka2</listitem></itemizedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka1</li><li>Polozka2</li></ul>', res)


    def testNumberOrderedList(self):
        tree = parse('''\n 1. Polozka1\n 1. Polozka2\n\n''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, '1-ordered')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')


        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<orderedlist numeration="arabic"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ol type="1"><li>Polozka1</li><li>Polozka2</li></ol>', res)


    def testAlphaOrderedList(self):
        tree = parse('''\n a. Polozka1\n a. Polozka2\n\n''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'A-ordered')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')


        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<orderedlist numeration="loweralpha"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ol type="a"><li>Polozka1</li><li>Polozka2</li></ol>', res)

    def testRomanOrderedList(self):
        tree = parse('''\n i. Polozka1\n i. Polozka2\n\n''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'I-ordered')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')


        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<orderedlist numeration="lowerroman"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ol type="i"><li>Polozka1</li><li>Polozka2</li></ol>', res)

class TestSublists(OutputTestCase):

    def testEarlierEndingSublist(self):
        tree = parse('''\n - Polozka1\n  - VnorenaPolozka1\n  - VnorenaPolozka2\n   - DvojitoVnorenaPolozka1\n - Polozka2\n\n''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'itemized')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].level, 0)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].level, 1)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'VnorenaPolozka1')
        self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[2].level, 1)
        self.assertEquals(tree.children[0].children[0].children[2].children[0].content, 'VnorenaPolozka2')
        self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[3].level, 2)
        self.assertEquals(tree.children[0].children[0].children[3].children[0].content, 'DvojitoVnorenaPolozka1')
        self.assertEquals(tree.children[0].children[0].children[4].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[4].level, 0)
        self.assertEquals(tree.children[0].children[0].children[4].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka1</listitem><itemizedlist><listitem>VnorenaPolozka1</listitem><listitem>VnorenaPolozka2</listitem><itemizedlist><listitem>DvojitoVnorenaPolozka1</listitem></itemizedlist></itemizedlist><listitem>Polozka2</listitem></itemizedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka1</li><ul><li>VnorenaPolozka1</li><li>VnorenaPolozka2</li><ul><li>DvojitoVnorenaPolozka1</li></ul></ul><li>Polozka2</li></ul>', res)
        
    def testSimpleSublist(self):
        tree = parse('''\n - Polozka prva\n  - Polozka vnorena prva\n  - Polozka vnorena druha\n - Polozka druha\n\n''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'itemized')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].level, 0)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka prva')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].level, 1)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka vnorena prva')
        self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[2].level, 1)
        self.assertEquals(tree.children[0].children[0].children[2].children[0].content, 'Polozka vnorena druha')
        self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[3].level, 0)
        self.assertEquals(tree.children[0].children[0].children[3].children[0].content, 'Polozka druha')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka prva</listitem><itemizedlist><listitem>Polozka vnorena prva</listitem><listitem>Polozka vnorena druha</listitem></itemizedlist><listitem>Polozka druha</listitem></itemizedlist>', res)
        
        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka prva</li><ul><li>Polozka vnorena prva</li><li>Polozka vnorena druha</li></ul><li>Polozka druha</li></ul>', res)
        
    def testDoubleSublist(self):
        tree = parse('''\n - Polozka1\n  - VnorenaPolozka1\n  - VnorenaPolozka2\n   - DvojitoVnorenaPolozka1\n  - VnorenaPolozka3\n - Polozka2\n\n''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'itemized')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].level, 0)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].level, 1)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'VnorenaPolozka1')
        self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[2].level, 1)
        self.assertEquals(tree.children[0].children[0].children[2].children[0].content, 'VnorenaPolozka2')
        self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[3].level, 2)
        self.assertEquals(tree.children[0].children[0].children[3].children[0].content, 'DvojitoVnorenaPolozka1')
        self.assertEquals(tree.children[0].children[0].children[4].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[4].level, 1)
        self.assertEquals(tree.children[0].children[0].children[4].children[0].content, 'VnorenaPolozka3')
        self.assertEquals(tree.children[0].children[0].children[5].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[5].level, 0)
        self.assertEquals(tree.children[0].children[0].children[5].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka1</listitem><itemizedlist><listitem>VnorenaPolozka1</listitem><listitem>VnorenaPolozka2</listitem><itemizedlist><listitem>DvojitoVnorenaPolozka1</listitem></itemizedlist><listitem>VnorenaPolozka3</listitem></itemizedlist><listitem>Polozka2</listitem></itemizedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka1</li><ul><li>VnorenaPolozka1</li><li>VnorenaPolozka2</li><ul><li>DvojitoVnorenaPolozka1</li></ul><li>VnorenaPolozka3</li></ul><li>Polozka2</li></ul>', res)
        
    def testMultiTypeSublist(self):
        tree = parse('''\n - Polozka prva\n  i. Polozka vnorena prva\n  i. Polozka vnorena druha\n - Polozka druha\n\n''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'itemized')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].level, 0)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka prva')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].level, 1)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka vnorena prva')
        self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[2].level, 1)
        self.assertEquals(tree.children[0].children[0].children[2].children[0].content, 'Polozka vnorena druha')
        self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[3].level, 0)
        self.assertEquals(tree.children[0].children[0].children[3].children[0].content, 'Polozka druha')

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka prva</li><ol type="i"><li>Polozka vnorena prva</li><li>Polozka vnorena druha</li></ol><li>Polozka druha</li></ul>', res)

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka prva</listitem><orderedlist numeration="lowerroman"><listitem>Polozka vnorena prva</listitem><listitem>Polozka vnorena druha</listitem></orderedlist><listitem>Polozka druha</listitem></itemizedlist>', res)

class TestSpecialCases(OutputTestCase):

    def testLeaveDocumentToContinue(self):
        tree = parse('''\n i. Polozka1\n i. Polozka2\n\nNormalni odstavec''', register_map)

        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].type_, 'I-ordered')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, 'Normalni odstavec')

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ol type="i"><li>Polozka1</li><li>Polozka2</li></ol><p>Normalni odstavec</p>', res)
        
    def testIfDashIsNotParseredAsList(self): # it is not very nice name for test function ;)
        tree = parse('''jeden - dva tri-styri''', register_map)

        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'jeden - dva tri-styri')
        
    def testIfDashInIsNotParseredAsList2(self):
        # in this test we are finding out if dash is not parsered as list in listitem too
        tree = parse('''\n - jeden - dva tri-styri\n\n''', register_map)

        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'jeden - dva tri-styri')

    def testListAtEOF(self):
        tree = parse('''\n - jeden\n - dva''', register_map)

        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'jeden')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'dva')

    def testListAtBOF(self):
        tree = parse(''' - jeden\n - dva\n\n''', register_map)

        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'jeden')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'dva')


    def testListAtBOFAndAtEOF(self):
        tree = parse(''' - jeden\n - dva''', register_map)

        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'jeden')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'dva')


if __name__ == "__main__":
    main()
