#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.11 $
:Date: $Date: 2002/01/25 23:43:41 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['section_headers'] = [
["""\
Title
=====

Paragraph.
""",
"""\
<document>
    <section name="title">
        <title>
            Title
        <paragraph>
            Paragraph.
"""],
["""\
Title
=====
Paragraph (no blank line).
""",
"""\
<document>
    <section name="title">
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
Test unexpected section title.

    Title
    =====
    Paragraph.
""",
"""\
<document>
    <paragraph>
        Test unexpected section title.
    <block_quote>
        <system_warning level="3">
            <paragraph>
                Unexpected section title at line 4.
        <paragraph>
            Paragraph.
"""],
["""\
Title
====

Test short underline.
""",
"""\
<document>
    <system_warning level="0">
        <paragraph>
            Title underline too short at line 2.
    <section name="title">
        <title>
            Title
        <paragraph>
            Test short underline.
"""],
["""\
=====
Title
=====

Test overline title.
""",
"""\
<document>
    <section name="title">
        <title>
            Title
        <paragraph>
            Test overline title.
"""],
["""\
=======
 Title
=======

Test overline title with inset.
""",
"""\
<document>
    <section name="title">
        <title>
            Title
        <paragraph>
            Test overline title with inset.
"""],
["""\
========================
 Test Missing Underline
""",
"""\
<document>
    <system_warning level="3">
        <paragraph>
            Incomplete section title at line 1.
"""],
["""\
========================
 Test Missing Underline

""",
"""\
<document>
    <system_warning level="3">
        <paragraph>
            Missing underline for overline at line 1.
"""],
["""\
=======
 Title

Test missing underline, with paragraph.
""",
"""\
<document>
    <system_warning level="3">
        <paragraph>
            Missing underline for overline at line 1.
    <paragraph>
        Test missing underline, with paragraph.
"""],
["""\
=======
 Long    Title
=======

Test long title and space normalization.
""",
"""\
<document>
    <system_warning level="0">
        <paragraph>
            Title overline too short at line 1.
    <section name="long title">
        <title>
            Long    Title
        <paragraph>
            Test long title and space normalization.
"""],
["""\
=======
 Title
-------

Paragraph.
""",
"""\
<document>
    <system_warning level="3">
        <paragraph>
            Title overline & underline mismatch at line 1.
    <paragraph>
        Paragraph.
"""],
["""\
========================

========================

Test missing titles; blank line in-between.

========================

========================
""",
"""\
<document>
    <system_warning level="2">
        <paragraph>
            Document or section may not begin with a transition (line 1).
    <transition>
    <paragraph>
        Test missing titles; blank line in-between.
    <transition>
    <system_warning level="2">
        <paragraph>
            Document or section may not end with a transition (line 9).
"""],
["""\
========================
========================

Test missing titles; nothing in-between.

========================
========================
""",
"""\
<document>
    <system_warning level="2">
        <paragraph>
            Invalid section title or transition marker at line 1.
    <paragraph>
        Test missing titles; nothing in-between.
    <system_warning level="2">
        <paragraph>
            Invalid section title or transition marker at line 6.
"""],
["""\
.. Test return to existing, highest-level section (Title 3).

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
=======
Paragraph 3.

Title 4
-------
Paragraph 4.
""",
"""\
<document>
    <comment>
        Test return to existing, highest-level section (Title 3).
    <section name="title 1">
        <title>
            Title 1
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
        <section name="title 4">
            <title>
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
Test return to existing, highest-level section (Title 3, with overlines).

=======
Title 1
=======
Paragraph 1.

-------
Title 2
-------
Paragraph 2.

=======
Title 3
=======
Paragraph 3.

-------
Title 4
-------
Paragraph 4.
""",
"""\
<document>
    <paragraph>
        Test return to existing, highest-level section (Title 3, with overlines).
    <section name="title 1">
        <title>
            Title 1
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
        <section name="title 4">
            <title>
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
Test return to existing, higher-level section (Title 4).

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
```````
Paragraph 3.

Title 4
-------
Paragraph 4.
""",
"""\
<document>
    <paragraph>
        Test return to existing, higher-level section (Title 4).
    <section name="title 1">
        <title>
            Title 1
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
        <section name="title 4">
            <title>
                Title 4
            <paragraph>
                Paragraph 4.
"""],
["""\
Test bad subsection order (Title 4).

Title 1
=======
Paragraph 1.

Title 2
-------
Paragraph 2.

Title 3
=======
Paragraph 3.

Title 4
```````
Paragraph 4.
""",
"""\
<document>
    <paragraph>
        Test bad subsection order (Title 4).
    <section name="title 1">
        <title>
            Title 1
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
        <system_warning level="3">
            <paragraph>
                Title level inconsistent at line 15:
            <literal_block>
                Title 4
                ```````
        <paragraph>
            Paragraph 4.
"""],
["""\
Test bad subsection order (Title 4, with overlines).

=======
Title 1
=======
Paragraph 1.

-------
Title 2
-------
Paragraph 2.

=======
Title 3
=======
Paragraph 3.

```````
Title 4
```````
Paragraph 4.
""",
"""\
<document>
    <paragraph>
        Test bad subsection order (Title 4, with overlines).
    <section name="title 1">
        <title>
            Title 1
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
        <system_warning level="3">
            <paragraph>
                Title level inconsistent at line 19:
            <literal_block>
                ```````
                Title 4
                ```````
        <paragraph>
            Paragraph 4.
"""],
["""\
Title containing *inline* ``markup``
====================================

Paragraph.
""",
"""\
<document>
    <section name="title containing inline markup">
        <title>
            Title containing \n\
            <emphasis>
                inline
             \n\
            <literal>
                markup
        <paragraph>
            Paragraph.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
