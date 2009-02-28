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

import unittest

import os
from tempfile import mkstemp

class OutputTestCase(unittest.TestCase):

    def assertXhtml(self, txt, out):
        # result from CZT must be unicode string
        self.assertEquals(unicode, type(out))
        # for backward compatibility, tests assertEqals could be strings
        if isinstance(txt, str):
            txt.decode('utf-8')
        return self.assertEquals(u''.join([u'''<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="cs" lang="cs"><body class="article">''', txt, u'</body></html>']), out)

    def assertDocbook4(self, txt, out):
        # result from CZT must be unicode string
        self.assertEquals(unicode, type(out))
        # for backward compatibility, tests assertEqals could be strings
        if isinstance(txt, str):
            txt.decode('utf-8')
        return self.assertEquals(u''.join([u'''<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE article PUBLIC "-//OASIS//DTD DocBook XML V4.4//EN" "http://www.oasis-open.org/docbook/xml/4.4/docbookx.dtd"><article>''', txt, '</article>']), out)

    def assertBbcode(self, txt, out):
        # result from CZT must be unicode string
        self.assertEquals(unicode, type(out))
        # for backward compatibility, tests assertEqals could be strings
        if isinstance(txt, str):
            txt.decode('utf-8')
        return self.assertEquals(txt, out)

# slightly modified, taken from PyArticle
def getPersistentTmpfile(suffix='.czt', prefix='czechtile_', object=False):
    fd, fn = mkstemp(suffix=suffix,prefix=prefix)
    f = os.fdopen(fd, 'w')
    f.close()
    if object == True:
        return open(fn, 'w+b')
    else:
        return fn
