#! /usr/bin/env python

"""
Author: Garth Kidd 
Contact: dgoodger@bigfoot.com
Revision: $Revision: 1.1.2.1 $
Date: $Date: 2001/07/29 12:21:09 $
Copyright: This module has been placed in the public domain.

Test module for states.py.
"""

from TestFramework import *  # states, main, debug, verbose
import sys
import unittest, re, difflib

from dps.statemachine import string2lines

try:
    import mypdb as pdb
except:
    import pdb

"""\
Okay, here's where things get a little confusing. For this part of the
test framework I'm going to be resorting to the use of metaclasses_.
Why? I need to be able to add bound methods to a test case *after* it
has been defined, which counts out the previous methodology. 

.. _metaclasses: http://www.python.org/doc/essays/metaclasses/

David's old code follows:
"""

class ParserTestCase(unittest.TestCase):

    """
    Test data marked with 'XXX' denotes areas where further error checking
    needs to be done.
    """

    diff = difflib.Differ().compare

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
            print '-: expected'
            print '+: output'
            print ''.join(self.diff(expected.splitlines(1),
                                    output.splitlines(1)))
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

