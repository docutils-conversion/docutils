#! /usr/bin/env python

"""
Author: Garth Kidd 
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1.2.3 $
Date: $Date: 2001/07/31 14:46:24 $
Copyright: This module has been placed in the public domain.

Test module for states.py.
"""

__all__ = [ 'ParserTestCaseFactory' ]

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

def makeStateMachine():
    """Make an RSTStateMachine for a ParserTestCaseFactory or a lone
    ParserTestCase."""
    return states.RSTStateMachine(stateclasses=states.stateclasses,
                                  initialstate='Body', debug=debug)

def makeDiffer():
    """Make a Differ for a ParserTestCaseFactory or a lone
    ParserTestCase."""
    return difflib.Differ()

class ParserTestCaseFactory(unittest.TestSuite):
    """A collection of ParserTestCases.
    
    A ParserTestCaseFactory instance manufactures ParserTestCases,
    keeps track of them, and provides a shared test fixture (a-la
    setUp and tearDown).

    """

    sharedStateMachine = None

    """states.RSTStateMachine shared during tests by ParserTestCases
    created by the factory."""

    differ = None

    """difflib.Differ shared during tests by ParserTestCases created
    by the factory."""
    
    id = "AnonymousCoward"
    
    """Identifier for the ParserTestCaseFactory. Prepended to the
    ParserTestCase identifiers to make identification easier."""
    
    nextParserTestCaseId = 0
    
    """The next identifier to use for non-identified test cases."""
    
    def __init__(self, id=None, tests=()):
        """Initialise the ParserTestCaseFactory.
        
        Arguments:
        
        id -- identifier for the factory, prepended to test cases.
        
        """
        unittest.TestSuite.__init__(self, tests)
        if id is not None:
            self.id = id
        
    def addParserTestCase(self, input, expected,
                          id=None, 
                          runInDebugger=0,
                          shortDescription=None):
        """Create a ParserTestCase in the ParserTestCaseFactory.
        Also returns it, just in case.

        Arguments:

        id -- unique test identifier, used by the test framework.
        input -- input to the parser.
        expected -- expected output from the parser.
        runInDebugger -- if true, run this test under the pdb debugger.
        shortDescription -- override to default test description.
        """
        # generate id if required
        if id is None:
            id = self.nextParserTestCaseId
            self.nextParserTestCaseId = self.nextParserTestCaseId+1
            
        # test identifier will become factoryid.testid
        ptcid = "%s.%s" % (self.id, id)
        
        # generate and add test case
        ptc = ParserTestCase(input, expected, ptcid, 
                             runInDebugger=runInDebugger,
                             shortDescription=shortDescription,
                             factory=self)
        self.addTest(ptc)
        return ptc
    
    def stockFactory(self, oldStyleTestDictionary):
        """Stock the factory using an old-style test dictionary."""
        for name, cases in oldStyleTestDictionary.items():
            for case in cases:
                runInDebugger = 0
                if len(case)==3 and case[2]:
                    runInDebugger = 1
                self.addParserTestCase(case[0], case[1], 
                                       runInDebugger=runInDebugger)

    def getStateMachine(self):
        """Return a shared RSTStateMachine."""
        if self.sharedStateMachine is None:
            self.sharedStateMachine = makeStateMachine()
        return self.sharedStateMachine
    
    def getCompareFunction(self):
        """Return a shared compare function."""
        if self.differ is None: 
            self.differ = makeDiffer()
        return self.differ.compare

class ParserTestCase(unittest.TestCase):
    """Output checker for the parser.
    
    Should probably be called ParserOutputChecker, but I can deal with
    that later when/if someone comes up with a category of parser test
    cases that have nothing to do with the input and output of the parser.
    
    """
    
    def __init__(self, input, expected, id, 
                 runInDebugger=0,
                 shortDescription=None,
                 factory=None):
        """Initialise the ParserTestCase.
        
        Arguments:
        
        id -- unique test identifier, used by the test framework.
        input -- input to the parser.
        expected -- expected output from the parser.
        runInDebugger -- if true, run this test under the pdb debugger.
        shortDescription -- override to default test description.
        factory -- ParserTestCaseFactory() from which to get shared state. 
        """
        
        # Set ParserTestCase attributes
        self.id = id
        self.input = input
        self.expected = expected
        self.runInDebugger = runInDebugger
        self.factory = factory
                
        # Ring your mother.
        unittest.TestCase.__init__(self, methodName = 'compareOutput')
        
        # Cheat on the method documentation. Oh, the shame!
        if shortDescription is not None:
            self.__testMethodDoc = shortDescription
            
    def id(self):
        """Return identifier.
        Overridden to give test id, not method name."""
        return "%s.%s" % (self.__class__, self.id)
    
    def __str__(self):
        """Return string conversion.
        Overridden to give test id, not method name."""
        return "%s (%s)" % (self.id, self.__class__)
        
    # Is it worth over-riding id()? 
    
    def compareOutput(self):
        sm = self.getStateMachine()
        compare = self.getCompareFunction()
        if self.runInDebugger:
            pdb.set_trace()
        sm.run(string2lines(self.input), warninglevel=4, errorlevel=4)
        output = sm.memo.document.pprint()
        
        try:
            self.assertEquals('\n' + output, '\n' + self.expected)
        except AssertionError:
            print
            print 'input:'
            print input
            print '-: expected'
            print '+: output'
            print ''.join(compare(self.expected.splitlines(1),
                                    output.splitlines(1)))
            raise
            
        
    def getStateMachine(self):
        """Return the RSTStateMachine from the factory, or a new one."""
        if self.factory is not None:
            return self.factory.getStateMachine()
        return makeStateMachine()
    
    def getCompareFunction(self):
        """Return the compare function from the factory, or a new one."""
        if self.factory is not None:
            return self.factory.getCompareFunction()
        return makeDiffer().compare
