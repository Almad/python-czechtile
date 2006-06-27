#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test wiki engine transformation """

###
#Czechtile: Wiki for Czech users
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
from tempfile import mkstemp
from os.path import join
import sys
sys.path.insert(0, join(pardir, pardir))
import logging

from unittest import main,TestCase

from czechtile import transform

class TestEasyWikiHtml(TestCase):
    """ Test easy and uncomplicated replacement cases
    """

    def testHeadings(self):
        assert transform('= Nadpis druhé úrovně =') == '<h2>Nadpis druhé úrovně</h2>'
        assert transform('== Nadpis druhé úrovně ==') == '<h3>Nadpis druhé úrovně</h3>'
        assert transform('=== Nadpis druhé úrovně ===') == '<h4>Nadpis druhé úrovně</h4>'

    def testStrong(self):
        assert transform('**bold**') == '<strong>bold</strong>'

    def testOrderedList(self):
        s = '''1. jedna
1. dva
1. tri'''
        exp = '''<ol>
<li>jedna</li>
<li>dva</li>
<li>tri</li>
</ol>'''
        assert transform(s) == exp


    def testUnorderedList(self):
        s = ''' - jedna
 - dva
 - tri'''
        exp = '''<ul>
<li>jedna</li>
<li>dva</li>
<li>tri</li>
</ul>'''
        assert transform(s) == exp

    def testNestedLists(self):
        s = '''1. jedna
1. dva
  - dva jedna
  - dva dva
1. tri'''
        exp = '''<ol>
<li>jedna</li>
<li>dva</li>
<ul>
<li>dva jedna</li>
<li>dva dva</li>
</ul>
<li>tri</li>
</ol>'''
        assert transform(s) == exp

    def testUntouchedQuirks(self):
        """ Test quicks: some things similar to WikiSyntax, but should be leaved untouched instaead """
        s = '''- jedna
- dva
- tri'''
        assert transform(s) == s, 'This list have no space on beggining of the line, should be leaved untouched'

        s = '''1. jedna
1. dva
 - dva jedna
 - dva dva
1. tri'''
        exp = '''<ol>
<li>jedna</li>
<li>dva</li>
</ol>
<ul>
<li>dva jedna</li>
<li>dva dva</li>
</ul>
<ol>
<li>tri</li>
</ol>'''
        assert transform(s) == exp, 'Only one space on beginning, so unordered list is not nested'

if __name__ == "__main__":
    main()