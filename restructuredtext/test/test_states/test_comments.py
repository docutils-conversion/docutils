#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:01:49 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['comments'] = [
["""\
.. A comment

Paragraph.
""",
"""\
<document>
    <comment>
        A comment
    </comment>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. A comment
   block.

Paragraph.
""",
"""\
<document>
    <comment>
        A comment
        block.
    </comment>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
..
   A comment consisting of multiple lines
   starting on the line after the
   explicit markup start.
""",
"""\
<document>
    <comment>
        A comment consisting of multiple lines
        starting on the line after the
        explicit markup start.
    </comment>
</document>
"""],
["""\
.. A comment.
.. Another.

Paragraph.
""",
"""\
<document>
    <comment>
        A comment.
    </comment>
    <comment>
        Another.
    </comment>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. A comment
no blank line

Paragraph.
""",
"""\
<document>
    <comment>
        A comment
    </comment>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. A comment::

Paragraph.
""",
"""\
<document>
    <comment>
        A comment::
    </comment>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. Next is an empty comment, which serves to end this comment and
   prevents the following block quote being swallowed up.

..

    A block quote.
""",
"""\
<document>
    <comment>
        Next is an empty comment, which serves to end this comment and
        prevents the following block quote being swallowed up.
    </comment>
    <comment/>
    <block_quote>
        <paragraph>
            A block quote.
        </paragraph>
    </block_quote>
</document>
"""],
["""\
term 1
  definition 1

  .. a comment

term 2
  definition 2
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            </term>
            <definition>
                <paragraph>
                    definition 1
                </paragraph>
                <comment>
                    a comment
                </comment>
            </definition>
        </definition_list_item>
        <definition_list_item>
            <term>
                term 2
            </term>
            <definition>
                <paragraph>
                    definition 2
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
term 1
  definition 1

.. a comment

term 2
  definition 2
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            </term>
            <definition>
                <paragraph>
                    definition 1
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
    <comment>
        a comment
    </comment>
    <definition_list>
        <definition_list_item>
            <term>
                term 2
            </term>
            <definition>
                <paragraph>
                    definition 2
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
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

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
