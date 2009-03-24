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
        tree = parse('"""silne"""', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'silne')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><emphasis role="bold">silne</emphasis></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><strong>silne</strong></p>''', res)

        res = expand(tree, 'bbcode', expander_map)
        self.assertBbcode('''[b]silne[/b]''', res)

    def testSilneWithAlternativeSyntax(self):
        tree = parse('*silne*', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'silne')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><emphasis role="bold">silne</emphasis></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><strong>silne</strong></p>''', res)

    def testSilneWithPrefix(self):
        tree = parse('" nic """silne"""', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].content, '" nic ')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'silne')
        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para>" nic <emphasis role="bold">silne</emphasis></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p>" nic <strong>silne</strong></p>''', res)

class TestZvyraznene(OutputTestCase):
    def testZvyraznene(self):
        tree = parse('''""zvyraznene""''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Zvyraznene)

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><emphasis>zvyraznene</emphasis></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><em>zvyraznene</em></p>''', res)

    def testZvyrazneneAlternativeSyntax(self):
        tree = parse('//zvyraznene//', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Zvyraznene)

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><emphasis>zvyraznene</emphasis></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><em>zvyraznene</em></p>''', res)

class TestOdkaz(OutputTestCase):
    def testOdkazEasyNahrazovani(self):
        tree = parse('''http://rpgplanet.cz''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Hyperlink)

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><ulink url="http://rpgplanet.cz">http://rpgplanet.cz</ulink></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><a href="http://rpgplanet.cz">http://rpgplanet.cz</a></p>''', res)

    def testOdkazVZavorkach(self):
        tree = parse('''(http://rpgplanet.cz)''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].content, '(')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[1].link, 'http://rpgplanet.cz')
        self.assertEquals(tree.children[0].children[0].children[1].children[0].content, 'http://rpgplanet.cz')
        self.assertEquals(tree.children[0].children[0].children[2].content, ')')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para>(<ulink url="http://rpgplanet.cz">http://rpgplanet.cz</ulink>)</para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p>(<a href="http://rpgplanet.cz">http://rpgplanet.cz</a>)</p>''', res)

    def _testLinkStructure(self, link):
        tree = parse("(%s Stranky materskeho projektu)" % link, register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Stranky materskeho projektu')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><ulink url="%s">Stranky materskeho projektu</ulink></para>''' % link, res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><a href="%s">Stranky materskeho projektu</a></p>''' % link, res)

    def testOdkaz(self):
        self._testLinkStructure("http://rpgplanet.cz/")

    def testOdkazWithAlternateSyntax(self):
        self._testLinkStructure("http://www.dracidoupe.cz/index.php?rub=forum&skin=dark")

    def testOdkazBigChars(self):
        self._testLinkStructure("http://RPGPLANET.CZ/NECO")

    def testOdkazWithEscapedChars(self):
        self._testLinkStructure("http://shii.org/knows/Shii%27s_Solution_to_the_Problem_of_Wikipedia")

    def testOdkazWithEscapedCharsAndSection(self):
        self._testLinkStructure("http://shii.org/knows/Shii%27s_Solution_to_the_Problem_of_Wikipedia#Then_what.27s_to_be_done.3F")

    def testOdkazMakro(self):
        tree = parse('''((odkaz http://rpgplanet.cz Stranky materskeho projektu))''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Stranky materskeho projektu')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><ulink url="http://rpgplanet.cz">Stranky materskeho projektu</ulink></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><a href="http://rpgplanet.cz">Stranky materskeho projektu</a></p>''', res)

    def testOdkazBadSyntax(self):
        tree = parse('''(http://rpgplanet.cz Stranky materskeho projektu''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.TextNode)
        self.assertEquals(tree.children[0].children[0].children[0].content, '(')
        self.assertEquals(tree.children[0].children[0].children[1].__class__, nodes.Hyperlink)

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para>(<ulink url="http://rpgplanet.cz">http://rpgplanet.cz</ulink> Stranky materskeho projektu</para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p>(<a href="http://rpgplanet.cz">http://rpgplanet.cz</a> Stranky materskeho projektu</p>''', res)

    def testOdkazWithEmpansedParts(self):
        tree = parse('''(http://rpgplanet.cz Stranky ""materskeho"" """projektu""")''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Stranky ')
        self.assertEquals(tree.children[0].children[0].children[0].children[1].__class__, nodes.Zvyraznene)
        self.assertEquals(tree.children[0].children[0].children[0].children[1].children[0].content, 'materskeho')
        self.assertEquals(tree.children[0].children[0].children[0].children[2].content, ' ')
        self.assertEquals(tree.children[0].children[0].children[0].children[3].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[0].children[0].children[3].children[0].content, 'projektu')

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><ulink url="http://rpgplanet.cz">Stranky <emphasis>materskeho</emphasis> <emphasis role="bold">projektu</emphasis></ulink></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><a href="http://rpgplanet.cz">Stranky <em>materskeho</em> <strong>projektu</strong></a></p>''', res)

    def testConversionInHeading(self):
        tree = parse('''= (http://rpgplanet.cz Stranky materskeho projektu) =\n''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Nadpis)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[0].link, 'http://rpgplanet.cz')
        self.assertEquals(tree.children[0].children[0].children[0].children[0].content, 'Stranky materskeho projektu')

    def testConversionInZvyraznene(self):
        tree = parse('''""(http://rpgplanet.cz Stranky materskeho projektu)""''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Zvyraznene)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].link, 'http://rpgplanet.cz')
        self.assertEquals(tree.children[0].children[0].children[0].children[0].children[0].content, 'Stranky materskeho projektu')

    def testConversionInSilne(self):
        tree = parse('''"""(http://rpgplanet.cz Stranky materskeho projektu)"""''', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Silne)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].__class__, nodes.Hyperlink)
        self.assertEquals(tree.children[0].children[0].children[0].children[0].link, 'http://rpgplanet.cz')
        self.assertEquals(tree.children[0].children[0].children[0].children[0].children[0].content, 'Stranky materskeho projektu')

class TestFixedText(OutputTestCase):

    def testSimple(self):
        tree = parse(u'\n§§\nTohle je ""nenaparsovaný"" text\nKterý je fixní.\n§§\n', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.NeformatovanyText)
        self.assertEquals(len(tree.children[0].children), 1)
        self.assertEquals(tree.children[0].children[0].children[0].content, u'Tohle je ""nenaparsovaný"" text\nKterý je fixní.')

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml(u'<pre>Tohle je ""nenaparsovaný"" text\nKterý je fixní.</pre>', res)

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4(u'<literallayout>Tohle je ""nenaparsovaný"" text\nKterý je fixní.</literallayout>', res)

class TestPreskrtnute(OutputTestCase):
    def testMakro(self):
        tree = parse(u'((preskrtnute preciarknuty text))', register_map)
        self.assertEquals(tree.children[0].children[0].__class__, nodes.Odstavec)
        self.assertEquals(tree.children[0].children[0].children[0].__class__, nodes.Preskrtnute)

        res = expand(tree, 'docbook4', expander_map)
        self.assertDocbook4('''<para><emphasis role="strikethrough">preciarknuty text</emphasis></para>''', res)

        res = expand(tree, 'xhtml11', expander_map)
        self.assertXhtml('''<p><strike>preciarknuty text</strike></p>''', res)

class TestHorniIndex(OutputTestCase):
    
    def setUp(self):
        super(TestHorniIndex, self).setUp()
        
        self.text = u"text v nornim indexu zdravi - 你好"
        self.tree = parse(u'((horni-index %s))' % self.text, register_map)
    
    def testMacroParsing(self):
        self.assertEquals(nodes.Odstavec, self.tree.children[0].children[0].__class__)
        self.assertEquals(nodes.HorniIndex, self.tree.children[0].children[0].children[0].__class__)
        self.assertEquals(self.text, self.tree.children[0].children[0].children[0].children[0].content)
    
    def testXhtmlExpansion(self):
        res = expand(self.tree, 'xhtml11', expander_map)
        self.assertXhtml(u'<p><sup>%s</sup></p>' % self.text, res)

class TestDolniIndex(OutputTestCase):
    
    def setUp(self):
        super(TestDolniIndex, self).setUp()
        
        self.tree = parse(u'H((dolni-index 2))0', register_map)
    
    def testMacroParsing(self):
        self.assertEquals(nodes.Odstavec, self.tree.children[0].children[0].__class__)
        self.assertEquals(nodes.DolniIndex, self.tree.children[0].children[0].children[1].__class__)
        self.assertEquals(u"2", self.tree.children[0].children[0].children[1].children[0].content)
    
    def testXhtmlExpansion(self):
        res = expand(self.tree, 'xhtml11', expander_map)
        self.assertXhtml(u'<p>H<sub>2</sub>0</p>', res)

class TestTrademark(OutputTestCase):
    def setUp(self):
        super(TestTrademark, self).setUp()
        
        self.tree = parse(u'((trademark))', register_map)
    
    def _assertTree(self, tree):
        self.assertEquals(nodes.Odstavec, tree.children[0].children[0].__class__)
        self.assertEquals(nodes.Trademark, tree.children[0].children[0].children[0].__class__)
    
    def testMacroParsing(self):
        self._assertTree(self.tree)
    
    def testXhtmlExpansion(self):
        res = expand(self.tree, 'xhtml11', expander_map)
        self.assertXhtml(u'<p>&#0153;</p>', res)
    
    def testUppercaseAlternative(self):
        tree = parse(u'(TM)', register_map)
        self._assertTree(tree)

    def testLowercaseAlternative(self):
        tree = parse(u'(tm)', register_map)
        self._assertTree(tree)

    def testTmNotResolved(self):
        tree = parse(u'tm', register_map)
        self.assertEquals(u"tm", tree.children[0].children[0].children[0].content)

    def testNegated(self):
        tree = parse(u'!(tm)', register_map)
        self.assertEquals(u"(tm)", tree.children[0].children[0].children[0].content)

class TestCopyright(OutputTestCase):
    def setUp(self):
        super(TestCopyright, self).setUp()
        
        self.tree = parse(u'((copyright))', register_map)
    
    def _assertTree(self, tree):
        self.assertEquals(nodes.Odstavec, tree.children[0].children[0].__class__)
        self.assertEquals(nodes.Copyright, tree.children[0].children[0].children[0].__class__)
    
    def testMacroParsing(self):
        self._assertTree(self.tree)
    
    def testXhtmlExpansion(self):
        res = expand(self.tree, 'xhtml11', expander_map)
        self.assertXhtml(u'<p>&#0169;</p>', res)
    
    def testUppercaseAlternative(self):
        tree = parse(u'(C)', register_map)
        self._assertTree(tree)

    def testLowercaseAlternative(self):
        tree = parse(u'(c)', register_map)
        self._assertTree(tree)

    def testcNotResolved(self):
        tree = parse(u'c', register_map)
        self.assertEquals(u"c", tree.children[0].children[0].children[0].content)

    def testCNotResolved(self):
        tree = parse(u'C', register_map)
        self.assertEquals(u"C", tree.children[0].children[0].children[0].content)

    def testNegated(self):
        tree = parse(u'!(C)', register_map)
        self.assertEquals(u"(C)", tree.children[0].children[0].children[0].content)

class TestRightsReserved(OutputTestCase):
    def setUp(self):
        super(TestRightsReserved, self).setUp()
        
        self.tree = parse(u'((rights-reserved))', register_map)
    
    def _assertTree(self, tree):
        self.assertEquals(nodes.Odstavec, tree.children[0].children[0].__class__)
        self.assertEquals(nodes.RightsReserved, tree.children[0].children[0].children[0].__class__)
    
    def testMacroParsing(self):
        self._assertTree(self.tree)
    
    def testXhtmlExpansion(self):
        res = expand(self.tree, 'xhtml11', expander_map)
        self.assertXhtml(u'<p>&#0174;</p>', res)
    
    def testUppercaseAlternative(self):
        tree = parse(u'(R)', register_map)
        self._assertTree(tree)

    def testLowercaseAlternative(self):
        tree = parse(u'(r)', register_map)
        self._assertTree(tree)

    def testrNotResolved(self):
        tree = parse(u'r', register_map)
        self.assertEquals(u"r", tree.children[0].children[0].children[0].content)

    def testRNotResolved(self):
        tree = parse(u'R', register_map)
        self.assertEquals(u"R", tree.children[0].children[0].children[0].content)

    def testNegated(self):
        tree = parse(u'!(R)', register_map)
        self.assertEquals(u"(R)", tree.children[0].children[0].children[0].content)
    
if __name__ == "__main__":
    main()
