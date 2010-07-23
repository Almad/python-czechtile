#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Test nahrazovani na peknou ceskou typografii
"""

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

class TestCzechTypos(OutputTestCase):

    def testTriTecky(self):
        tree = parse('''Typo hezky cesky...''', register_map)
        result = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para>Typo hezky cesky&#8230;</para>''', result)

        result = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p>Typo hezky cesky&#8230;</p>''', result)

    def testPomlcka(self):
        tree = parse('''Typo - hezky-cesky -''', register_map)
        result = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para>Typo&nbsp;&#8211;&nbsp;hezky-cesky&nbsp;&#8211;</para>''', result)

        result = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p>Typo&nbsp;&#8211;&nbsp;hezky-cesky&nbsp;&#8211;</p>''', result)


    def testUvodzovky(self):
        tree = parse('''"Uvodzovkujem"''', register_map)
        result = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para>&#8222;Uvodzovkujem&#8220;</para>''', result)

        result = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p>&#8222;Uvodzovkujem&#8220;</p>''', result)

    def testNovyRadek(self):
        tree = parse('''A
B
C''', register_map)

        result = expand(tree, 'docbook4', expander_map)
        result = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p>A<br />B<br />C</p>''', result)

if __name__ == "__main__":
    main()
