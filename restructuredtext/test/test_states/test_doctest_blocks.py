#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/01 16:58:28 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite(id=__file__)
    s.generateTests(totest)
    return s

totest = {}

totest['doctest_blocks'] = [
["""\
Paragraph.

>>> print "Doctest block."
Doctest block.

Paragraph.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    </paragraph>
    <doctest_block>
        >>> print "Doctest block."
        Doctest block.
    </doctest_block>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
Paragraph.

>>> print "    Indented output."
    Indented output.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    </paragraph>
    <doctest_block>
        >>> print "    Indented output."
            Indented output.
    </doctest_block>
</document>
"""],
["""\
Paragraph.

    >>> print "    Indented block & output."
        Indented block & output.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    </paragraph>
    <block_quote>
        <doctest_block>
            >>> print "    Indented block & output."
                Indented block & output.
        </doctest_block>
    </block_quote>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
