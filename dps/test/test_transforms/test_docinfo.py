#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/01/26 00:07:53 $
:Copyright: This module has been placed in the public domain.

Tests for dps.transforms.frontmatter.DocInfo.
"""

import DPSTestSupport
from dps.transforms.frontmatter import DocInfo
import UnitTestFolder
try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser


def suite():
    parser = Parser(warninglevel=4, errorlevel=4, languagecode='en',
                    debug=UnitTestFolder.debug)
    s = DPSTestSupport.TransformTestSuite(parser)
    s.generateTests(totest)
    return s

totest = {}

totest['bibliographic_field_lists'] = ((DocInfo,), [
["""\
.. Bibliographic element extraction.

:Abstract:
    There can only be one abstract.

    It is automatically moved to the end of the other bibliographic elements.

:Author: Me
:Version: 1
:Date: 2001-08-11
:Parameter i: integer
""",
"""\
<document>
    <docinfo>
        <author>
            Me
        <version>
            1
        <date>
            2001-08-11
        <abstract>
            <paragraph>
                There can only be one abstract.
            <paragraph>
                It is automatically moved to the end of the other bibliographic elements.
    <comment>
        Bibliographic element extraction.
    <field_list>
        <field>
            <field_name>
                Parameter
            <field_argument>
                i
            <field_body>
                <paragraph>
                    integer
"""],
["""\
.. Bibliographic element extraction.

:Abstract: Abstract 1.
:Author: Me
:Contact: me@my.org
:Version: 1
:Abstract: Abstract 2 (should generate a warning).
:Date: 2001-08-11
:Parameter i: integer
""",
"""\
<document>
    <docinfo>
        <author>
            Me
        <contact>
            <reference refuri="mailto:me@my.org">
                me@my.org
        <version>
            1
        <date>
            2001-08-11
        <abstract>
            <paragraph>
                Abstract 1.
    <comment>
        Bibliographic element extraction.
    <field_list>
        <field>
            <field_name>
                Abstract
            <field_body>
                <paragraph>
                    Abstract 2 (should generate a warning).
                <system_warning level="2">
                    <paragraph>
                        There can only be one abstract.
        <field>
            <field_name>
                Parameter
            <field_argument>
                i
            <field_body>
                <paragraph>
                    integer
"""],
["""\
:Author: - must be a paragraph
:Status: a *simple* paragraph
:Date: But only one

       paragraph.
:Version:

.. and not empty either
""",
"""\
<document>
    <docinfo>
        <status>
            a \n\
            <emphasis>
                simple
             paragraph
    <field_list>
        <field>
            <field_name>
                Author
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            must be a paragraph
                <system_warning level="2">
                    <paragraph>
                        Cannot extract bibliographic field "Author" containing anything other than a single paragraph.
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    But only one
                <paragraph>
                    paragraph.
                <system_warning level="2">
                    <paragraph>
                        Cannot extract compound bibliographic field "Date".
        <field>
            <field_name>
                Version
            <field_body>
                <system_warning level="2">
                    <paragraph>
                        Cannot extract empty bibliographic field "Version".
    <comment>
        and not empty either
"""],
["""\
:Authors: Me, Myself, **I**
:Authors: PacMan; Ms. PacMan; PacMan, Jr.
:Authors:
    Here

    There

    *Everywhere*
:Authors: - First
          - Second
          - Third
""",
"""\
<document>
    <docinfo>
        <authors>
            <author>
                Me
            <author>
                Myself
            <author>
                I
        <authors>
            <author>
                PacMan
            <author>
                Ms. PacMan
            <author>
                PacMan, Jr.
        <authors>
            <author>
                Here
            <author>
                There
            <author>
                <emphasis>
                    Everywhere
        <authors>
            <author>
                First
            <author>
                Second
            <author>
                Third
"""],
["""\
:Authors:

:Authors: 1. One
          2. Two

:Authors:
    -
    -

:Authors:
    - One

    Two

:Authors:
    - One

      Two
""",
"""\
<document>
    <field_list>
        <field>
            <field_name>
                Authors
            <field_body>
                <system_warning level="2">
                    <paragraph>
                        Cannot extract empty bibliographic field "Authors".
        <field>
            <field_name>
                Authors
            <field_body>
                <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
                    <list_item>
                        <paragraph>
                            One
                    <list_item>
                        <paragraph>
                            Two
                <system_warning level="2">
                    <paragraph>
                        Bibliographic field "Authors" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of ";,"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.
        <field>
            <field_name>
                Authors
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                    <list_item>
                <system_warning level="2">
                    <paragraph>
                        Bibliographic field "Authors" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of ";,"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.
        <field>
            <field_name>
                Authors
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            One
                <paragraph>
                    Two
                <system_warning level="2">
                    <paragraph>
                        Bibliographic field "Authors" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of ";,"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.
        <field>
            <field_name>
                Authors
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            One
                        <paragraph>
                            Two
                <system_warning level="2">
                    <paragraph>
                        Bibliographic field "Authors" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of ";,"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.
"""],
["""\
.. RCS keyword extraction.

:Status: $RCSfile: test_docinfo.py,v $
:Date: $Date: 2002/01/26 00:07:53 $

RCS keyword 'RCSfile' doesn't change unless the file name changes,
so it's safe. The 'Date' keyword changes every time the file is
checked in to CVS, so the test's expected output text has to be
derived (hacked) in parallel in order to stay in sync.
""",
"""\
<document>
    <docinfo>
        <status>
            test_docinfo.py
        <date>
            %s
    <comment>
        RCS keyword extraction.
    <paragraph>
        RCS keyword 'RCSfile' doesn't change unless the file name changes,
        so it's safe. The 'Date' keyword changes every time the file is
        checked in to CVS, so the test's expected output text has to be
        derived (hacked) in parallel in order to stay in sync.
""" % ('$Date: 2002/01/26 00:07:53 $'[7:17].replace('/', '-'),)],
])

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
