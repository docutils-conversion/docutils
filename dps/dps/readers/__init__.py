#! /usr/bin/env python

"""
:Authors: David Goodger; Ueli Schlaepfer
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/02/06 03:01:40 $
:Copyright: This module has been placed in the public domain.

This package contains DPS Reader modules.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Reader', 'get_reader_class']


from dps import nodes, utils


class Reader:

    """
    Abstract base class for docutils Readers.

    The three steps of a Reader's responsibility are defined: `scan()`,
    `parse()`, and `transform()`. Call `read()` to process a document.
    """

    def __init__(self, languagecode='en', warninglevel=2, errorlevel=4,
                 warningstream=None, debug=0):
        """
        Initialize the Reader instance.

        Several instance attributes are defined with dummy initial values.
        Subclasses may use these attributes as they wish.
        """

        self.languagecode = languagecode
        """Default language for new documents."""

        self.reporter = utils.Reporter(warninglevel, errorlevel, warningstream,
                                       debug)
        """A `utils.Reporter` instance shared by all doctrees."""

        self.source = None
        """Path to the source of raw input."""

        self.input = None
        """Raw text input; either a single string or, for more complex cases,
        a collection of strings."""

    def read(self, source, parser):
        self.source = source
        self.scan()
        self.parse(parser)              # parser may vary depending on input
        self.transform()
        return self.getdocument()

    def scan(self, source):
        """Override to read `self.input` from `source`."""
        raise NotImplementedError('subclass must override this method')

    def parse(self, parser):
        """Override to parse `self.input` into one or more document trees."""
        raise NotImplementedError('subclass must override this method')

    def transform(self):
        """Override to run document tree transforms."""
        raise NotImplementedError('subclass must override this method')

    def newdocument(self, languagecode=None):
        """Create and return a new empty document tree (root node)."""
        if not languagecode:
            languagecode = self.languagecode
        document = nodes.document(languagecode=languagecode,
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
