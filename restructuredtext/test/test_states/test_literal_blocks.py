#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/01 17:00:38 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite(id=__file__)
    s.generateTests(totest)
    return s

totest = {}

totest['literal_blocks'] = [
["""\
A paragraph::

    A literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
</document>
"""],
["""\
A paragraph
on more than
one line::

    A literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph
        on more than
        one line:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
</document>
"""],
["""\
A paragraph
on more than
one line::
    A literal block
    with no blank line above.
""",
"""\
<document>
    <paragraph>
        A paragraph
        on more than
        one line:
    </paragraph>
    <system_warning level="2">
        <paragraph>
            Unexpected indentation at line 4.
        </paragraph>
    </system_warning>
    <literal_block>
        A literal block
        with no blank line above.
    </literal_block>
</document>
"""],
["""\
A paragraph::

    A literal block.
no blank line
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
</document>
"""],
["""\
A paragraph: ::

    A literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
</document>
"""],
["""\
A paragraph:

::

    A literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
</document>
"""],
["""\
A paragraph::

Not a literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Literal block expected at line 2; none found.
        </paragraph>
    </system_warning>
    <paragraph>
        Not a literal block.
    </paragraph>
</document>
"""],
["""\
A paragraph::

    A wonky literal block.
  Literal line 2.

    Literal line 3.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
          A wonky literal block.
        Literal line 2.
        
          Literal line 3.
    </literal_block>
</document>
"""],
["""\
EOF, even though a literal block is indicated::
""",
"""\
<document>
    <paragraph>
        EOF, even though a literal block is indicated:
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Literal block expected at line 2; none found.
        </paragraph>
    </system_warning>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
