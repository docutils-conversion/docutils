#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/03/12 03:32:26 $
:Copyright: This module has been placed in the public domain.

Tests for images.py image directives.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

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
    <system_message level="3" type="ERROR">
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
    <system_message level="3" type="ERROR">
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
["""\
.. image:: picture.png
   [height=100 width=200 scale=50]
   [alt="Alternate text for the picture"]
""",
"""\
<document>
    <image alt="Alternate text for the picture" height="100" scale="50" uri="picture.png" width="200">
"""],
["""\
.. image:: picture.png
   [height=100]
   [width=200]
   [scale=50]
   [alt="Alternate text for the picture"]
""",
"""\
<document>
    <image alt="Alternate text for the picture" height="100" scale="50" uri="picture.png" width="200">
"""],
["""\
.. image:: picture.png
   [height=100]
   [width=200 scale=50
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Invalid image attribute data at line 1: input line not enclosed in "[" and "]".
        <literal_block>
            .. image:: picture.png
               [height=100]
               [width=200 scale=50
"""],
["""\
.. image:: picture.png
   [scale=]
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Invalid image attribute data at line 1: missing value after "scale=".
        <literal_block>
            .. image:: picture.png
               [scale=]
"""],
["""\
.. image:: picture.png
   [scale 50]
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Invalid image attribute data at line 1: missing "=".
        <literal_block>
            .. image:: picture.png
               [scale 50]
"""],
["""\
.. image:: picture.png
   [=50]
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Invalid image attribute data at line 1: missing attribute name before "=".
        <literal_block>
            .. image:: picture.png
               [=50]
"""],
["""\
.. image:: picture.png
   [sale=50]
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Unknown image attribute at line 1: "sale".
        <literal_block>
            .. image:: picture.png
               [sale=50]
"""],
["""\
.. image:: picture.png
   [scale=fifty]
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Invalid image attribute value at line 1: invalid literal for int(): fifty.
        <literal_block>
            .. image:: picture.png
               [scale=fifty]
"""],
["""\
.. image:: picture.png
   [scale=50 scale=50]
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Invalid image attribute data at line 1: duplicate attribute "scale".
        <literal_block>
            .. image:: picture.png
               [scale=50 scale=50]
"""],
["""\
.. image:: picture.png
   [alt='a picture]
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Invalid image attribute data at line 1: attribute "alt" missing end quote (').
        <literal_block>
            .. image:: picture.png
               [alt='a picture]
"""],
["""\
.. image:: picture.png
   [alt='a picture'scale=50]
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Invalid image attribute data at line 1: attribute "alt" end quote (') not followed by whitespace.
        <literal_block>
            .. image:: picture.png
               [alt='a picture'scale=50]
"""],
]


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
