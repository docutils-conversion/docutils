#! /usr/bin/env python
"""
:Authors: David Goodger, Ueli Schlaepfer
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.5 $
:Date: $Date: 2002/03/28 04:42:29 $
:Copyright: This module has been placed in the public domain.

Transforms needed by most or all documents:

- `Messages`: Placement of system messages stored in
  `nodes.document.messages`.
- `TestMessages`: Like `Messages`, used on test runs.
- `FinalReferences`: Resolve remaining references.
- `Pending`: Execute pending transforms (abstract base class;
  `FirstReaderPending`, `LastReaderPending`, `FirstWriterPending`, and
  `LastWriterPending` are its concrete subclasses).
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

    def transform(self):
        # @@@ filter out msgs below threshold?
        if len(self.doctree.messages) > 0:
            section = nodes.section(CLASS='system-messages')
            # @@@ get this from the language module?
            section += nodes.title('', 'Docutils System Messages')
            section += self.doctree.messages.getchildren()
            self.doctree.messages[:] = []
            self.doctree += section


class TestMessages(Transform):

    """
    Append all system messages to the end of the doctree.
    """

    def transform(self):
        self.doctree += self.doctree.messages.getchildren()


class FinalReferences(Transform):

    """
    Resolve any remaining references, check for dangling.
    """

    def transform(self):
        pass


class Pending(Transform):

    """
    Execute pending transforms.
    """

    stage = None
    """The stage of processing applicable to this transform; match with
    `nodes.pending.stage`.  Possible values include 'first_reader',
    'last_reader', 'first_writer', and 'last_writer'.  Override in
    subclasses."""

    def transform(self):
        for pending in self.doctree.pending:
            if pending.stage == self.stage:
                pending.transform(self.doctree, pending).transform()


class FirstReaderPending(Pending):

    stage = 'first_reader'


class LastReaderPending(Pending):

    stage = 'last_reader'


class FirstWriterPending(Pending):

    stage = 'first_writer'


class LastWriterPending(Pending):

    stage = 'last_writer'


test_transforms = (TestMessages,)
"""Universal transforms to apply to the raw doctree when testing."""

first_reader_transforms = (FirstReaderPending,)
"""Universal transforms to apply before any other Reader transforms."""

last_reader_transforms = (LastReaderPending,)
"""Universal transforms to apply after all other Reader transforms."""

first_writer_transforms = (FirstWriterPending,)
"""Universal transforms to apply before any other Writer transforms."""

last_writer_transforms = (LastWriterPending, FinalReferences, Messages)
"""Universal transforms to apply after all other Writer transforms."""
