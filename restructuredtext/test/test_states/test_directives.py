#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.6 $
:Date: $Date: 2001/09/17 04:29:24 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['directives'] = [
["""\
.. reStructuredText-test-directive::

Paragraph.
""",
"""\
<document>
    <directive type="reStructuredText-test-directive">
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive:: argument

Paragraph.
""",
"""\
<document>
    <directive data="argument" type="reStructuredText-test-directive">
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive::

   Directive block contains one paragraph, with a blank line before.

Paragraph.
""",
"""\
<document>
    <directive type="reStructuredText-test-directive">
        <paragraph>
            Directive block contains one paragraph, with a blank line before.
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive::
   Directive block contains one paragraph, no blank line before.

Paragraph.
""",
"""\
<document>
    <directive type="reStructuredText-test-directive">
        <paragraph>
            Directive block contains one paragraph, no blank line before.
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-test-directive::
   block
no blank line.

Paragraph.
""",
"""\
<document>
    <directive type="reStructuredText-test-directive">
        <paragraph>
            block
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 3.
    <paragraph>
        no blank line.
    <paragraph>
        Paragraph.
"""],
["""\
.. reStructuredText-unknown-directive::

.. reStructuredText-unknown-directive:: argument

.. reStructuredText-unknown-directive::
   block
""",
"""\
<document>
    <system_warning level="2">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive" at line 1.
            Rendering the directive as a literal block.
    <literal_block>
        .. reStructuredText-unknown-directive::
    <system_warning level="2">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive" at line 3.
            Rendering the directive as a literal block.
    <literal_block>
        .. reStructuredText-unknown-directive:: argument
    <system_warning level="2">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive" at line 5.
            Rendering the directive as a literal block.
    <literal_block>
        .. reStructuredText-unknown-directive::
           block
"""],
]

totest['admonitions'] = [
["""\
.. Attention:: Directives at large.

.. Note:: This is a note.

.. Tip:: 15% if the
   service is good.

- .. WARNING:: Strong prose may provoke extreme mental exertion.
     Reader discretion is strongly advised.
- .. Error:: Does not compute.

.. Caution::

   Don't take any wooden nickels.

.. DANGER:: Mad scientist at work!

.. Important::
   - Wash behind your ears.
   - Clean up your room.
   - Call your mother.
   - Back up your data.
""",
"""\
<document>
    <attention>
        <paragraph>
            Directives at large.
    <note>
        <paragraph>
            This is a note.
    <tip>
        <paragraph>
            15% if the
            service is good.
    <bullet_list bullet="-">
        <list_item>
            <warning>
                <paragraph>
                    Strong prose may provoke extreme mental exertion.
                    Reader discretion is strongly advised.
        <list_item>
            <error>
                <paragraph>
                    Does not compute.
    <caution>
        <paragraph>
            Don't take any wooden nickels.
    <danger>
        <paragraph>
            Mad scientist at work!
    <important>
        <bullet_list bullet="-">
            <list_item>
                <paragraph>
                    Wash behind your ears.
            <list_item>
                <paragraph>
                    Clean up your room.
            <list_item>
                <paragraph>
                    Call your mother.
            <list_item>
                <paragraph>
                    Back up your data.
"""],
["""\
.. note:: One-line notes.
.. note:: One after the other.
.. note:: No blank lines in-between.
""",
"""\
<document>
    <note>
        <paragraph>
            One-line notes.
    <note>
        <paragraph>
            One after the other.
    <note>
        <paragraph>
            No blank lines in-between.
"""],
]

totest['images'] = [
["""\
.. image:: picture.png
""",
"""\
<document>
    <image uri="picture.png">
"""],
["""\
.. image::
""",
"""\
<document>
    <system_warning level="2">
        <paragraph>
            Missing image URI argument at line 1.
        <literal_block>
            .. image::
"""],
["""\
.. image:: one two three
""",
"""\
<document>
    <system_warning level="1">
        <paragraph>
            Image URI at line 1 contains whitespace.
        <literal_block>
            .. image:: one two three
"""],
["""\
.. image:: picture.png
   [height=100 width=200 scale=50]
""",
"""\
<document>
    <image height="100" scale="50" uri="picture.png" width="200">
"""],
["""\
.. image::
   picture.png
   [height=100 width=200 scale=50]
""",
"""\
<document>
    <image height="100" scale="50" uri="picture.png" width="200">
"""],
["""\
.. image:: a/very/long/path/to/
   picture.png
   [height=100 width=200 scale=50]
""",
"""\
<document>
    <image height="100" scale="50" uri="a/very/long/path/to/picture.png" width="200">
"""],
]

totest['figures'] = [
["""\
.. figure:: picture.png

   A picture with a caption.
""",
"""\
<document>
    <figure>
        <image uri="picture.png">
        <caption>
            A picture with a caption.
"""],
["""\
.. Figure:: picture.png
   [height=100 width=200 scale=50]

   A picture with image attributes and a caption.
""",
"""\
<document>
    <figure>
        <image height="100" scale="50" uri="picture.png" width="200">
        <caption>
            A picture with image attributes and a caption.
"""],
["""\
This figure lacks a caption. It may still have a
"Figure 1."-style caption appended in the output.

.. figure:: picture.png
""",
"""\
<document>
    <paragraph>
        This figure lacks a caption. It may still have a
        "Figure 1."-style caption appended in the output.
    <figure>
        <image uri="picture.png">
"""],
["""\
.. figure:: picture.png

   A picture with a caption and a legend.

   +-----------------------+-----------------------+
   | Symbol                | Meaning               |
   +=======================+=======================+
   | .. image:: tent.png   | Campground            |
   +-----------------------+-----------------------+
   | .. image:: waves.png  | Lake                  |
   +-----------------------+-----------------------+
   | .. image:: peak.png   | Mountain              |
   +-----------------------+-----------------------+
""",
"""\
<document>
    <figure>
        <image uri="picture.png">
        <caption>
            A picture with a caption and a legend.
        <legend>
            <table>
                <tgroup cols="2">
                    <colspec colwidth="23">
                    <colspec colwidth="23">
                    <thead>
                        <row>
                            <entry>
                                <paragraph>
                                    Symbol
                            <entry>
                                <paragraph>
                                    Meaning
                    <tbody>
                        <row>
                            <entry>
                                <image uri="tent.png">
                            <entry>
                                <paragraph>
                                    Campground
                        <row>
                            <entry>
                                <image uri="waves.png">
                            <entry>
                                <paragraph>
                                    Lake
                        <row>
                            <entry>
                                <image uri="peak.png">
                            <entry>
                                <paragraph>
                                    Mountain
"""],
["""\
.. figure:: picture.png

   ..

   A picture with a legend but no caption.
   (The empty comment replaces the caption, which must
   be a single paragraph.)
""",
"""\
<document>
    <figure>
        <image uri="picture.png">
        <legend>
            <paragraph>
                A picture with a legend but no caption.
                (The empty comment replaces the caption, which must
                be a single paragraph.)
"""],
["""\
Testing for line-leaks:

.. figure:: picture.png

   A picture with a caption.
.. figure:: picture.png

   A picture with a caption.
.. figure:: picture.png

   A picture with a caption.
.. figure:: picture.png
.. figure:: picture.png
.. figure:: picture.png
.. figure:: picture.png

   A picture with a caption.

.. figure:: picture.png

.. figure:: picture.png

   A picture with a caption.

.. figure:: picture.png
""",
"""\
<document>
    <paragraph>
        Testing for line-leaks:
    <figure>
        <image uri="picture.png">
        <caption>
            A picture with a caption.
    <figure>
        <image uri="picture.png">
        <caption>
            A picture with a caption.
    <figure>
        <image uri="picture.png">
        <caption>
            A picture with a caption.
    <figure>
        <image uri="picture.png">
    <figure>
        <image uri="picture.png">
    <figure>
        <image uri="picture.png">
    <figure>
        <image uri="picture.png">
        <caption>
            A picture with a caption.
    <figure>
        <image uri="picture.png">
    <figure>
        <image uri="picture.png">
        <caption>
            A picture with a caption.
    <figure>
        <image uri="picture.png">
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
