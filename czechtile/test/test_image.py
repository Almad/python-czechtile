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

class TestImages(OutputTestCase):
    def testBasicImage(self):
        tree = parse('''((obrazek http://rpgplanet.cz/images/logo.png))''', register_map)
        self.assertEquals(tree.children[0].__class__, nodes.Article)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Obrazek)
        self.assertEquals(tree.children[0].children[0].source, 'http://rpgplanet.cz/images/logo.png')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('<mediaobject><imageobject><imagedata fileref="http://rpgplanet.cz/images/logo.png" /></imageobject></mediaobject>', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('<img src="http://rpgplanet.cz/images/logo.png" />', res)
        
if __name__ == "__main__":
    main() 
