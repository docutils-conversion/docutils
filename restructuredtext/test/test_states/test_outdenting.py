#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/01 17:01:14 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite(id=__file__)
    s.generateTests(totest)
    return s

totest = {}

totest['outdenting'] = [
["""\
Anywhere a paragraph would have an effect on the current
indentation level, a comment or list item should also.

+ bullet

This paragraph ends the bullet list item before a block quote.

  Block quote.
""",
"""\
<document>
    <paragraph>
        Anywhere a paragraph would have an effect on the current
        indentation level, a comment or list item should also.
    </paragraph>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet
            </paragraph>
        </list_item>
    </bullet_list>
    <paragraph>
        This paragraph ends the bullet list item before a block quote.
    </paragraph>
    <block_quote>
        <paragraph>
            Block quote.
        </paragraph>
    </block_quote>
</document>
"""],
["""\
+ bullet

.. Comments swallow up all indented text following.

  (Therefore this is not a) block quote.

- bullet

  If we want a block quote after this bullet list item,
  we need to use an empty comment:

..

  Block quote.
""",
"""\
<document>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet
            </paragraph>
        </list_item>
    </bullet_list>
    <comment>
        Comments swallow up all indented text following.
        
        (Therefore this is not a) block quote.
    </comment>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                bullet
            </paragraph>
            <paragraph>
                If we want a block quote after this bullet list item,
                we need to use an empty comment:
            </paragraph>
        </list_item>
    </bullet_list>
    <comment/>
    <block_quote>
        <paragraph>
            Block quote.
        </paragraph>
    </block_quote>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
