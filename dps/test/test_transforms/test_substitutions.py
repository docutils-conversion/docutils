#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/01/29 02:18:14 $
:Copyright: This module has been placed in the public domain.

Tests for dps.transforms.references.Substitutions.
"""

import DPSTestSupport
from dps.transforms.references import Substitutions
import UnitTestFolder
try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser


def suite():
    parser = Parser(warninglevel=4, errorlevel=4, languagecode='en',
                    debug=UnitTestFolder.debug)
    s = DPSTestSupport.TransformTestSuite(parser)
    s.generateTests(totest)
    return s

totest = {}

totest['substitutions'] = ((Substitutions,), [
["""\
The |biohazard| symbol is deservedly scary-looking.

.. |biohazard| image:: biohazard.png
""",
"""\
<document>
    <paragraph>
        The 
        <image alt="biohazard" uri="biohazard.png">
         symbol is deservedly scary-looking.
    <substitution_definition name="biohazard">
        <image alt="biohazard" uri="biohazard.png">
"""],
["""\
Here's an |unknown| substitution.
""",
"""\
<document>
    <paragraph>
        Here's an 
        <problematic>
            unknown
         substitution.
    <system_warning level="2">
        <paragraph>
            Undefined substitution referenced: "unknown".
"""],
])


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
