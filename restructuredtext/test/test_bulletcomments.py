#! /usr/bin/env python

"""
Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1.2.1 $
Date: $Date: 2001/07/31 15:25:01 $
Copyright: This module has been placed in the public domain.

Test comments in bullets.
"""

from TestFramework import *
import ParserTestCase

def suite():
    f = ParserTestCase.ParserTestCaseFactory('outdenting')

    totest = {}
    
    totest['comments_in_bullets'] = [
["""\
+ bullet paragraph 1

  bullet paragraph 2

  .. comment between bullet paragraphs 2 and 3

  bullet paragraph 3
""",
"""\
<document>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet paragraph 1
            </paragraph>
            <paragraph>
                bullet paragraph 2
            </paragraph>
            <comment>
                comment between bullet paragraphs 2 and 3
            </comment>
            <paragraph>
                bullet paragraph 3
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
+ bullet paragraph 1

  .. comment between bullet paragraphs 1 (leader) and 2

  bullet paragraph 2
""",
"""\
<document>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet paragraph 1
            </paragraph>
            <comment>
                comment between bullet paragraphs 1 (leader) and 2
            </comment>
            <paragraph>
                bullet paragraph 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
+ bullet

  .. trailing comment
""",
"""\
<document>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                bullet
            </paragraph>
            <comment>
                trailing comment
            </comment>
        </list_item>
    </bullet_list>
</document>
"""],
]

    f.stockFactory(totest)
    return f

if __name__ == '__main__':
    main(suite=suite())
