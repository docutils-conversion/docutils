#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:02:43 $
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
.. directive::

Paragraph.
""",
"""\
<document>
    <directive type="directive"/>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. directive:: argument

Paragraph.
""",
"""\
<document>
    <directive data="argument" type="directive"/>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. directive::
   block

Paragraph.
""",
"""\
<document>
    <directive type="directive">
        <literal_block>
            block
        </literal_block>
    </directive>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. directive::

   block

Paragraph.
""",
"""\
<document>
    <directive type="directive">
        <literal_block>
            block
        </literal_block>
    </directive>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. directive::
   block
no blank line.

Paragraph.
""",
"""\
<document>
    <directive type="directive">
        <literal_block>
            block
        </literal_block>
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
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
