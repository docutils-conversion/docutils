#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2002/02/12 02:19:43 $
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

    transforms = (frontmatter.DocTitle,
                  frontmatter.DocInfo,
                  references.Hyperlinks,
                  references.Footnotes,
                  references.Substitutions,)

    def scan(self):
        self.input = self.scanfile(self.source)
