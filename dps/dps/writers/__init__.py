#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2002/02/12 02:13:38 $
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

    document = None
    """The document to write."""

    destination = None
    """Where to write the document."""

    transforms = ()
    """Ordered list of transform classes (each with a ``transform()`` method).
    Populated by subclasses. `Writer.transform()` instantiates & runs them."""

    def __init__(self):
        """Initialize the Writer instance."""

        self.transforms = list(self.transforms)
        """Instance copy of `Writer.transforms`; may be modified by client."""

    def write(self, document, destination):
        self.document = document
        self.destination = destination
        self.transform()
        self.translate()
        self.record()

    def transform(self):
        """Run all of the transforms defined for this Writer."""
        for xclass in self.transforms:
            xclass().transform(self.document)

    def translate(self):
        """Override to do final document tree translation."""
        raise NotImplementedError('subclass must override this method')

    def record(self):
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


_writer_aliases = {}

def get_writer_class(writername):
    """Return the Writer class from the `writername` module."""
    writername = writername.lower()
    if _writer_aliases.has_key(writername):
        writername = _writer_aliases[writername]
    module = __import__(writername, globals(), locals())
    return module.Writer
