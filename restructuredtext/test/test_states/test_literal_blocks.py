#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/09/13 02:40:31 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
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
    <literal_block>
        A literal block.
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
    <literal_block>
        A literal block.
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
    <system_warning level="2">
        <paragraph>
            Unexpected indentation at line 4.
    <literal_block>
        A literal block
        with no blank line above.
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
    <literal_block>
        A literal block.
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
    <paragraph>
        no blank line
"""],
["""\
A paragraph: ::

    A literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    <literal_block>
        A literal block.
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
    <literal_block>
        A literal block.
"""],
["""\
A paragraph::

Not a literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    <system_warning level="1">
        <paragraph>
            Literal block expected at line 2; none found.
    <paragraph>
        Not a literal block.
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
    <literal_block>
          A wonky literal block.
        Literal line 2.
        
          Literal line 3.
"""],
["""\
EOF, even though a literal block is indicated::
""",
"""\
<document>
    <paragraph>
        EOF, even though a literal block is indicated:
    <system_warning level="1">
        <paragraph>
            Literal block expected at line 2; none found.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
