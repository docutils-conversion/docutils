#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This module has been placed in the public domain.

This is ``docutils.parsers.rst`` package. It exports a single class, `Parser`.

Usage
=====

1. Create a parser::

       parser = docutils.parsers.restructuredtext.Parser()

   Several optional arguments may be passed to modify the parser's behavior.
   Please see `docutils.parsers.Parser` for details.

2. Gather input (a multi-line string), by reading a file or the standard
   input::

       input = sys.stdin.read()

3. Create a new empty `docutils.nodes.document` tree::

       document = docutils.utils.new_document()

   See `docutils.utils.new_document()` for parameter details.

4. Run the parser, populating the document tree::

       parser.parse(input, document)

Parser Overview
===============

The reStructuredText parser is implemented as a state machine, examining its
input one line at a time. To understand how the parser works, please first
become familiar with the `docutils.statemachine` module, then see the
`states` module.
"""

__docformat__ = 'reStructuredText'


import docutils.parsers
import docutils.statemachine
import states


class Parser(docutils.parsers.Parser):

    """The reStructuredText parser."""

    supported = ('restructuredtext', 'rst', 'rest', 'restx', 'rtxt', 'rstx')
    """Aliases this parser supports."""

    def __init__(self, rfc2822=None, inliner=None):
        if rfc2822:
            self.initial_state = 'RFC2822Body'
        else:
            self.initial_state = 'Body'
        self.state_classes = states.state_classes
        self.inliner = inliner

    def parse(self, inputstring, document):
        """Parse `inputstring` and populate `document`, a document tree."""
        self.setup_parse(inputstring, document)
        debug = document.reporter[''].debug
        self.statemachine = states.RSTStateMachine(
              state_classes=self.state_classes,
              initial_state=self.initial_state,
              debug=debug)
        inputlines = docutils.statemachine.string2lines(
              inputstring, convert_whitespace=1)
        self.statemachine.run(inputlines, document, inliner=self.inliner)
