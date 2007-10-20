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
from subprocess import call, PIPE


from unittest import main
from czechtile import *

from module_test import *

# logging.basicConfig(level=logging.DEBUG)

scriptFile = join(pardir, pardir, 'bin', 'czechtile')

class TestConsoleScript(OutputTestCase):

    def testXhtmlTransform(self):
        txt = 'txt'
        inFile = getPersistentTmpfile()
        f = open(inFile, 'w')
        f.write(txt)
        f.close()

        xhtmlFile = getPersistentTmpfile(suffix='.html')
        docbookFile = getPersistentTmpfile(suffix='.xml')

        ec = call([scriptFile, '-i', inFile, '--xhtml', xhtmlFile, '--docbook4', docbookFile])
        logging.debug('Called with exit code %s' % ec)

        f = open(xhtmlFile)
        self.assertXhtml(u'<p>txt</p>', f.read().decode('utf-8'))
        f.close()

        f = open(docbookFile)
        self.assertDocbook4(u'<para>txt</para>', f.read().decode('utf-8'))
        f.close()

        remove(inFile)
        remove(xhtmlFile)
        remove(docbookFile)


if __name__ == "__main__":
    main()