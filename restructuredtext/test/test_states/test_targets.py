#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/09/13 02:41:53 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['targets'] = [
["""\
.. _target:

(internal hyperlink)
""",
"""\
<document>
    <target name="target">
    <paragraph>
        (internal hyperlink)
"""],
["""\
.. _one-liner: http://structuredtext.sourceforge.net

.. _starts-on-this-line: http://
                         structuredtext.
                         sourceforge.net

.. _entirely-below:
   http://structuredtext.
   sourceforge.net
""",
"""\
<document>
    <target name="one-liner">
        http://structuredtext.sourceforge.net
    <target name="starts-on-this-line">
        http://structuredtext.sourceforge.net
    <target name="entirely-below">
        http://structuredtext.sourceforge.net
"""],
["""\
.. _target: Not a proper hyperlink target
""",
"""\
<document>
    <system_warning level="1">
        <paragraph>
            Hyperlink target at line 1 contains whitespace. Perhaps a footnote was intended?
        <literal_block>
            .. _target: Not a proper hyperlink target
"""],
["""\
.. _a long target name:

.. _`a target name: including a colon (quoted)`:

.. _a target name\: including a colon (escaped):
""",
"""\
<document>
    <target name="a long target name">
    <target name="a target name: including a colon (quoted)">
    <target name="a target name: including a colon (escaped)">
"""],
["""\
.. _target: http://www.python.org/

(indirect external hyperlink)
""",
"""\
<document>
    <target name="target">
        http://www.python.org/
    <paragraph>
        (indirect external hyperlink)
"""],
["""\
Duplicate indirect links (different URIs):

.. _target: first

.. _target: second
""",
"""\
<document>
    <paragraph>
        Duplicate indirect links (different URIs):
    <target dupname="target">
        first
    <system_warning level="1">
        <paragraph>
            Duplicate indirect link name: "target"
    <target name="target">
        second
"""],
["""\
Duplicate indirect links (same URIs):

.. _target: first

.. _target: first
""",
"""\
<document>
    <paragraph>
        Duplicate indirect links (same URIs):
    <target dupname="target">
        first
    <system_warning level="0">
        <paragraph>
            Duplicate indirect link name: "target"
    <target name="target">
        first
"""],
["""\
Duplicate implicit links.

Title
=====

Paragraph.

Title
=====

Paragraph.
""",
"""\
<document>
    <paragraph>
        Duplicate implicit links.
    <section dupname="title">
        <title>
            Title
        <paragraph>
            Paragraph.
    <section dupname="title">
        <title>
            Title
        <system_warning level="0">
            <paragraph>
                Duplicate implicit link name: "title"
        <paragraph>
            Paragraph.
"""],
["""\
Duplicate implicit/explicit links.

Title
=====

.. _title:

Paragraph.
""",
"""\
<document>
    <paragraph>
        Duplicate implicit/explicit links.
    <section dupname="title">
        <title>
            Title
        <system_warning level="0">
            <paragraph>
                Duplicate implicit link name: "title"
        <target name="title">
        <paragraph>
            Paragraph.
"""],
["""\
Duplicate explicit links.

.. _title:

First.

.. _title:

Second.

.. _title:

Third.
""",
"""\
<document>
    <paragraph>
        Duplicate explicit links.
    <target dupname="title">
    <paragraph>
        First.
    <system_warning level="1">
        <paragraph>
            Duplicate explicit link name: "title"
    <target dupname="title">
    <paragraph>
        Second.
    <system_warning level="1">
        <paragraph>
            Duplicate explicit link name: "title"
    <target dupname="title">
    <paragraph>
        Third.
"""],
["""\
Duplicate targets:

Target
======

Implicit section header target.

.. [target] Implicit footnote target.

.. _target:

Explicit internal target.

.. _target: Explicit_indirect_target.
""",
"""\
<document>
    <paragraph>
        Duplicate targets:
    <section dupname="target">
        <title>
            Target
        <paragraph>
            Implicit section header target.
        <footnote dupname="target">
            <label>
                target
            <system_warning level="0">
                <paragraph>
                    Duplicate implicit link name: "target"
            <paragraph>
                Implicit footnote target.
        <system_warning level="0">
            <paragraph>
                Duplicate implicit link name: "target"
        <target dupname="target">
        <paragraph>
            Explicit internal target.
        <system_warning level="1">
            <paragraph>
                Duplicate indirect link name: "target"
        <target name="target">
            Explicit_indirect_target.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
