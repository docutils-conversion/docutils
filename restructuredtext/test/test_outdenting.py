#! /usr/bin/env python

"""
Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1.2.1 $
Date: $Date: 2001/07/31 15:25:01 $
Copyright: This module has been placed in the public domain.

Test outdenting. 
"""

from TestFramework import *
import ParserTestCase

def suite():
    f = ParserTestCase.ParserTestCaseFactory('outdenting')

    f.addParserTestCase("""\
Anywhere a paragraph would have an effect on the current
indentation level, a comment or list item should also.

+ bullet

paragraph used to end a bullet before a blockquote

  blockquote
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
        paragraph used to end a bullet before a blockquote
    </paragraph>
    <block_quote>
        <paragraph>
            blockquote
        </paragraph>
    </block_quote>
</document>
""")

    f.addParserTestCase("""\
+ bullet

.. a comment used to end a bullet before a blockquote
   (if you can't think of what to write in the paragraph)

  blockquote
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
        a comment used to end a bullet before a blockquote
        (if you can't think of what to write in the paragraph)
    </comment>
    <block_quote>
        <paragraph>
            blockquote
        </paragraph>
    </block_quote>
</document>
""")

    return f

if __name__ == '__main__':
    main(suite=suite())
