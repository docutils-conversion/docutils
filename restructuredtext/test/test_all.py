#!/usr/bin/env python

"""
Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1.2.4 $
Date: $Date: 2001/07/31 15:23:35 $
Copyright: This module has been placed in the public domain.
"""

from TestFramework import *
import os, os.path, re, sys, types

def isTestModule(filename):
    matcher = re.compile(r"^(test_[^\.]+)\.py$")
    match = matcher.match(filename)
    if match:
        return match.group(1)
    else:
        return None

def allSuite(scriptPath):
    """Return a test suite composed of all the tests we can find."""
    testLoader = unittest.defaultTestLoader
    testSuite = unittest.TestSuite()

    path, scriptName= os.path.split(os.path.abspath(scriptPath))
    if path is not None: 
        os.chdir(path)
    
    # get a list of test_*.py
    testPyMatcher = re.compile(r"^test_[^\.]+\.py$")  
    testModules = filter(None, map(isTestModule, os.listdir(path)))

    # remove test_all.py to avoid trouble
    if 'test_all' in testModules:
        testModules.remove('test_all')
        
    # Import modules and add their tests to the suite. 
    for modname in testModules:
        # import the module
        if debug:
            print "importing %s" % modname
        module = __import__(modname)
        
        # if there's a suite defined, incorporate its contents
        if 'suite' in dir(module):
            suite = getattr(module, 'suite')
            if type(suite) == types.FunctionType:
                s = suite()
                testSuite.addTests(s._tests)
            elif type(suite) == types.InstanceType \
                 and isinstance(suite, unittest.TestSuite):
                testSuite.addTests(suite._tests)
            else: 
                raise AssertionError, "don't understand suite"
        else:
            # Look for individual tests
            moduleTests = testLoader.loadTestsFromModule(module) 

            # unittest.TestSuite.addTests() doesn't work as advertised, 
            # as it can't load tests from another TestSuite, so we have
            # to cheat: 
            testSuite.addTests(moduleTests._tests)
        
    return testSuite

if __name__ == '__main__':
    main(suite=allSuite(sys.argv[0]))
