#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

    def _test_transform(self, txt=u'txt', format='xhtml', wrap_tag='p'):
        inFile = getPersistentTmpfile()
        f = open(inFile, 'w')
        f.write(txt.encode('utf-8'))
        f.close()

        output_file = getPersistentTmpfile(suffix='.'+format)

        ec = call([scriptFile, inFile, '-f', format, '-o', output_file, '--nowrap'])
        logging.debug('Called with exit code %s' % ec)

        f = open(output_file)
        output = f.read().decode('utf-8')
        f.close()

        self.assertEquals(u''.join([u'<%s>' % wrap_tag, txt, u'</%s>' % wrap_tag]), output)
        remove(inFile)
        remove(output_file)
    
    def test_basic_transform_xhtml(self):
        self._test_transform(u'test text', format='xhtml', wrap_tag='p')

    def test_basic_transform_docbook4(self):
        self._test_transform(u'test text', format='docbook4', wrap_tag='para')
        
    def test_transform_with_accents_xhtml(self):
        self._test_transform(u'živoťudarňý test', format='xhtml', wrap_tag='p')

    def test_transform_with_accents_docbook4(self):
        self._test_transform(u'živoťudarňý test', format='docbook4', wrap_tag='para')

if __name__ == "__main__":
    main()
