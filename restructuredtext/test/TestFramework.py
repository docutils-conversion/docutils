#! /usr/bin/env python

"""
Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1.2.5 $
Date: $Date: 2001/07/31 15:21:54 $
Copyright: This module has been placed in the public domain.
"""

# So that individual test modules can share a bit of state,
# `TestFramework` acts as an intermediary for the following
# variables: 

debug = 0
verbosity = 1

__all__ = ( 'debug', 'verbosity', 'states', 'main', 'unittest' )

# Imports

import sys, os, getopt, types, unittest, re

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


USAGE = """\
Usage: test_whatever [options]

Options:
  -h, --help       Show this message
  -v, --verbose    Verbose output
  -q, --quiet      Minimal output
  -d, --debug      Debug mode
"""

def usageExit(msg=None):
    """Print usage and exit."""
    if msg:
        print msg
    print USAGE
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
        suite = unittest.defaultTestLoader.loadTestsFromModule(__import__('__main__'))
    if debug:
        print "Debug: Suite=%s" % suite
    testRunner = unittest.TextTestRunner(verbosity=verbosity)
    testRunner.run(suite)
