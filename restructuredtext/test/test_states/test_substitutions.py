#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/11/06 23:11:52 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['substitutions'] = [
["""\
.. /text/ This is replacement text.
""",
"""\
<document>
    <substitution name="text">
        This is replacement text.
"""],
["""\
.. /text/ This is replacement text with *inline* ``markup``.
""",
"""\
<document>
    <substitution name="text">
        This is replacement text with 
        <emphasis>
            inline
         
        <literal>
            markup
        .
"""],
["""\
.. /text/ This is replacement text with another `/substitution/`.
""",
"""\
<document>
    <substitution name="text">
        This is replacement text with another 
        <substitution_reference refname="substitution">
            substitution
        .
"""],
["""\
Here's an image substitution:

.. /symbol/ image:: symbol.png
""",
"""\
<document>
    <paragraph>
        Here's an image substitution:
    <substitution name="symbol">
        <image uri="symbol.png">
"""],
["""\
Here's a series of substitutions:

.. /symbol1/ image:: symbol1.png
.. /text1/ This is replacement text.
.. /symbol2/ image:: symbol2.png
.. /text2/ This is replacement text.
""",
"""\
<document>
    <paragraph>
        Here's a series of substitutions:
    <substitution name="symbol1">
        <image uri="symbol1.png">
    <substitution name="text1">
        This is replacement text.
    <substitution name="symbol2">
        <image uri="symbol2.png">
    <substitution name="text2">
        This is replacement text.
"""],
["""\
Here are some duplicate substitutions:

.. /symbol/ image:: symbol.png
.. /text/ This is replacement text.
.. /symbol/ image:: symbol.png
.. /text/ This is replacement text.
""",
"""\
<document>
    <paragraph>
        Here are some duplicate substitutions:
    <substitution name="symbol">
        <image uri="symbol.png">
    <substitution name="text">
        This is replacement text.
    <system_warning level="2">
        <paragraph>
            Duplicate substitution name: "symbol"
    <substitution name="symbol">
        <image uri="symbol.png">
    <system_warning level="2">
        <paragraph>
            Duplicate substitution name: "text"
    <substitution name="text">
        This is replacement text.
"""],
["""\
Here are some bad cases:

.. /symbol/ image:: symbol.png
No blank line after.

.. /empty/

.. /unknown/ directive:: symbol.png
""",
"""\
<document>
    <paragraph>
        Here are some bad cases:
    <substitution name="symbol">
        <image uri="symbol.png">
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
    <paragraph>
        No blank line after.
    <system_warning level="1">
        <paragraph>
            Substitution missing contents at line 6
    <substitution name="empty">
    <system_warning level="2">
        <paragraph>
            Unknown directive type "directive" at line 8.
            Rendering the directive as a literal block.
    <literal_block>
        directive:: symbol.png
    <substitution name="unknown">
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
