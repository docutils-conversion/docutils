#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/02/07 01:58:44 $
:Copyright: This module has been placed in the public domain.

Simple internal document tree Writer, writes indented pseudo-XML.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Writer']


from dps import writers


class Writer(writers.Writer):

    def transform(self):
        pass

    def record(self, document, destination):
        output = document.pformat()
        self.recordfile(output, destination)
