#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/02/06 02:56:47 $
:Copyright: This module has been placed in the public domain.

Simple internal document tree Writer, writes indented pseudo-XML.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Writer']


from dps import writers


class Writer(writers.Writer):

    def write(self, document, destination):
        output = document.pformat()
        if destination:
            open(destination, 'w').write(output)
        else:
            print output
