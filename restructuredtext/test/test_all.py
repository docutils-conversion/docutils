#!/usr/bin/env python

"""
Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1.2.2 $
Date: $Date: 2001/07/29 22:34:52 $
Copyright: This module has been placed in the public domain.
"""

from TestFramework import *

def suite():
    """Return a test suite composed of all the tests we can find."""
    testLoader = unittest.defaultTestLoader
    testSuite = unittest.TestSuite()
    
    # Import modules and add their tests to the suite. 
    for modname in [ 'test_escapers' ]:
        module = __import__(modname)
        moduleTests = testLoader.loadTestsFromModule(module)
        # unittest.TestSuite.addTests() doesn't work as advertised, 
        # as it can't load tests from another TestSuite, so we have
        # to cheat: 
        testSuite.addTests(moduleTests._tests)
        
    return testSuite

if __name__ == '__main__':
    main(suite=suite())
