#! /usr/bin/env python

"""
:Authors: Garth Kidd, David Goodger
:Contact: garth@deadlybloodyserious.com
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/01 16:29:12 $
:Copyright: This module has been placed in the public domain.

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

__all__ = [ 'ParserTestCaseSuite' ]

import UnitTestFolder
import sys, os, unittest, re, difflib, types
from pprint import pformat

# try to import the current working version if possible
try:
    import states                       # works if running in local directory
except ImportError:
    try:                                # running in test framework dir?
        sys.path.insert(0, os.path.join(os.pardir, 'restructuredtext'))
        import states
    except ImportError:
        try:                            # restructuredtext on path?
            from restructuredtext import states
        except ImportError:             # try to run installed code
            from dps.parsers.restructuredtext import states

from dps.statemachine import string2lines

try:
    import mypdb as pdb
except:
    import pdb


class CustomTestSuite(unittest.TestSuite):

    """
    A collection of custom TestCases.

    """

    id = ''
    """Identifier for the TestSuite. Prepended to the
    TestCase identifiers to make identification easier."""

    nextTestCaseId = 0
    """The next identifier to use for non-identified test cases."""

    def __init__(self, tests=(), id=None):
        """Initialise the CustomTestSuite.

        Arguments:

        id -- identifier for the suite, prepended to test cases.
        """
        unittest.TestSuite.__init__(self, tests)
        if id is not None:
            self.id = id

    def addTestCase(self, testCaseClass, methodName, input, expected,
                    id=None, runInDebugger=0, shortDescription=None):
        """
        Create a custom TestCase in the CustomTestSuite.
        Also returns it, just in case.

        Arguments:

        testCaseClass -- 
        methodName -- 
        input -- input to the parser.
        expected -- expected output from the parser.
        id -- unique test identifier, used by the test framework.
        runInDebugger -- if true, run this test under the pdb debugger.
        shortDescription -- override to default test description.
        """
        # generate id if required
        if id is None:
            id = self.nextTestCaseId
            self.nextTestCaseId += 1

        # test identifier will become suiteid.testid
        tcid = '%s: %s' % (self.id, id)

        # generate and add test case
        tc = testCaseClass(methodName, input, expected, tcid,
                             runInDebugger=runInDebugger,
                             shortDescription=shortDescription)
        self.addTest(tc)
        return tc


class CustomTestCase(unittest.TestCase):

    compare = difflib.Differ().compare
    """Comparison method shared by all subclasses."""

    def __init__(self, methodName, input, expected, id,
                 runInDebugger=0, shortDescription=None):
        """
        Initialise the CustomTestCase.

        Arguments:

        methodName -- name of test method to run.
        input -- input to the parser.
        expected -- expected output from the parser.
        id -- unique test identifier, used by the test framework.
        runInDebugger -- if true, run this test under the pdb debugger.
        shortDescription -- override to default test description.
        """
        self.id = id
        self.input = input
        self.expected = expected
        self.runInDebugger = runInDebugger
        # Ring your mother.
        unittest.TestCase.__init__(self, methodName)
        # Cheat on the method documentation. Oh, the shame!
        if shortDescription is not None:
            self.__testMethodDoc = shortDescription

    def __str__(self):
        """
        Return string conversion. Overridden to give test id, not method name.
        """
        return "%s (%s)" % (self.id, self.__class__)

    def id(self):
        """Return identifier. Overridden to give test id, not method name."""
        return "%s.%s" % (self.__class__, self.id)

    def compareOutput(self, input, output, expected):
        """`input`, `output`, and `expected` should all be strings."""
        try:
            self.assertEquals('\n' + output, '\n' + expected)
        except AssertionError:
            print >>sys.stderr
            print >>sys.stderr, 'input:'
            print >>sys.stderr, input
            print >>sys.stderr, '-: expected'
            print >>sys.stderr, '+: output'
            print >>sys.stderr, ''.join(self.compare(expected.splitlines(1),
                                                     output.splitlines(1)))
            raise


class ParserTestSuite(CustomTestSuite):

    """
    A collection of ParserTestCases.

    A ParserTestSuite instance manufactures ParserTestCases,
    keeps track of them, and provides a shared test fixture (a-la
    setUp and tearDown).
    """

    def generateTests(self, dict, dictname='totest'):
        """
        Stock the suite with test cases generated from a test data dictionary.

        Each dictionary key (test type name) maps to a list of tests. Each
        test is a list: input, expected output, optional modifier. The
        optional third entry, a behavior modifier, can be 0 (temporarily
        disable this test) or 1 (run this test under the pdb debugger). Tests
        should be self-documenting and not require external comments.
        """
        for name, cases in dict.items():
            casenum = 0
            for case in cases:
                runInDebugger = 0
                if len(case)==3:
                    if case[2]:
                        runInDebugger = 1
                    else:
                        continue
                self.addTestCase(ParserTestCase, 'test_statemachine',
                                 input=case[0], expected=case[1],
                                 id='%s[%r][%s]' % (dictname, name, casenum),
                                 runInDebugger=runInDebugger)
                casenum = casenum + 1


class ParserTestCase(CustomTestCase):

    """
    Output checker for the parser.

    Should probably be called ParserOutputChecker, but I can deal with
    that later when/if someone comes up with a category of parser test
    cases that have nothing to do with the input and output of the parser.
    """

    statemachine = states.RSTStateMachine(stateclasses=states.stateclasses,
                                          initialstate='Body',
                                          debug=UnitTestFolder.debug)
    """states.RSTStateMachine shared by all ParserTestCases."""

    def test_statemachine(self):
        if self.runInDebugger:
            pdb.set_trace()
        document = self.statemachine.run(string2lines(self.input),
                                         warninglevel=4,
                                         errorlevel=4)
        output = document.pprint()
        self.compareOutput(self.input, output, self.expected)


class TableParserTestSuite(unittest.TestSuite):

    """
    A collection of TableParserTestCases.

    A TableParserTestSuite instance manufactures TableParserTestCases,
    keeps track of them, and provides a shared test fixture (a-la
    setUp and tearDown).
    """

    def generateTests(self, dict, dictname='totest'):
        """
        Stock the suite with test cases generated from a test data dictionary.

        Each dictionary key (test type name) maps to a list of tests. Each
        test is a list: an input table, expected output from parsegrid(),
        expected output from parse(), optional modifier. The optional fourth
        entry, a behavior modifier, can be 0 (temporarily disable this test)
        or 1 (run this test under the pdb debugger). Tests should be
        self-documenting and not require external comments.
        """
        for name, cases in dict.items():
            casenum = 0
            for case in cases:
                runInDebugger = 0
                if len(case)==4:
                    if case[3]:
                        runInDebugger = 1
                    else:
                        continue
                self.addTestCase(TableParserTestCase, 'test_parsegrid',
                                 input=case[0], expected=case[1],
                                 id='%s[%r][%s]' % (dictname, name, casenum),
                                 runInDebugger=runInDebugger)
                """self.addTestCase(TableParserTestCase, 'test_parse',
                                 input=case[0], expected=case[2],
                                 id='%s[%r][%s]' % (dictname, name, casenum),
                                 runInDebugger=runInDebugger)"""
                casenum = casenum + 1


class TableParserTestCase(CustomTestCase):

    parser = states.TableParser()

    def test_parsegrid(self):
        parser.init(self.input)
        output = parser.parsegrid(self.input)
        self.compareOutput(pformat(self.input), pformat(output),
                           pformat(self.expected))
