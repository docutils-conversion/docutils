#! /usr/bin/env python

"""
Author: Garth Kidd 
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1.2.2 $
Date: $Date: 2001/07/29 22:34:52 $
Copyright: This module has been placed in the public domain.

Test module for states.py.
"""

from TestFramework import *  # states, main, debug, verbose
import sys, unittest, re, difflib, types

from dps.statemachine import string2lines

try:
    import mypdb as pdb
except:
    import pdb

"""\
All of my previous ramblings about metaclasses_ are fatigue-deranged.
The primary benefit of basing tests as ``test*`` methods in a very
large TestCase is that they can share `setUp()` and `tearDown()`. If
it's too hard to use the method method <ahem>, the appropriate recourse
is to *find another way of providing shared fixtures*. So, here's the
design I'm going to pursue when I can next sit down and hack code: 

`ParserTestSuite` instances will provide shared test fixtures (`sm`, an 
instance of `states.RSTStateMachine`) and methods (`matchOutput()` et
al) and will crank out internally any `ParserTest`s required.

I'll decide on whether it should subclass `unittest.Suite` or just
return one from a `suite()` method when I get back to the code. 

Finally; now that I've decided on which class I'm going to expose, the 
filename of this module is looking like a silly choice. I'll ponder
that issue later, too. 

.. _metaclasses: http://www.python.org/doc/essays/metaclasses/
"""


"""
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

