#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/11/13 03:17:16 $
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
.. /symbol2/ image:: symbol2.png
   [height=50 width=100]
.. /symbol3/ image:: symbol3.png
""",
"""\
<document>
    <paragraph>
        Here's a series of substitutions:
    <substitution name="symbol1">
        <image uri="symbol1.png">
    <substitution name="symbol2">
        <image height="50" uri="symbol2.png" width="100">
    <substitution name="symbol3">
        <image uri="symbol3.png">
"""],
["""\
Here are some duplicate substitutions:

.. /symbol/ image:: symbol.png
.. /symbol/ image:: symbol.png
""",
"""\
<document>
    <paragraph>
        Here are some duplicate substitutions:
    <substitution name="symbol">
        <image uri="symbol.png">
    <system_warning level="2">
        <paragraph>
            Duplicate substitution name: "symbol"
    <substitution name="symbol">
        <image uri="symbol.png">
"""],
["""\
Here are some bad cases:

.. /symbol/ image:: symbol.png
No blank line after.

.. /empty/

.. /unknown/ directive:: symbol.png

.. /invalid/ there's no directive here
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
            Substitution "empty" missing contents at line 6.
    <system_warning level="2">
        <paragraph>
            Unknown directive type "directive" at line 8.
            Rendering the directive as a literal block.
    <literal_block>
        directive:: symbol.png
    <system_warning level="1">
        <paragraph>
            Substitution "unknown" empty or invalid at line 8.
    <system_warning level="1">
        <paragraph>
            Substitution "invalid" empty or invalid at line 10.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
