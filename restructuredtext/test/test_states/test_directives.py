#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.4 $
:Date: $Date: 2001/09/12 04:10:58 $
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
    <directive type="reStructuredText-test-directive"/>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. reStructuredText-test-directive:: argument

Paragraph.
""",
"""\
<document>
    <directive data="argument" type="reStructuredText-test-directive"/>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
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
        </paragraph>
    </directive>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
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
        </paragraph>
    </directive>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
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
        </paragraph>
    </directive>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 3.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line.
    </paragraph>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
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
        </paragraph>
    </system_warning>
    <literal_block>
        .. reStructuredText-unknown-directive::
    </literal_block>
    <system_warning level="2">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive" at line 3.
            Rendering the directive as a literal block.
        </paragraph>
    </system_warning>
    <literal_block>
        .. reStructuredText-unknown-directive:: argument
    </literal_block>
    <system_warning level="2">
        <paragraph>
            Unknown directive type "reStructuredText-unknown-directive" at line 5.
            Rendering the directive as a literal block.
        </paragraph>
    </system_warning>
    <literal_block>
        .. reStructuredText-unknown-directive::
           block
    </literal_block>
</document>
"""],
]

totest['admonitions'] = [
["""\
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
    <note>
        <paragraph>
            This is a note.
        </paragraph>
    </note>
    <tip>
        <paragraph>
            15% if the
            service is good.
        </paragraph>
    </tip>
    <bullet_list bullet="-">
        <list_item>
            <warning>
                <paragraph>
                    Strong prose may provoke extreme mental exertion.
                    Reader discretion is strongly advised.
                </paragraph>
            </warning>
        </list_item>
        <list_item>
            <error>
                <paragraph>
                    Does not compute.
                </paragraph>
            </error>
        </list_item>
    </bullet_list>
    <caution>
        <paragraph>
            Don't take any wooden nickels.
        </paragraph>
    </caution>
    <danger>
        <paragraph>
            Mad scientist at work!
        </paragraph>
    </danger>
    <important>
        <bullet_list bullet="-">
            <list_item>
                <paragraph>
                    Wash behind your ears.
                </paragraph>
            </list_item>
            <list_item>
                <paragraph>
                    Clean up your room.
                </paragraph>
            </list_item>
            <list_item>
                <paragraph>
                    Call your mother.
                </paragraph>
            </list_item>
            <list_item>
                <paragraph>
                    Back up your data.
                </paragraph>
            </list_item>
        </bullet_list>
    </important>
</document>
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
        </paragraph>
    </note>
    <note>
        <paragraph>
            One after the other.
        </paragraph>
    </note>
    <note>
        <paragraph>
            No blank lines in-between.
        </paragraph>
    </note>
</document>
"""],
]

totest['images'] = [
["""\
.. image:: picture.png
""",
"""\
<document>
    <image uri="picture.png"/>
</document>
"""],
["""\
.. image::
""",
"""\
<document>
    <system_warning level="2">
        <paragraph>
            Missing image URI argument at line 1.
        </paragraph>
        <literal_block>
            .. image::
        </literal_block>
    </system_warning>
</document>
"""],
["""\
.. image:: one two three
""",
"""\
<document>
    <system_warning level="2">
        <paragraph>
            Unknown image attribute "two" at line 1.
        </paragraph>
        <literal_block>
            .. image:: one two three
        </literal_block>
    </system_warning>
</document>
"""],
["""\
.. image:: picture.png height=100 width=200 scale=50
""",
"""\
<document>
    <image height="100" scale="50" uri="picture.png" width="200"/>
</document>
"""],
["""\
.. figure:: picture.png
   A picture with a caption.
""",
"""\
<document>
    <figure>
        <image uri="picture.png"/>
        <caption>
            A picture with a caption.
        </caption>
    </figure>
</document>
"""],
["""\
.. Figure:: picture.png height=100 width=200 scale=50
   A picture with image attributes and a caption.
""",
"""\
<document>
    <figure>
        <image height="100" scale="50" uri="picture.png" width="200"/>
        <caption>
            A picture with image attributes and a caption.
        </caption>
    </figure>
</document>
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
    </paragraph>
    <figure>
        <image uri="picture.png"/>
    </figure>
</document>
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
        <image uri="picture.png"/>
        <caption>
            A picture with a caption and a legend.
        </caption>
        <legend>
            <table>
                <tgroup cols="2">
                    <colspec colwidth="23"/>
                    <colspec colwidth="23"/>
                    <thead>
                        <row>
                            <entry>
                                <paragraph>
                                    Symbol
                                </paragraph>
                            </entry>
                            <entry>
                                <paragraph>
                                    Meaning
                                </paragraph>
                            </entry>
                        </row>
                    </thead>
                    <tbody>
                        <row>
                            <entry>
                                <image uri="tent.png"/>
                            </entry>
                            <entry>
                                <paragraph>
                                    Campground
                                </paragraph>
                            </entry>
                        </row>
                        <row>
                            <entry>
                                <image uri="waves.png"/>
                            </entry>
                            <entry>
                                <paragraph>
                                    Lake
                                </paragraph>
                            </entry>
                        </row>
                        <row>
                            <entry>
                                <image uri="peak.png"/>
                            </entry>
                            <entry>
                                <paragraph>
                                    Mountain
                                </paragraph>
                            </entry>
                        </row>
                    </tbody>
                </tgroup>
            </table>
        </legend>
    </figure>
</document>
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
        <image uri="picture.png"/>
        <legend>
            <paragraph>
                A picture with a legend but no caption.
                (The empty comment replaces the caption, which must
                be a single paragraph.)
            </paragraph>
        </legend>
    </figure>
</document>
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
    </paragraph>
    <figure>
        <image uri="picture.png"/>
        <caption>
            A picture with a caption.
        </caption>
    </figure>
    <figure>
        <image uri="picture.png"/>
        <caption>
            A picture with a caption.
        </caption>
    </figure>
    <figure>
        <image uri="picture.png"/>
        <caption>
            A picture with a caption.
        </caption>
    </figure>
    <figure>
        <image uri="picture.png"/>
    </figure>
    <figure>
        <image uri="picture.png"/>
    </figure>
    <figure>
        <image uri="picture.png"/>
    </figure>
    <figure>
        <image uri="picture.png"/>
        <caption>
            A picture with a caption.
        </caption>
    </figure>
    <figure>
        <image uri="picture.png"/>
    </figure>
    <figure>
        <image uri="picture.png"/>
        <caption>
            A picture with a caption.
        </caption>
    </figure>
    <figure>
        <image uri="picture.png"/>
    </figure>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
