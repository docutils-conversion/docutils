#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/11/19 04:33:36 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['substitution_definitions'] = [
["""\
Here's an image substitution definition:

.. |symbol| image:: symbol.png
""",
"""\
<document>
    <paragraph>
        Here's an image substitution definition:
    <substitution_definition name="symbol">
        <image alt="symbol" uri="symbol.png">
"""],
["""\
Embedded directive starts on the next line:

.. |symbol|
   image:: symbol.png
""",
"""\
<document>
    <paragraph>
        Embedded directive starts on the next line:
    <substitution_definition name="symbol">
        <image alt="symbol" uri="symbol.png">
"""],
["""\
Here's a series of substitution definitions:

.. |symbol 1| image:: symbol1.png
.. |SYMBOL 2| image:: symbol2.png
   [height=50 width=100]
.. |symbol 3| image:: symbol3.png
""",
"""\
<document>
    <paragraph>
        Here's a series of substitution definitions:
    <substitution_definition name="symbol 1">
        <image alt="symbol 1" uri="symbol1.png">
    <substitution_definition name="symbol 2">
        <image alt="SYMBOL 2" height="50" uri="symbol2.png" width="100">
    <substitution_definition name="symbol 3">
        <image alt="symbol 3" uri="symbol3.png">
"""],
["""\
.. |very long substitution text,
   split across lines| image:: symbol.png
""",
"""\
<document>
    <substitution_definition name="very long substitution text, split across lines">
        <image alt="very long substitution text, split across lines" uri="symbol.png">
"""],
["""\
Here are some duplicate substitution definitions:

.. |symbol| image:: symbol.png
.. |symbol| image:: symbol.png
""",
"""\
<document>
    <paragraph>
        Here are some duplicate substitution definitions:
    <substitution_definition dupname="symbol">
        <image alt="symbol" uri="symbol.png">
    <system_warning level="2">
        <paragraph>
            Duplicate substitution definition name: "symbol"
    <substitution_definition name="symbol">
        <image alt="symbol" uri="symbol.png">
"""],
["""\
Here are some bad cases:

.. |symbol| image:: symbol.png
No blank line after.

.. |empty|

.. |unknown| directive:: symbol.png

.. |invalid| there's no directive here
""",
"""\
<document>
    <paragraph>
        Here are some bad cases:
    <substitution_definition name="symbol">
        <image alt="symbol" uri="symbol.png">
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
    <paragraph>
        No blank line after.
    <system_warning level="1">
        <paragraph>
            Substitution definition "empty" missing contents at line 6.
    <system_warning level="2">
        <paragraph>
            Unknown directive type "directive" at line 8.
            Rendering the directive as a literal block.
    <literal_block>
        directive:: symbol.png
    <system_warning level="1">
        <paragraph>
            Substitution definition "unknown" empty or invalid at line 8.
    <system_warning level="1">
        <paragraph>
            Substitution definition "invalid" empty or invalid at line 10.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
