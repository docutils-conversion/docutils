#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:00:50 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['block_quotes'] = [
["""\
Line 1.
Line 2.

   Indented.
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
    </paragraph>
    <block_quote>
        <paragraph>
            Indented.
        </paragraph>
    </block_quote>
</document>
"""],
["""\
Line 1.
Line 2.

   Indented 1.

      Indented 2.
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
    </paragraph>
    <block_quote>
        <paragraph>
            Indented 1.
        </paragraph>
        <block_quote>
            <paragraph>
                Indented 2.
            </paragraph>
        </block_quote>
    </block_quote>
</document>
"""],
["""\
Line 1.
Line 2.
    Unexpectedly indented.
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
    </paragraph>
    <system_warning level="2">
        <paragraph>
            Unexpected indentation at line 3.
        </paragraph>
    </system_warning>
    <block_quote>
        <paragraph>
            Unexpectedly indented.
        </paragraph>
    </block_quote>
</document>
"""],
["""\
Line 1.
Line 2.

   Indented.
no blank line
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
    </paragraph>
    <block_quote>
        <paragraph>
            Indented.
        </paragraph>
    </block_quote>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 5.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
</document>
"""],
["""\
Here is a paragraph.

        Indent 8 spaces.

    Indent 4 spaces.

Is this correct? Should it generate a warning?
Yes, it is correct, no warning necessary.
""",
"""\
<document>
    <paragraph>
        Here is a paragraph.
    </paragraph>
    <block_quote>
        <block_quote>
            <paragraph>
                Indent 8 spaces.
            </paragraph>
        </block_quote>
        <paragraph>
            Indent 4 spaces.
        </paragraph>
    </block_quote>
    <paragraph>
        Is this correct? Should it generate a warning?
        Yes, it is correct, no warning necessary.
    </paragraph>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
