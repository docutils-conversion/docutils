#! /usr/bin/env python

"""
Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1.2.3 $
Date: $Date: 2001/07/29 22:34:52 $
Copyright: This module has been placed in the public domain.
"""

# So that individual test modules can share a bit of state,
# `TestFramework` acts as an intermediary for the following
# variables: 

debug = 0
verbosity = 1

__all__ = ( 'debug', 'verbosity', 'states' )

# Imports

import sys, os, getopt

# Import `states`, prepending to `sys.path` if necessary. 

try:
    import states
except ImportError:
    sys.path.insert(0, os.path.join('..', 'restructuredtext'))
    import states

class Tee:

    """Write to a file and a stream (default: stdout) simulteaneously."""
    
    def __init__(self, filename, stream=sys.__stdout__):
        self.file = open(filename, 'w')
        self.stream = stream
    
    def write(self, string):
        self.stream.write(string)
        self.file.write(string)

import unittest, re
# import ndiff
# import states
#from dps.statemachine import string2lines
#try:
#    import mypdb as pdb
#except:
#    import pdb

class DataTests(unittest.TestCase):

    """
    Test data marked with 'XXX' denotes areas where further error checking
    needs to be done.
    """

    def setUp(self):
        self.sm = states.RSTStateMachine(stateclasses=states.stateclasses,
                                         initialstate='Body', debug=debug)

    def trytest(self, name, index):
        input, expected = self.totest[name][index]
        self.sm.run(string2lines(input), warninglevel=4,
                    errorlevel=4)
        output = self.sm.memo.document.pprint()
        try:
            self.assertEquals('\n' + output, '\n' + expected)
        except AssertionError:
            print
            print 'input:'
            print input
            print '-: output'
            print '+: expected'
            ndiff.lcompare(output.splitlines(1), expected.splitlines(1))
            raise

    totest = {}

    """Tests to be run. Each key (test type name) maps to a list of tests.
    Each test is a list: input, expected output, optional modifier. The
    optional third entry, a behavior modifier, can be 0 (temporarily disable
    this test) or 1 (run this test under the pdb debugger)."""
    
    proven = {}
    """tests that have proven successful"""

    notyet = {}
    """tests we *don't* want to run"""

    ## uncomment to run previously successful tests also
    totest.update(proven)

    ## uncomment to run previously successful tests *only*
    #totest = proven

    ## uncomment to run experimental, expected-to-fail tests also
    #totest.update(notyet)

    ## uncomment to run experimental, expected-to-fail tests *only*
    #totest = notyet

    for name, cases in totest.items():
        numcases = len(cases)
        casenumlen = len('%s' % (numcases - 1))
        for i in range(numcases):
            trace = ''
            if len(cases[i]) == 3:      # optional modifier
                if cases[i][-1] == 1:   # 1 => run under debugger
                    del cases[i][0]
                    trace = 'pdb.set_trace();'
                else:                   # 0 => disable
                    continue
            exec ('def test_%s_%0*i(self): %s self.trytest("%s", %i)'
                  % (name, casenumlen, i, trace, name, i))

USAGE = """\
Usage: %(progName)s [options]

Options:
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output
  -d, --debug      Debug mode
"""

def usageExit(self, msg=None):
    """Print usage and exit."""
    if msg:
        print msg
    print self.USAGE % self.__dict__
    sys.exit(2)

def parseArgs(argv=sys.argv):
    """Parse command line arguments and set TestFramework state.
    
    State is to be acquired by test_* modules by a grotty hack:
    ``from TestFramework import *``. For this stylistic
    transgression, I expect to be first up against the wall
    when the revolution comes. --Garth"""
    try:
        options, args = getopt.getopt(argv[1:], 'hHvqd',
                                      ['help', 'verbose', 'quiet', 'debug'])
        
        for opt, value in options:
            if opt in ('-h', '-H', '--help'):
                usageExit()
            if opt in ('-q', '--quiet'):
                verbosity = 0
            if opt in ('-v', '--verbose'):
                verbosity = 2
            if opt in ('-d', '--debug'):
                debug =1
        
        if len(args) != 0:
            usageExit("No command-line arguments supported yet.")
        
    except getopt.error, msg:
        self.usageExit(msg)

def loadTestsFromModule(self, module, exceptThese=[]):
    """Return a suite of all tests cases contained in the given module"""
    tests = []
    module = __import__('__main__')
    for name in dir(module):
        if name in exceptThese:
            continue
        obj = getattr(module, name)
        if type(obj) == types.ClassType and issubclass(obj, TestCase):
            tests.append(self.loadTestsFromTestCase(obj))
    return self.suiteClass(tests)

def main(suite=None):
    """Shared `main` for any individual test_* file.
    
    suite -- TestSuite to run. If not specified, look for any
    globally defined tests and run them."""
    
    # ### Need to consider the output filename. ###
    sys.stderr = sys.stdout = Tee('test_all.out')
    parseArgs()
    if suite is None:
        # Load any globally defined tests.
        # WARNING: picks up DataTests above. Oops. 
        suite = loadTestsFromModule(module)
    if debug:
        print "Debug: Suite=%s" % suite
    testRunner = unittest.TextTestRunner(verbosity=verbosity)
    testRunner.run(suite)
