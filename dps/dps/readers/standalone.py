#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/02/06 03:01:46 $
:Copyright: This module has been placed in the public domain.

Standalone file Reader for the reStructuredText markup syntax.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Reader']


import sys
from dps import readers
from dps.transforms import frontmatter, references
try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser


class Reader(readers.Reader):

    document = None
    """A single document tree."""

    def scan(self):
        if self.source:
            self.input = open(self.source).read()
        else:
            self.input = sys.stdin.read()

    def parse(self, parser):
        self.document = self.newdocument()
        parser.parse(self.input, self.document)

    def transform(self):
        frontmatter.DocTitle().transform(self.document)
        frontmatter.DocInfo().transform(self.document)
        references.Hyperlinks().transform(self.document)
        references.Footnotes().transform(self.document)
        references.Substitutions().transform(self.document)

    def getdocument(self):
        return self.document
