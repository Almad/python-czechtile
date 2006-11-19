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

from unittest import main, TestCase
from czechtile import *

from module_test import *
#logging.basicConfig(level=logging.DEBUG)

class TestSilne(OutputTestCase):

    def testSilne(self):
        tree = parse('''"""silne"""''', registerMap)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Silne)

        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('''<para><emphasis role="bold">silne</emphasis></para>''', res)

        res = expand(tree, 'xhtml11', nodeMap)
        self.assertXhtml('''<p><strong>silne</strong></p>''', res)

class TestZvyraznene(OutputTestCase):
    def testZvyraznene(self):
        tree = parse('''""zvyraznene""''', registerMap)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Zvyraznene)

        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('''<para><emphasis>zvyraznene</emphasis></para>''', res)

        res = expand(tree, 'xhtml11', nodeMap)
        self.assertXhtml('''<p><em>zvyraznene</em></p>''', res)

class TestOdkaz(OutputTestCase):
    def testOdkazEasyNahrazovani(self):
        tree = parse('''http://rpgplanet.cz''', registerMap)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Hyperlink)

        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('''<para><ulink url="http://rpgplanet.cz">http://rpgplanet.cz</ulink></para>''', res)

        res = expand(tree, 'xhtml11', nodeMap)
        self.assertXhtml('''<p><a href="http://rpgplanet.cz">http://rpgplanet.cz</a></p>''', res)

    def testOdkaz(self):
        tree = parse('''(http://rpgplanet.cz Stranky materskeho projektu)''', registerMap)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Stranky materskeho projektu')

        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('''<para><ulink url="http://rpgplanet.cz">Stranky materskeho projektu</ulink></para>''', res)

        res = expand(tree, 'xhtml11', nodeMap)
        self.assertXhtml('''<p><a href="http://rpgplanet.cz">Stranky materskeho projektu</a></p>''', res)

    def testOdkazBadSyntax(self):
        tree = parse('''(http://rpgplanet.cz Stranky materskeho projektu''', registerMap)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, TextNode)
        self.assertEquals(tree.children[0].children[0].children[0].content, '(')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.Hyperlink)

        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('''<para>(<ulink url="http://rpgplanet.cz">http://rpgplanet.cz</ulink> Stranky materskeho projektu</para>''', res)

        res = expand(tree, 'xhtml11', nodeMap)
        self.assertXhtml('''<p>(<a href="http://rpgplanet.cz">http://rpgplanet.cz</a> Stranky materskeho projektu</p>''', res)

    def testFixedText(self):
        tree = parse('\n§§\nTohle je ""nenaparsovaný"" text\nKterý je fixní.\n§§\n', registerMap)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.NeformatovanyText)
        self.assertEquals(len(tree.children[0].children), 1)
        self.assertEquals(tree.children[0].children[0].children[0].content, 'Tohle je ""nenaparsovaný"" text\nKterý je fixní.')

        res = expand(tree, 'xhtml11', nodeMap)
        self.assertXhtml('<pre>Tohle je ""nenaparsovaný"" text\nKterý je fixní.</pre>', res)

        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('<literallayout>Tohle je ""nenaparsovaný"" text\nKterý je fixní.</literallayout>', res)

    def testOdkazWithEmpansedParts(self):
        tree = parse('''(http://rpgplanet.cz Stranky ""materskeho"" """projektu""")''', registerMap)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Stranky ')
        self.assertEquals(tree.children[0].children[0].children[0].children[1].__class__, nodes.Zvyraznene)
        self.assertEquals(tree.children[0].children[0].children[0].children[2].content, ' ')
        self.assertEquals(tree.children[0].children[0].children[0].children[3].__class__, nodes.Silne)

        res = expand(tree, 'docbook4', nodeMap)
        self.assertDocbook4('''<para><ulink url="http://rpgplanet.cz">Stranky <emphasis>materskeho</emphasis> <emphasis role="bold">projektu</emphasis></ulink></para>''', res)

        res = expand(tree, 'xhtml11', nodeMap)
        self.assertXhtml('''<p><a href="http://rpgplanet.cz">Stranky <em>materskeho</em> <strong>projektu</strong></a></p>''', res)

if __name__ == "__main__":
    main()