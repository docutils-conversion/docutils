#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/09/07 01:47:00 $
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
    </paragraph>
    <field_list>
        <field>
            <field_name>
                Author
            </field_name>
            <field_body>
                <paragraph>
                    Me
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Version
            </field_name>
            <field_body>
                <paragraph>
                    1
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Date
            </field_name>
            <field_body>
                <paragraph>
                    2001-08-11
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Parameter
            </field_name>
            <field_argument>
                i
            </field_argument>
            <field_body>
                <paragraph>
                    integer
                </paragraph>
            </field_body>
        </field>
    </field_list>
</document>
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
    </paragraph>
    <field_list>
        <field>
            <field_name>
                Author
            </field_name>
            <field_body>
                <paragraph>
                    Me
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Version
            </field_name>
            <field_body>
                <paragraph>
                    1
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Date
            </field_name>
            <field_body>
                <paragraph>
                    2001-08-11
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Parameter
            </field_name>
            <field_argument>
                i
            </field_argument>
            <field_body>
                <paragraph>
                    integer
                </paragraph>
            </field_body>
        </field>
    </field_list>
</document>
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
            </field_name>
            <field_body/>
        </field>
    </field_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
        </paragraph>
    </system_warning>
    <paragraph>
        empty item above, no blank line
    </paragraph>
</document>
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
    </paragraph>
    <field_list>
        <field>
            <field_name>
                Author
            </field_name>
            <field_body>
                <paragraph>
                    Me
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Version
            </field_name>
            <field_body>
                <paragraph>
                    1
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Date
            </field_name>
            <field_body>
                <paragraph>
                    2001-08-11
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Parameter
            </field_name>
            <field_argument>
                i
            </field_argument>
            <field_body>
                <paragraph>
                    integer
                </paragraph>
            </field_body>
        </field>
    </field_list>
</document>
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
    </paragraph>
    <field_list>
        <field>
            <field_name>
                Authors
            </field_name>
            <field_body>
                <paragraph>
                    Me,
                    Myself,
                    and I
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Version
            </field_name>
            <field_body>
                <paragraph>
                    1
                    or so
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Date
            </field_name>
            <field_body>
                <paragraph>
                    2001-08-11
                    (Saturday)
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Parameter
            </field_name>
            <field_argument>
                i
            </field_argument>
            <field_body>
                <paragraph>
                    counter
                    (integer)
                </paragraph>
            </field_body>
        </field>
    </field_list>
</document>
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
    </paragraph>
    <field_list>
        <field>
            <field_name>
                Authors
            </field_name>
            <field_body>
                <paragraph>
                    Me,
                    Myself,
                    and I
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Version
            </field_name>
            <field_body>
                <paragraph>
                    1
                    or so
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Date
            </field_name>
            <field_body>
                <paragraph>
                    2001-08-11
                    (Saturday)
                </paragraph>
            </field_body>
        </field>
        <field>
            <field_name>
                Parameter
            </field_name>
            <field_argument>
                i
            </field_argument>
            <field_body>
                <paragraph>
                    counter
                    (integer)
                </paragraph>
            </field_body>
        </field>
    </field_list>
</document>
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
    </paragraph>
    <field_list>
        <field>
            <field_name>
                Authors
            </field_name>
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            Me
                        </paragraph>
                    </list_item>
                    <list_item>
                        <paragraph>
                            Myself
                        </paragraph>
                    </list_item>
                    <list_item>
                        <paragraph>
                            I
                        </paragraph>
                    </list_item>
                </bullet_list>
            </field_body>
        </field>
        <field>
            <field_name>
                Abstract
            </field_name>
            <field_body>
                <paragraph>
                    This is a field list item's body,
                    containing multiple elements.
                </paragraph>
                <paragraph>
                    Here's a literal block:
                </paragraph>
                <literal_block>
                    def f(x):
                        return x**2 + x
                </literal_block>
                <paragraph>
                    Even nested field lists are possible:
                </paragraph>
                <field_list>
                    <field>
                        <field_name>
                            Date
                        </field_name>
                        <field_body>
                            <paragraph>
                                2001-08-11
                            </paragraph>
                        </field_body>
                    </field>
                    <field>
                        <field_name>
                            Day
                        </field_name>
                        <field_body>
                            <paragraph>
                                Saturday
                            </paragraph>
                        </field_body>
                    </field>
                    <field>
                        <field_name>
                            Time
                        </field_name>
                        <field_body>
                            <paragraph>
                                15:07
                            </paragraph>
                        </field_body>
                    </field>
                </field_list>
            </field_body>
        </field>
    </field_list>
</document>
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
            </field_name>
            <field_argument>
                i
            </field_argument>
            <field_argument>
                j
            </field_argument>
            <field_argument>
                k
            </field_argument>
            <field_body>
                <paragraph>
                    multiple arguments
                </paragraph>
            </field_body>
        </field>
    </field_list>
</document>
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
    </paragraph>
    <field_list>
        <field>
            <field_name>
                Empty
            </field_name>
            <field_body/>
        </field>
        <field>
            <field_name>
                Author
            </field_name>
            <field_body>
                <paragraph>
                    Me
                </paragraph>
            </field_body>
        </field>
    </field_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
        </paragraph>
    </system_warning>
    <paragraph>
        No blank line before this paragraph.
    </paragraph>
    <field_list>
        <field>
            <field_name>
                *Field*
            </field_name>
            <field_argument>
                `with`
            </field_argument>
            <field_argument>
                **inline**
            </field_argument>
            <field_argument>
                ``markup``
            </field_argument>
            <field_body>
                <paragraph>
                    inline markup shouldn't be recognized.
                </paragraph>
            </field_body>
        </field>
    </field_list>
    <paragraph>
        : Field: marker must not begin with whitespace.
    </paragraph>
    <paragraph>
        :Field : marker must not end with whitespace.
    </paragraph>
    <paragraph>
        Field: marker is missing its open-colon.
    </paragraph>
    <paragraph>
        :Field marker is missing its close-colon.
    </paragraph>
</document>
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
    </title>
    <author>
        Me
    </author>
    <version>
        1
    </version>
    <date>
        2001-08-11
    </date>
    <abstract>
        <paragraph>
            There can only be one abstract.
        </paragraph>
        <paragraph>
            It is automatically moved to the end of the other bibliographic elements.
        </paragraph>
    </abstract>
    <comment>
        Bibliographic element extraction.
    </comment>
    <field_list>
        <field>
            <field_name>
                Parameter
            </field_name>
            <field_argument>
                i
            </field_argument>
            <field_body>
                <paragraph>
                    integer
                </paragraph>
            </field_body>
        </field>
    </field_list>
</document>
"""],
["""\
.. Bibliographic element extraction.

Title
=====
:Title: Second Title
:Subtitle: The Title field should generate a warning
:Abstract: Abstract 1.
:Author: Me
:Version: 1
:Abstract: Abstract 2.
:Date: 2001-08-11
:Parameter i: integer
""",
"""\
<document name="title">
    <title>
        Title
    </title>
    <subtitle>
        The Title field should generate a warning
    </subtitle>
    <author>
        Me
    </author>
    <version>
        1
    </version>
    <date>
        2001-08-11
    </date>
    <abstract>
        <paragraph>
            Abstract 1.
        </paragraph>
    </abstract>
    <comment>
        Bibliographic element extraction.
    </comment>
    <field_list>
        <field>
            <field_name>
                Title
            </field_name>
            <field_body>
                <paragraph>
                    Second Title
                </paragraph>
                <system_warning level="2">
                    <paragraph>
                        Multiple document titles (bibliographic field "Title").
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
        <field>
            <field_name>
                Abstract
            </field_name>
            <field_body>
                <paragraph>
                    Abstract 2.
                </paragraph>
                <system_warning level="2">
                    <paragraph>
                        There can only be one abstract.
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
        <field>
            <field_name>
                Parameter
            </field_name>
            <field_argument>
                i
            </field_argument>
            <field_body>
                <paragraph>
                    integer
                </paragraph>
            </field_body>
        </field>
    </field_list>
</document>
"""],
["""\
:Author: - must be a paragraph
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
            </field_name>
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            must be a paragraph
                        </paragraph>
                    </list_item>
                </bullet_list>
                <system_warning level="2">
                    <paragraph>
                        Cannot extract bibliographic field "Author" containing anything other than a simple paragraph.
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
        <field>
            <field_name>
                Date
            </field_name>
            <field_body>
                <paragraph>
                    But only one
                </paragraph>
                <paragraph>
                    paragraph.
                </paragraph>
                <system_warning level="2">
                    <paragraph>
                        Cannot extract compound title bibliographic field "Date".
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
        <field>
            <field_name>
                Version
            </field_name>
            <field_body>
                <system_warning level="2">
                    <paragraph>
                        Cannot extract empty bibliographic field "Version".
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
    </field_list>
    <comment>
        and not empty either
    </comment>
</document>
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
        </author>
        <author>
            Myself
        </author>
        <author>
            I
        </author>
    </authors>
    <authors>
        <author>
            PacMan
        </author>
        <author>
            Ms. PacMan
        </author>
        <author>
            PacMan, Jr.
        </author>
    </authors>
    <authors>
        <author>
            Here
        </author>
        <author>
            There
        </author>
        <author>
            <emphasis>
                Everywhere
            </emphasis>
        </author>
    </authors>
    <authors>
        <author>
            First
        </author>
        <author>
            Second
        </author>
        <author>
            Third
        </author>
    </authors>
</document>
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
            </field_name>
            <field_body>
                <system_warning level="2">
                    <paragraph>
                        Cannot extract empty bibliographic field "Authors".
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
        <field>
            <field_name>
                Authors
            </field_name>
            <field_body>
                <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
                    <list_item>
                        <paragraph>
                            One
                        </paragraph>
                    </list_item>
                    <list_item>
                        <paragraph>
                            Two
                        </paragraph>
                    </list_item>
                </enumerated_list>
                <system_warning level="2">
                    <paragraph>
                        Bibliographic field "Authors" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of ";,"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
        <field>
            <field_name>
                Authors
            </field_name>
            <field_body>
                <bullet_list bullet="-">
                    <list_item/>
                    <list_item/>
                </bullet_list>
                <system_warning level="2">
                    <paragraph>
                        Bibliographic field "Authors" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of ";,"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
        <field>
            <field_name>
                Authors
            </field_name>
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            One
                        </paragraph>
                    </list_item>
                </bullet_list>
                <paragraph>
                    Two
                </paragraph>
                <system_warning level="2">
                    <paragraph>
                        Bibliographic field "Authors" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of ";,"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
        <field>
            <field_name>
                Authors
            </field_name>
            <field_body>
                <bullet_list bullet="-">
                    <list_item>
                        <paragraph>
                            One
                        </paragraph>
                        <paragraph>
                            Two
                        </paragraph>
                    </list_item>
                </bullet_list>
                <system_warning level="2">
                    <paragraph>
                        Bibliographic field "Authors" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of ";,"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.
                    </paragraph>
                </system_warning>
            </field_body>
        </field>
    </field_list>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
