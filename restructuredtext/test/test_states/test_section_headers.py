#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/01 17:01:40 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite(id=__file__)
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
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
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
        </title>
        <paragraph>
            Paragraph (no blank line).
        </paragraph>
    </section>
</document>
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
    </paragraph>
    <section name="title">
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
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
    </paragraph>
    <block_quote>
        <system_warning level="3">
            <paragraph>
                Unexpected section title at line 4.
            </paragraph>
        </system_warning>
        <paragraph>
            Paragraph.
        </paragraph>
    </block_quote>
</document>
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
        </paragraph>
    </system_warning>
    <section name="title">
        <title>
            Title
        </title>
        <paragraph>
            Test short underline.
        </paragraph>
    </section>
</document>
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
        </title>
        <paragraph>
            Test overline title.
        </paragraph>
    </section>
</document>
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
        </title>
        <paragraph>
            Test overline title with inset.
        </paragraph>
    </section>
</document>
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
        </paragraph>
    </system_warning>
    <system_warning level="3">
        <paragraph>
            Missing underline for overline at line 1.
        </paragraph>
    </system_warning>
</document>
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
        </paragraph>
    </system_warning>
    <paragraph>
        Test missing underline, with paragraph.
    </paragraph>
</document>
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
        </paragraph>
    </system_warning>
    <section name="long title">
        <title>
            Long    Title
        </title>
        <paragraph>
            Test long title and space normalization.
        </paragraph>
    </section>
</document>
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
        </paragraph>
    </system_warning>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
Test return to existing, highest-level section (Title 3).

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
    <paragraph>
        Test return to existing, highest-level section (Title 3).
    </paragraph>
    <section name="title 1">
        <title>
            Title 1
        </title>
        <paragraph>
            Paragraph 1.
        </paragraph>
        <section name="title 2">
            <title>
                Title 2
            </title>
            <paragraph>
                Paragraph 2.
            </paragraph>
        </section>
    </section>
    <section name="title 3">
        <title>
            Title 3
        </title>
        <paragraph>
            Paragraph 3.
        </paragraph>
        <section name="title 4">
            <title>
                Title 4
            </title>
            <paragraph>
                Paragraph 4.
            </paragraph>
        </section>
    </section>
</document>
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
    </paragraph>
    <section name="title 1">
        <title>
            Title 1
        </title>
        <paragraph>
            Paragraph 1.
        </paragraph>
        <section name="title 2">
            <title>
                Title 2
            </title>
            <paragraph>
                Paragraph 2.
            </paragraph>
        </section>
    </section>
    <section name="title 3">
        <title>
            Title 3
        </title>
        <paragraph>
            Paragraph 3.
        </paragraph>
        <section name="title 4">
            <title>
                Title 4
            </title>
            <paragraph>
                Paragraph 4.
            </paragraph>
        </section>
    </section>
</document>
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
    </paragraph>
    <section name="title 1">
        <title>
            Title 1
        </title>
        <paragraph>
            Paragraph 1.
        </paragraph>
        <section name="title 2">
            <title>
                Title 2
            </title>
            <paragraph>
                Paragraph 2.
            </paragraph>
            <section name="title 3">
                <title>
                    Title 3
                </title>
                <paragraph>
                    Paragraph 3.
                </paragraph>
            </section>
        </section>
        <section name="title 4">
            <title>
                Title 4
            </title>
            <paragraph>
                Paragraph 4.
            </paragraph>
        </section>
    </section>
</document>
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
    </paragraph>
    <section name="title 1">
        <title>
            Title 1
        </title>
        <paragraph>
            Paragraph 1.
        </paragraph>
        <section name="title 2">
            <title>
                Title 2
            </title>
            <paragraph>
                Paragraph 2.
            </paragraph>
        </section>
    </section>
    <section name="title 3">
        <title>
            Title 3
        </title>
        <paragraph>
            Paragraph 3.
        </paragraph>
        <system_warning level="3">
            <paragraph>
                <strong>
                    ABORT
                </strong>
                : Title level inconsistent at line 15:
            </paragraph>
            <literal_block>
                Title 4
                ```````
            </literal_block>
        </system_warning>
        <paragraph>
            Paragraph 4.
        </paragraph>
    </section>
</document>
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
    </paragraph>
    <section name="title 1">
        <title>
            Title 1
        </title>
        <paragraph>
            Paragraph 1.
        </paragraph>
        <section name="title 2">
            <title>
                Title 2
            </title>
            <paragraph>
                Paragraph 2.
            </paragraph>
        </section>
    </section>
    <section name="title 3">
        <title>
            Title 3
        </title>
        <paragraph>
            Paragraph 3.
        </paragraph>
        <system_warning level="3">
            <paragraph>
                <strong>
                    ABORT
                </strong>
                : Title level inconsistent at line 19:
            </paragraph>
            <literal_block>
                ```````
                Title 4
                ```````
            </literal_block>
        </system_warning>
        <paragraph>
            Paragraph 4.
        </paragraph>
    </section>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
