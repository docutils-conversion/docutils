#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:06:35 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['paragraphs'] = [
["""\
A paragraph.
""",
"""\
<document>
    <paragraph>
        A paragraph.
    </paragraph>
</document>
"""],
["""\
Paragraph 1.

Paragraph 2.
""",
"""\
<document>
    <paragraph>
        Paragraph 1.
    </paragraph>
    <paragraph>
        Paragraph 2.
    </paragraph>
</document>
"""],
["""\
Line 1.
Line 2.
Line 3.
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
        Line 3.
    </paragraph>
</document>
"""],
["""\
Paragraph 1, Line 1.
Line 2.
Line 3.

Paragraph 2, Line 1.
Line 2.
Line 3.
""",
"""\
<document>
    <paragraph>
        Paragraph 1, Line 1.
        Line 2.
        Line 3.
    </paragraph>
    <paragraph>
        Paragraph 2, Line 1.
        Line 2.
        Line 3.
    </paragraph>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
