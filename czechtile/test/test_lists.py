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
#pylog.basicConfig(level=pylog.DEBUG)

from unittest import main
from czechtile import *

from module_test import *

class TestBasicLists(OutputTestCase):

    def testItemizedList(self):
        tree = parse('''\n - Polozka1\n - Polozka2''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].token, '-')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka1</listitem><listitem>Polozka2</listitem></itemizedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka1</li><li>Polozka2</li></ul>', res)

        res = expand(tree, 'mediawiki', expander_map)
        self.assertMediawiki('\n* Polozka1\n* Polozka2\n', res)

    def testNumberOrderedList(self):
        tree = parse('''\n 1. Polozka1\n 1. Polozka2''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].token, '1.')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<orderedlist numeration="arabic"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ol type="1"><li>Polozka1</li><li>Polozka2</li></ol>', res)

        res = expand(tree, 'mediawiki', expander_map)
        self.assertMediawiki('\n# Polozka1\n# Polozka2\n', res)

    def testAlphaOrderedList(self):
        tree = parse('''\n a. Polozka1\n a. Polozka2''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].token, 'a.')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<orderedlist numeration="loweralpha"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ol type="a"><li>Polozka1</li><li>Polozka2</li></ol>', res)

        res = expand(tree, 'mediawiki', expander_map)
        self.assertMediawiki('\n# Polozka1\n# Polozka2\n', res)

    def testRomanOrderedList(self):
        tree = parse('''\n i. Polozka1\n i. Polozka2''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].token, 'i.')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<orderedlist numeration="lowerroman"><listitem>Polozka1</listitem><listitem>Polozka2</listitem></orderedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ol type="i"><li>Polozka1</li><li>Polozka2</li></ol>', res)

        res = expand(tree, 'mediawiki', expander_map)
        self.assertMediawiki('\n# Polozka1\n# Polozka2\n', res)

class TestSublists(OutputTestCase):

    def testEarlierEndingSublist(self):
        tree = parse('''\n - Polozka1\n  - VnorenaPolozka1\n  - VnorenaPolozka2\n   - DvojitoVnorenaPolozka1\n - Polozka2''', register_map)
        #self.assertEquals(tree.children[0].__class__, nodes.Article)
        #self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        #self.assertEquals(tree.children[0].children[0].token, '-')
        #self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        #self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'VnorenaPolozka1')
        #self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[2].children[0].content, 'VnorenaPolozka2')
        #self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[3].children[0].content, 'DvojitoVnorenaPolozka1')
        #self.assertEquals(tree.children[0].children[0].children[4].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[4].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka1</listitem><itemizedlist><listitem>VnorenaPolozka1</listitem><listitem>VnorenaPolozka2</listitem><itemizedlist><listitem>DvojitoVnorenaPolozka1</listitem></itemizedlist></itemizedlist><listitem>Polozka2</listitem></itemizedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka1</li><ul><li>VnorenaPolozka1</li><li>VnorenaPolozka2</li><ul><li>DvojitoVnorenaPolozka1</li></ul></ul><li>Polozka2</li></ul>', res)

        res = expand(tree, 'mediawiki', expander_map)
        self.assertMediawiki('''\n* Polozka1\n** VnorenaPolozka1\n** VnorenaPolozka2\n*** DvojitoVnorenaPolozka1\n* Polozka2\n''', res)
        
    def testSimpleSublist(self):
        tree = parse('''\n - Polozka prva\n  - Polozka vnorena prva\n  - Polozka vnorena druha\n - Polozka druha''', register_map)
        #self.assertEquals(tree.children[0].__class__, nodes.Article)
        #self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        #self.assertEquals(tree.children[0].children[0].token, '-')
        #self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka prva')
        #self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka vnorena prva')
        #self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[2].children[0].content, 'Polozka vnorena druha')
        #self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[3].children[0].content, 'Polozka druha')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka prva</listitem><itemizedlist><listitem>Polozka vnorena prva</listitem><listitem>Polozka vnorena druha</listitem></itemizedlist><listitem>Polozka druha</listitem></itemizedlist>', res)
        
        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka prva</li><ul><li>Polozka vnorena prva</li><li>Polozka vnorena druha</li></ul><li>Polozka druha</li></ul>', res)
        
    def testDoubleSublist(self):
        tree = parse('''\n - Polozka1\n  - VnorenaPolozka1\n  - VnorenaPolozka2\n   - DvojitoVnorenaPolozka1\n  - VnorenaPolozka3\n - Polozka2''', register_map)
        #self.assertEquals(tree.children[0].__class__, nodes.Article)
        #self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        #self.assertEquals(tree.children[0].children[0].token, '-')
        #self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        #self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'VnorenaPolozka1')
        #self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[2].children[0].content, 'VnorenaPolozka2')
        #self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[3].children[0].content, 'DvojitoVnorenaPolozka1')
        #self.assertEquals(tree.children[0].children[0].children[4].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[4].children[0].content, 'VnorenaPolozka3')
        #self.assertEquals(tree.children[0].children[0].children[5].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[5].children[0].content, 'Polozka2')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka1</listitem><itemizedlist><listitem>VnorenaPolozka1</listitem><listitem>VnorenaPolozka2</listitem><itemizedlist><listitem>DvojitoVnorenaPolozka1</listitem></itemizedlist><listitem>VnorenaPolozka3</listitem></itemizedlist><listitem>Polozka2</listitem></itemizedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka1</li><ul><li>VnorenaPolozka1</li><li>VnorenaPolozka2</li><ul><li>DvojitoVnorenaPolozka1</li></ul><li>VnorenaPolozka3</li></ul><li>Polozka2</li></ul>', res)
        
    def testMultiTypeSublist(self):
        tree = parse('''\n - Polozka prva\n  i. Polozka vnorena prva\n  i. Polozka vnorena druha\n - Polozka druha''', register_map)
        #self.assertEquals(tree.children[0].__class__, nodes.Article)
        #self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        #self.assertEquals(tree.children[0].children[0].token, '-')
        #self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka prva')
        #self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka vnorena prva')
        #self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[2].children[0].content, 'Polozka vnorena druha')
        #self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.ListItem)
        #self.assertEquals(tree.children[0].children[0].children[3].children[0].content, 'Polozka druha')

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ul><li>Polozka prva</li><ol type="i"><li>Polozka vnorena prva</li><li>Polozka vnorena druha</li></ol><li>Polozka druha</li></ul>', res)

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<itemizedlist><listitem>Polozka prva</listitem><orderedlist numeration="lowerroman"><listitem>Polozka vnorena prva</listitem><listitem>Polozka vnorena druha</listitem></orderedlist><listitem>Polozka druha</listitem></itemizedlist>', res)

class TestSpecialCases(OutputTestCase):

    def testLeaveDocumentToContinue(self):
        tree = parse('''\n i. Polozka1\n i. Polozka2\n\nNormalni odstavec''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].token, 'i.')
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Polozka1')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'Polozka2')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, 'Normalni odstavec')

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<ol type="i"><li>Polozka1</li><li>Polozka2</li></ol><p>Normalni odstavec</p>', res)
        
    def testDash(self): # tests if dash is not parsered as list
        tree = parse('''jeden - dva tri-styri''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'jeden')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.PevnaMedzera)
        self.assertEquals(tree.children[0].children[0].children[2].__class__, nodes.Pomlcka)
        self.assertEquals(tree.children[0].children[0].children[3].__class__, nodes.PevnaMedzera)
        self.assertEquals(tree.children[0].children[0].children[4].content, 'dva tri')
        self.assertEquals(tree.children[0].children[0].children[5].__class__, nodes.Pomlcka)
        self.assertEquals(tree.children[0].children[0].children[6].content, 'styri')
        
    def testDashInListItem(self):
        tree = parse('''\n - jeden - dva tri-styri''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'jeden')
        self.assertEquals(tree.children[0].children[0].children[0].children[1].__class__, nodes.PevnaMedzera)
        self.assertEquals(tree.children[0].children[0].children[0].children[2].__class__, nodes.Pomlcka)
        self.assertEquals(tree.children[0].children[0].children[0].children[3].__class__, nodes.PevnaMedzera)
        self.assertEquals(tree.children[0].children[0].children[0].children[4].content, 'dva tri')
        self.assertEquals(tree.children[0].children[0].children[0].children[5].__class__, nodes.Pomlcka)
        self.assertEquals(tree.children[0].children[0].children[0].children[6].content, 'styri')

    def testListAtEOF(self):
        tree = parse('''\n - jeden\n - dva''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'jeden')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'dva')

    def testListAtBOF(self):
        tree = parse(''' - jeden\n - dva''', register_map)
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


class TestStandardUsage(OutputTestCase):

    def testZoznamPodNadpisom(self):
        text = '''= nadpis =
 - seznam1
 - seznam2'''

        tree = parse(text, register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'nadpis')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[1].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[1].children[0].children[0].content, 'seznam1')
        self.assertEquals(tree.children[0].children[1].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[1].children[1].children[0].content, 'seznam2')

    def testZoznamPodNadpisomSTextom(self):
        text = '''= nadpis =
Ahooj - ludia..
 1. seznam1
 1. seznam2

CzechTile ruleez.'''

        tree = parse(text, register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'nadpis')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, 'Ahooj')
        self.assertEquals(tree.children[0].children[1].children[1].__class__, nodes.PevnaMedzera)
        self.assertEquals(tree.children[0].children[1].children[2].__class__, nodes.Pomlcka)
        self.assertEquals(tree.children[0].children[1].children[3].__class__, nodes.PevnaMedzera)
        self.assertEquals(tree.children[0].children[1].children[4].content, 'ludia..')
        self.assertEquals(tree.children[0].children[2].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[2].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[2].children[0].children[0].content, 'seznam1')
        self.assertEquals(tree.children[0].children[2].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[2].children[1].children[0].content, 'seznam2')
        self.assertEquals(tree.children[0].children[3].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[3].children[0].content, 'CzechTile ruleez.')

    def testZoznamNaKonciPodNadpisomSTextom(self):
        text = '''= nadpis =
Ahooj, ludia..

 - seznam1
 - seznam2'''

        tree = parse(text, register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'nadpis')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, u'Ahooj, ludia..')
        self.assertEquals(tree.children[0].children[2].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[2].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[2].children[0].children[0].content, 'seznam1')
        self.assertEquals(tree.children[0].children[2].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[2].children[1].children[0].content, 'seznam2')

    def testZoznamBezMedzery(self):
        text = '''= nadpis =
Ahooj - ludia..
1. seznam1
1. seznam2

CzechTile ruleez.

- xyz
 - abc
- dfj'''

        tree = parse(text, register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'nadpis')
        self.assertEquals(tree.children[0].children[1].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[1].children[0].content, 'Ahooj')
        self.assertEquals(tree.children[0].children[1].children[1].__class__, nodes.PevnaMedzera)
        self.assertEquals(tree.children[0].children[1].children[2].__class__, nodes.Pomlcka)
        self.assertEquals(tree.children[0].children[1].children[3].__class__, nodes.PevnaMedzera)
        self.assertEquals(tree.children[0].children[1].children[4].content, 'ludia..')
        self.assertEquals(tree.children[0].children[2].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[2].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[2].children[0].children[0].content, 'seznam1')
        self.assertEquals(tree.children[0].children[2].children[1].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[2].children[1].children[0].content, 'seznam2')
        self.assertEquals(tree.children[0].children[3].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[3].children[0].content, 'CzechTile ruleez.')
        self.assertEquals(tree.children[0].children[4].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[4].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[4].children[0].children[0].content, 'xyz')
        self.assertEquals(tree.children[0].children[4].children[1].__class__, nodes.List)
        self.assertEquals(tree.children[0].children[4].children[1].token, '-')
        self.assertEquals(tree.children[0].children[4].children[1].children[0].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[4].children[1].children[0].children[0].content, 'abc')
        self.assertEquals(tree.children[0].children[4].children[2].__class__, nodes.ListItem)
        self.assertEquals(tree.children[0].children[4].children[2].children[0].content, 'dfj')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<title>nadpis</title><para>Ahooj&nbsp;&#8211;&nbsp;ludia..</para><orderedlist numeration="arabic"><listitem>seznam1</listitem><listitem>seznam2</listitem></orderedlist><para>CzechTile ruleez.</para><itemizedlist><listitem>xyz</listitem><itemizedlist><listitem>abc</listitem></itemizedlist><listitem>dfj</listitem></itemizedlist>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<h1>nadpis</h1><p>Ahooj&nbsp;&#8211;&nbsp;ludia..</p><ol type="1"><li>seznam1</li><li>seznam2</li></ol><p>CzechTile ruleez.</p><ul><li>xyz</li><ul><li>abc</li></ul><li>dfj</li></ul>', res)

if __name__ == "__main__":
    main()
