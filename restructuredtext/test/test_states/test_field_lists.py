#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.6 $
:Date: $Date: 2001/09/18 21:24:27 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['field_lists'] = [
["""\
One-liners:

:Author: Me

:Version: 1

:Date: 2001-08-11

:Parameter i: integer
""",
"""\
<document>
    <paragraph>
        One-liners:
    <field_list>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
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
One-liners, no blank lines:

:Author: Me
:Version: 1
:Date: 2001-08-11
:Parameter i: integer
""",
"""\
<document>
    <paragraph>
        One-liners, no blank lines:
    <field_list>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
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
:field:
empty item above, no blank line
""",
"""\
<document>
    <field_list>
        <field>
            <field_name>
                field
            <field_body>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
    <paragraph>
        empty item above, no blank line
"""],
["""\
Field bodies starting on the next line:

:Author:
  Me
:Version:
  1
:Date:
  2001-08-11
:Parameter i:
  integer
""",
"""\
<document>
    <paragraph>
        Field bodies starting on the next line:
    <field_list>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
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
One-paragraph, multi-liners:

:Authors: Me,
          Myself,
          and I
:Version: 1
          or so
:Date: 2001-08-11
       (Saturday)
:Parameter i: counter
              (integer)
""",
"""\
<document>
    <paragraph>
        One-paragraph, multi-liners:
    <field_list>
        <field>
            <field_name>
                Authors
            <field_body>
                <paragraph>
                    Me,
                    Myself,
                    and I
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
                    or so
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
                    (Saturday)
        <field>
            <field_name>
                Parameter
            <field_argument>
                i
            <field_body>
                <paragraph>
                    counter
                    (integer)
"""],
["""\
One-paragraph, multi-liners, not lined up:

:Authors: Me,
  Myself,
  and I
:Version: 1
  or so
:Date: 2001-08-11
  (Saturday)
:Parameter i: counter
  (integer)
""",
"""\
<document>
    <paragraph>
        One-paragraph, multi-liners, not lined up:
    <field_list>
        <field>
            <field_name>
                Authors
            <field_body>
                <paragraph>
                    Me,
                    Myself,
                    and I
        <field>
            <field_name>
                Version
            <field_body>
                <paragraph>
                    1
                    or so
        <field>
            <field_name>
                Date
            <field_body>
                <paragraph>
                    2001-08-11
                    (Saturday)
        <field>
            <field_name>
                Parameter
            <field_argument>
                i
            <field_body>
                <paragraph>
                    counter
                    (integer)
"""],
["""\
Multiple body elements:

:Authors: - Me
          - Myself
          - I

:Abstract:
    This is a field list item's body,
    containing multiple elements.

    Here's a literal block::

        def f(x):
            return x**2 + x

    Even nested field lists are possible:

    :Date: 2001-08-11
    :Day: Saturday
    :Time: 15:07
""",
"""\
<document>
    <paragraph>
        Multiple body elements:
    <field_list>
        <field>
            <field_name>
                Authors
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            Me
                    <list_item>
                        <paragraph>
                            Myself
                    <list_item>
                        <paragraph>
                            I
        <field>
            <field_name>
                Abstract
            <field_body>
                <paragraph>
                    This is a field list item's body,
                    containing multiple elements.
                <paragraph>
                    Here's a literal block:
                <literal_block>
                    def f(x):
                        return x**2 + x
                <paragraph>
                    Even nested field lists are possible:
                <field_list>
                    <field>
                        <field_name>
                            Date
                        <field_body>
                            <paragraph>
                                2001-08-11
                    <field>
                        <field_name>
                            Day
                        <field_body>
                            <paragraph>
                                Saturday
                    <field>
                        <field_name>
                            Time
                        <field_body>
                            <paragraph>
                                15:07
"""],
["""\
:Parameter i j k: multiple arguments
""",
"""\
<document>
    <field_list>
        <field>
            <field_name>
                Parameter
            <field_argument>
                i
            <field_argument>
                j
            <field_argument>
                k
            <field_body>
                <paragraph>
                    multiple arguments
"""],
["""\
Some edge cases:

:Empty:
:Author: Me
No blank line before this paragraph.

:*Field* `with` **inline** ``markup``: inline markup shouldn't be recognized.

: Field: marker must not begin with whitespace.

:Field : marker must not end with whitespace.

Field: marker is missing its open-colon.

:Field marker is missing its close-colon.
""",
"""\
<document>
    <paragraph>
        Some edge cases:
    <field_list>
        <field>
            <field_name>
                Empty
            <field_body>
        <field>
            <field_name>
                Author
            <field_body>
                <paragraph>
                    Me
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
    <paragraph>
        No blank line before this paragraph.
    <field_list>
        <field>
            <field_name>
                *Field*
            <field_argument>
                `with`
            <field_argument>
                **inline**
            <field_argument>
                ``markup``
            <field_body>
                <paragraph>
                    inline markup shouldn't be recognized.
    <paragraph>
        : Field: marker must not begin with whitespace.
    <paragraph>
        :Field : marker must not end with whitespace.
    <paragraph>
        Field: marker is missing its open-colon.
    <paragraph>
        :Field marker is missing its close-colon.
"""],
]

totest['bibliographic_field_lists'] = [
["""\
.. Bibliographic element extraction.

:Title: Document Title
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
    <title>
        Document Title
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

Title
=====
:Title: Second Title (this should generate a warning)
:Subtitle: First Subtitle
:Abstract: Abstract 1.
:Author: Me
:Version: 1
:Abstract: Abstract 2 (should generate a warning).
:Date: 2001-08-11
:Parameter i: integer
:Subtitle: Second Subtitle (should generate a warning)
""",
"""\
<document name="title">
    <title>
        Title
    <subtitle>
        First Subtitle
    <author>
        Me
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
                Title
            <field_body>
                <paragraph>
                    Second Title (this should generate a warning)
                <system_warning level="2">
                    <paragraph>
                        Multiple document titles (bibliographic field "Title").
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
        <field>
            <field_name>
                Subtitle
            <field_body>
                <paragraph>
                    Second Subtitle (should generate a warning)
                <system_warning level="2">
                    <paragraph>
                        Multiple document subtitles (bibliographic field "Subtitle").
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
                        Cannot extract bibliographic field "Author" containing anything other than a simple, unformatted paragraph.
        <field>
            <field_name>
                Status
            <field_body>
                <paragraph>
                    a 
                    <emphasis>
                        simple
                     paragraph
                <system_warning level="2">
                    <paragraph>
                        Cannot extract bibliographic field "Status" containing anything other than a simple, unformatted paragraph.
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

:Title: $RCSfile: test_field_lists.py,v $
:Date: $Date: 2001/09/18 21:24:27 $

RCS keyword 'RCSfile' doesn't change unless the file name changes,
so it's safe. The 'Date' keyword changes every time the file is
checked in to CVS, so the test's expected output text has to be
derived (hacked) in parallel in order to stay in sync.
""",
"""\
<document>
    <title>
        test_field_lists.py
    <date>
        %s
    <comment>
        RCS keyword extraction.
    <paragraph>
        RCS keyword 'RCSfile' doesn't change unless the file name changes,
        so it's safe. The 'Date' keyword changes every time the file is
        checked in to CVS, so the test's expected output text has to be
        derived (hacked) in parallel in order to stay in sync.
""" % ('$Date: 2001/09/18 21:24:27 $'[7:17].replace('/', '-'),)],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
