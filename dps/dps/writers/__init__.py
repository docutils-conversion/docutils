#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/02/06 02:56:21 $
:Copyright: This module has been placed in the public domain.

This package contains DPS Writer modules.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Writer', 'get_writer_class']


class Writer:

    """
    Abstract base class for docutils Writers.

    Call `write()` to process a document.
    """

    pass


_writer_aliases = {}

def get_writer_class(writername):
    """Return the Writer class from the `writername` module."""
    writername = writername.lower()
    if _writer_aliases.has_key(writername):
        writername = _writer_aliases[writername]
    module = __import__(writername, globals(), locals())
    return module.Writer
