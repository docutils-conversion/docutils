#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:02:12 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['definition_lists'] = [
["""\
term
  definition
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term
            </term>
            <definition>
                <paragraph>
                    definition
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
term
  definition

paragraph
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term
            </term>
            <definition>
                <paragraph>
                    definition
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
    <paragraph>
        paragraph
    </paragraph>
</document>
"""],
["""\
term
  definition
no blank line
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term
            </term>
            <definition>
                <paragraph>
                    definition
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 3.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
</document>
"""],
["""\
A paragraph::
    A literal block without a blank line first?
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                A paragraph::
            </term>
            <definition>
                <system_warning level="0">
                    <paragraph>
                        Blank line missing before literal block? Interpreted as a definition list item. At line 2.
                    </paragraph>
                </system_warning>
                <paragraph>
                    A literal block without a blank line first?
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
term 1
  definition 1

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
  definition 1 (no blank line below)
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
                    definition 1 (no blank line below)
                </paragraph>
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

  term 1a
    definition 1a

  term 1b
    definition 1b

term 2
  definition 2

paragraph
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
                <definition_list>
                    <definition_list_item>
                        <term>
                            term 1a
                        </term>
                        <definition>
                            <paragraph>
                                definition 1a
                            </paragraph>
                        </definition>
                    </definition_list_item>
                    <definition_list_item>
                        <term>
                            term 1b
                        </term>
                        <definition>
                            <paragraph>
                                definition 1b
                            </paragraph>
                        </definition>
                    </definition_list_item>
                </definition_list>
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
    <paragraph>
        paragraph
    </paragraph>
</document>
"""],
["""\
Term : classifier
    The ' : ' indicates a classifier in
    definition list item terms only.
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                Term
            </term>
            <classifier>
                classifier
            </classifier>
            <definition>
                <paragraph>
                    The ' : ' indicates a classifier in
                    definition list item terms only.
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
Term: not a classifier
    Because there's no space before the colon.
Term :not a classifier
    Because there's no space after the colon.
Term \: not a classifier
    Because the colon is escaped.
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                Term: not a classifier
            </term>
            <definition>
                <paragraph>
                    Because there's no space before the colon.
                </paragraph>
            </definition>
        </definition_list_item>
        <definition_list_item>
            <term>
                Term :not a classifier
            </term>
            <definition>
                <paragraph>
                    Because there's no space after the colon.
                </paragraph>
            </definition>
        </definition_list_item>
        <definition_list_item>
            <term>
                Term : not a classifier
            </term>
            <definition>
                <paragraph>
                    Because the colon is escaped.
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
Term `with *inline ``text **errors : classifier `with *errors ``too
    Definition `with *inline ``text **markup errors.
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                Term `with *inline ``text **errors
            </term>
            <classifier>
                classifier `with *errors ``too
            </classifier>
            <definition>
                <system_warning level="1">
                    <paragraph>
                        Inline interpreted text or phrase link start-string without end-string at line 1.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline emphasis start-string without end-string at line 1.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline literal start-string without end-string at line 1.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline strong start-string without end-string at line 1.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline interpreted text or phrase link start-string without end-string at line 1.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline emphasis start-string without end-string at line 1.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline literal start-string without end-string at line 1.
                    </paragraph>
                </system_warning>
                <paragraph>
                    Definition `with *inline ``text **markup errors.
                </paragraph>
                <system_warning level="1">
                    <paragraph>
                        Inline interpreted text or phrase link start-string without end-string at line 2.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline emphasis start-string without end-string at line 2.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline literal start-string without end-string at line 2.
                    </paragraph>
                </system_warning>
                <system_warning level="1">
                    <paragraph>
                        Inline strong start-string without end-string at line 2.
                    </paragraph>
                </system_warning>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
