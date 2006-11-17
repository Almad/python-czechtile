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

class TestResult(OutputTestCase):

    def testBasicArticle(self):
        tree = parse('doc', registerMap)
        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('''<para>doc</para>''', res)

    def testBasicBook(self):
        tree = parse('doc', registerMap, parsers.Book)
        self.assertEquals(isinstance(tree.children[0], nodes.Book), True)
        res = expand(tree, 'docbook4', nodeMap)
        self.assertEquals(res, '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE book PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><book><para>doc</para></book>''')

if __name__ == "__main__":
    main()