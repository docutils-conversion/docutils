#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:01:21 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['bullet_lists'] = [
["""\
- item
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
* item 1

* item 2
""",
"""\
<document>
    <bullet_list bullet="*">
        <list_item>
            <paragraph>
                item 1
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
No blank line between:

+ item 1
+ item 2
""",
"""\
<document>
    <paragraph>
        No blank line between:
    </paragraph>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                item 1
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
- item 1, para 1.

  item 1, para 2.

- item 2
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1, para 1.
            </paragraph>
            <paragraph>
                item 1, para 2.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
- item 1, line 1
  item 1, line 2
- item 2
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1, line 1
                item 1, line 2
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
Different bullets:

- item 1

+ item 2

* item 3
- item 4
""",
"""\
<document>
    <paragraph>
        Different bullets:
    </paragraph>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1
            </paragraph>
        </list_item>
    </bullet_list>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
    <bullet_list bullet="*">
        <list_item>
            <paragraph>
                item 3
            </paragraph>
        </list_item>
    </bullet_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 8.
        </paragraph>
    </system_warning>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 4
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
- item
no blank line
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item
            </paragraph>
        </list_item>
    </bullet_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
</document>
"""],
["""\
-

empty item above
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item/>
    </bullet_list>
    <paragraph>
        empty item above
    </paragraph>
</document>
"""],
["""\
-
empty item above, no blank line
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item/>
    </bullet_list>
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
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
