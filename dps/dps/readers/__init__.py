#! /usr/bin/env python

"""
:Authors: David Goodger; Ueli Schlaepfer
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/02/07 01:59:51 $
:Copyright: This module has been placed in the public domain.

This package contains DPS Reader modules.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Reader', 'get_reader_class']


import sys
from dps import nodes, utils


class Reader:

    """
    Abstract base class for docutils Readers.

    The three steps of a Reader's responsibility are defined: `scan()`,
    `parse()`, and `transform()`. Call `read()` to process a document.
    """

    transforms = ()
    """Ordered list of transform classes (each with a ``transform()`` method).
    Populated by subclasses. `Reader.transform()` instantiates & runs them."""

    def __init__(self, reporter, languagecode):
        """
        Initialize the Reader instance.

        Several instance attributes are defined with dummy initial values.
        Subclasses may use these attributes as they wish.
        """

        self.languagecode = languagecode
        """Default language for new documents."""

        self.reporter = reporter
        """A `utils.Reporter` instance shared by all doctrees."""

        self.source = None
        """Path to the source of raw input."""

        self.input = None
        """Raw text input; either a single string or, for more complex cases,
        a collection of strings."""

        self.transforms = list(self.transforms)
        """Instance copy of `Reader.transforms`; may be modified by client."""

    def read(self, source, parser):
        self.source = source
        self.parser = parser
        self.scan(self.source)          # may modify self.parser,
                                        # depending on input
        self.parse(self.parser)
        self.transform()
        return self.document

    def scan(self, source):
        """Override to read `self.input` from `source`."""
        raise NotImplementedError('subclass must override this method')

    def scanfile(self, source):
        """
        Scan a single file, store data in `self.input`.

        Parameter `source` may be:

        (a) a file-like object, which is read directly;
        (b) a path to a file, which is opened and then read; or
        (c) `None`, which implies `sys.stdin`.
        """
        if hasattr(source, 'read'):
            self.input = source.read()
        elif self.source:
            self.input = open(source).read()
        else:
            self.input = sys.stdin.read()

    def parse(self, parser):
        """Parse `self.input` into a document tree."""
        self.document = self.newdocument()
        parser.parse(self.input, self.document)

    def transform(self):
        """Run all of the transforms defined for this Reader."""
        for xclass in self.transforms:
            xclass().transform(self.document)

    def newdocument(self, languagecode=None):
        """Create and return a new empty document tree (root node)."""
        document = nodes.document(
              languagecode=(languagecode or self.languagecode),
              reporter=self.reporter)
        return document


_reader_aliases = {'rtxt': 'standalone',
                   'restructuredtext': 'standalone'}

def get_reader_class(readername):
    """Return the Reader class from the `readername` module."""
    readername = readername.lower()
    if _reader_aliases.has_key(readername):
        readername = _reader_aliases[readername]
    module = __import__(readername, globals(), locals())
    return module.Reader
