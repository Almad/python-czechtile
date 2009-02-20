#!/usr/bin/env python
from ConfigParser import SafeConfigParser as ConfigParser
import os, os.path
from subprocess import check_call
from tempfile import mkstemp
import sys

def get_tests_path():
    config = os.path.join(os.path.dirname(__file__), 'tests.ini')
    if os.path.exists(config):
        parser = ConfigParser()
        parser.read(config)
        if parser.has_section('czechtile') and parser.has_option('czechtile', 'path'):
            path = parser.has_option('czechtile', 'path')
            if not os.path.exists(path):
                raise ValueError("%(path)s does not exists" % {'path' : path})
            return path
    else:
        return os.path.join(os.path.dirname(__file__), '../czechtile-syntax/testy/')


def get_macro_tests(path):
    return os.listdir(path)

def run_compare_test(format, testprefix):
    executable = os.path.join(os.path.join(os.path.dirname(__file__), 'bin', 'czechtile'))
    result = mkstemp()[1]
    check_call([executable, '-i', testprefix+'.czt',
                    '--'+format+'='+result])
    orig = open(testprefix+'.'+format)
    res = open(result)
    try:
        expected = orig.read()
        done = res.read()
        assert expected == done, "%s != %s" % (expected, done)
        sys.stdout.write(".")
        sys.stdout.flush()
    except AssertionError:
        sys.stdout.write("E")
        sys.stdout.flush()
        raise
    finally:
        orig.close()
        res.close()    
    
    

def run_macro_tests(path):
    tests = [file for file in os.listdir(path) if file.endswith('.czt')]
    for test in tests:
        name = test[:-4]
        if os.path.exists(os.path.join(path, name+'.html')):
            run_compare_test('html', os.path.join(path, name))

def main():
    check_call(os.path.join(os.path.dirname(__file__), 'czechtile', 'test', 'run.py'))
    #path = get_tests_path()
    #macro_path = os.path.join(path, 'makra')
    #macro_tests = get_macro_tests(macro_path)
    #for test in macro_tests:
    #    run_macro_tests(os.path.join(macro_path, test))
    #sys.stdout.write("\n")
    
if __name__ == "__main__":
    main()
