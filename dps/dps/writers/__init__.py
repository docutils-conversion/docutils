#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/02/07 01:58:29 $
:Copyright: This module has been placed in the public domain.

This package contains DPS Writer modules.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Writer', 'get_writer_class']


import sys


class Writer:

    """
    Abstract base class for docutils Writers.

    Call `write()` to process a document.
    """

    def write(self, document, destination):
        self.document = document
        self.destination = destination
        self.transform()
        self.record(self.document, self.destination)

    def transform(self):
        """Override to run document tree transforms."""
        raise NotImplementedError('subclass must override this method')

    def record(self, document, destination):
        """Override to record `document` to `destination`."""
        raise NotImplementedError('subclass must override this method')

    def recordfile(self, output, destination):
        """
        Write `output` to a single file.

        Parameters:
        - `output`: Data to write.
        - `destination`: one of:

          (a) a file-like object, which is written directly;
          (b) a path to a file, which is opened and then written; or
          (c) `None`, which implies `sys.stdout`.
        """
        if hasattr(self.destination, 'write'):
            destination.write(output)
        elif self.destination:
            open(self.destination, 'w').write(output)
        else:
            sys.stdout.write(output)
    pass


_writer_aliases = {}

def get_writer_class(writername):
    """Return the Writer class from the `writername` module."""
    writername = writername.lower()
    if _writer_aliases.has_key(writername):
        writername = _writer_aliases[writername]
    module = __import__(writername, globals(), locals())
    return module.Writer
