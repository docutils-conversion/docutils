#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.5 $
:Date: $Date: 2001/10/23 03:38:36 $
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

(Internal hyperlink target.)
""",
"""\
<document>
    <target name="target">
    <paragraph>
        (Internal hyperlink target.)
"""],
["""\
External hyperlink targets:

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
    <paragraph>
        External hyperlink targets:
    <target name="one-liner">
        http://structuredtext.sourceforge.net
    <target name="starts-on-this-line">
        http://structuredtext.sourceforge.net
    <target name="entirely-below">
        http://structuredtext.sourceforge.net
"""],
["""\
Indirect hyperlink targets:

.. _target1: reference_

.. _target2: `phrase-link reference`_
""",
"""\
<document>
    <paragraph>
        Indirect hyperlink targets:
    <target name="target1" refname="reference">
    <target name="target2" refname="phrase-link reference">
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

(external hyperlink)
""",
"""\
<document>
    <target name="target">
        http://www.python.org/
    <paragraph>
        (external hyperlink)
"""],
["""\
Duplicate external targets (different URIs):

.. _target: first

.. _target: second
""",
"""\
<document>
    <paragraph>
        Duplicate external targets (different URIs):
    <target dupname="target">
        first
    <system_warning level="1">
        <paragraph>
            Duplicate external target name: "target"
    <target name="target">
        second
"""],
["""\
Duplicate external targets (same URIs):

.. _target: first

.. _target: first
""",
"""\
<document>
    <paragraph>
        Duplicate external targets (same URIs):
    <target dupname="target">
        first
    <system_warning level="0">
        <paragraph>
            Duplicate external target name: "target"
    <target name="target">
        first
"""],
["""\
Duplicate implicit targets.

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
        Duplicate implicit targets.
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
                Duplicate implicit target name: "title"
        <paragraph>
            Paragraph.
"""],
["""\
Duplicate implicit/explicit targets.

Title
=====

.. _title:

Paragraph.
""",
"""\
<document>
    <paragraph>
        Duplicate implicit/explicit targets.
    <section dupname="title">
        <title>
            Title
        <system_warning level="0">
            <paragraph>
                Duplicate implicit target name: "title"
        <target name="title">
        <paragraph>
            Paragraph.
"""],
["""\
Duplicate explicit targets.

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
        Duplicate explicit targets.
    <target dupname="title">
    <paragraph>
        First.
    <system_warning level="1">
        <paragraph>
            Duplicate explicit target name: "title"
    <target dupname="title">
    <paragraph>
        Second.
    <system_warning level="1">
        <paragraph>
            Duplicate explicit target name: "title"
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

.. _target: Explicit_external_target.
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
                    Duplicate implicit target name: "target"
            <paragraph>
                Implicit footnote target.
        <system_warning level="0">
            <paragraph>
                Duplicate implicit target name: "target"
        <target dupname="target">
        <paragraph>
            Explicit internal target.
        <system_warning level="1">
            <paragraph>
                Duplicate external target name: "target"
        <target name="target">
            Explicit_external_target.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
