#! /usr/bin/env python
"""
:Authors: David Goodger, Ueli Schlaepfer
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2002/02/06 02:51:25 $
:Copyright: This module has been placed in the public domain.

This package contains modules for standard tree transforms available
to DPS components. Tree transforms serve a variety of purposes:

- To tie up certain syntax-specific "loose ends" that remain after the
  initial parsing of the input plaintext. These transforms are used to
  supplement a limited syntax.

- To automate the internal linking of the document tree (hyperlink
  references, footnote references, etc.).

- To extract useful information from the document tree. These
  transforms may be used to construct (for example) indexes and tables
  of contents.

Each transform is an optional step that a DPS Reader may choose to perform on
the parsed document, depending on the input context. A DPS Reader may also
perform Reader-specific transforms before or after performing these standard
transforms.
"""

__docformat__ = 'reStructuredText'


from dps import languages


class TransformError(Exception): pass


class Transform:

    def transform(self, doctree):
        """Override to transform the document tree."""
        raise NotImplementedError('subclass must override this method')

    def setup_transform(self, doctree):
        """Initial setup, used by `self.transform()`."""
        self.doctree = doctree
        self.language = languages.getlanguage(doctree.languagecode)
