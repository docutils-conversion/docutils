#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.5 $
:Date: $Date: 2002/02/06 02:17:21 $
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
            <definition>
                <paragraph>
                    definition
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
            <definition>
                <paragraph>
                    definition
    <paragraph>
        paragraph
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
            <definition>
                <paragraph>
                    definition
    <system_warning level="2" type="WARNING">
        <paragraph>
            Unindent without blank line at line 3.
    <paragraph>
        no blank line
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
            <definition>
                <system_warning level="1" type="INFO">
                    <paragraph>
                        Blank line missing before literal block? Interpreted as a definition list item. At line 2.
                <paragraph>
                    A literal block without a blank line first?
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
            <definition>
                <paragraph>
                    definition 1
        <definition_list_item>
            <term>
                term 2
            <definition>
                <paragraph>
                    definition 2
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
            <definition>
                <paragraph>
                    definition 1 (no blank line below)
        <definition_list_item>
            <term>
                term 2
            <definition>
                <paragraph>
                    definition 2
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
            <definition>
                <paragraph>
                    definition 1
                <definition_list>
                    <definition_list_item>
                        <term>
                            term 1a
                        <definition>
                            <paragraph>
                                definition 1a
                    <definition_list_item>
                        <term>
                            term 1b
                        <definition>
                            <paragraph>
                                definition 1b
        <definition_list_item>
            <term>
                term 2
            <definition>
                <paragraph>
                    definition 2
    <paragraph>
        paragraph
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
            <classifier>
                classifier
            <definition>
                <paragraph>
                    The ' : ' indicates a classifier in
                    definition list item terms only.
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
            <definition>
                <paragraph>
                    Because there's no space before the colon.
        <definition_list_item>
            <term>
                Term :not a classifier
            <definition>
                <paragraph>
                    Because there's no space after the colon.
        <definition_list_item>
            <term>
                Term : not a classifier
            <definition>
                <paragraph>
                    Because the colon is escaped.
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
            <classifier>
                classifier `with *errors ``too
            <definition>
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline interpreted text or phrase reference start-string without end-string at line 1.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline emphasis start-string without end-string at line 1.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline literal start-string without end-string at line 1.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline strong start-string without end-string at line 1.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline interpreted text or phrase reference start-string without end-string at line 1.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline emphasis start-string without end-string at line 1.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline literal start-string without end-string at line 1.
                <paragraph>
                    Definition `with *inline ``text **markup errors.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline interpreted text or phrase reference start-string without end-string at line 2.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline emphasis start-string without end-string at line 2.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline literal start-string without end-string at line 2.
                <system_warning level="2" type="WARNING">
                    <paragraph>
                        Inline strong start-string without end-string at line 2.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
