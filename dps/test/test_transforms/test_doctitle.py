#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.5 $
:Date: $Date: 2002/02/15 22:45:58 $
:Copyright: This module has been placed in the public domain.

Tests for dps.transforms.frontmatter.DocTitle.
"""

import DPSTestSupport
from dps.transforms.frontmatter import DocTitle
import UnitTestFolder
try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser


def suite():
    parser = Parser()
    s = DPSTestSupport.TransformTestSuite(parser)
    s.generateTests(totest)
    return s

totest = {}

totest['section_headers'] = ((DocTitle,), [
["""\
.. test title promotion

Title
=====

Paragraph.
""",
"""\
<document name="title">
    <title>
        Title
    <comment>
        test title promotion
    <paragraph>
        Paragraph.
"""],
["""\
Title
=====
Paragraph (no blank line).
""",
"""\
<document name="title">
    <title>
        Title
    <paragraph>
        Paragraph (no blank line).
"""],
["""\
Paragraph.

Title
=====

Paragraph.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    <section name="title">
        <title>
            Title
        <paragraph>
            Paragraph.
"""],
["""\
Title
=====

Subtitle
--------

Test title & subtitle.
""",
"""\
<document name="title">
    <title>
        Title
    <subtitle name="subtitle">
        Subtitle
    <paragraph>
        Test title & subtitle.
"""],
["""\
Title
====

Test short underline.
""",
"""\
<document name="title">
    <title>
        Title
    <system_message level="1" type="INFO">
        <paragraph>
            Title underline too short at line 2.
    <paragraph>
        Test short underline.
"""],
["""\
=======
 Long    Title
=======

Test long title and space normalization.
The system_message should move after the document title
(it was before the beginning of the section).
""",
"""\
<document name="long title">
    <title>
        Long    Title
    <system_message level="1" type="INFO">
        <paragraph>
            Title overline too short at line 1.
    <paragraph>
        Test long title and space normalization.
        The system_message should move after the document title
        (it was before the beginning of the section).
"""],
["""\
.. Test multiple second-level titles.

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
-------
Paragraph 3.
""",
"""\
<document name="title 1">
    <title>
        Title 1
    <comment>
        Test multiple second-level titles.
    <paragraph>
        Paragraph 1.
    <section name="title 2">
        <title>
            Title 2
        <paragraph>
            Paragraph 2.
    <section name="title 3">
        <title>
            Title 3
        <paragraph>
            Paragraph 3.
"""],
])

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
