#! /usr/bin/env python
"""
:Authors: David Goodger, Ueli Schlaepfer
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/03/01 03:13:37 $
:Copyright: This module has been placed in the public domain.

Transforms needed by most or all documents:

- `Messages`: Placement of system messages stored in
  `nodes.document.messages`.
"""

__docformat__ = 'reStructuredText'

import re
from dps import nodes, utils
from dps.transforms import TransformError, Transform


class Messages(Transform):

    """
    Place any system messages generated after parsing into a dedicated section
    of the document.
    """

    def transform(self, doctree):
        self.setup_transform(doctree)
        if len(doctree.messages) > 0:
            section = nodes.section(CLASS='system_messages')
            # @@@ get this from the language module?
            section += nodes.title('', 'Docutils System Messages')
            section += doctree.messages.getchildren()
            doctree += section


class TestMessages(Transform):

    """
    Append all system messages to the end of the doctree.
    """

    def transform(self, doctree):
        self.setup_transform(doctree)
        doctree += doctree.messages.getchildren()


test_transforms = (TestMessages,)
"""Tuple of universal transforms to apply to the raw doctree when testing."""

first_reader_transforms = ()
"""Tuple of universal transforms to apply before any other Reader transforms."""

last_reader_transforms = (Messages,)
"""Tuple of universal transforms to apply after all other Reader transforms."""

first_writer_transforms = ()
"""Tuple of universal transforms to apply before any other Writer transforms."""

last_writer_transforms = ()
"""Tuple of universal transforms to apply after all other Writer transforms."""
