#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/09/10 04:50:53 $
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
        <literal_block>
            Directive block contains one paragraph, with a blank line before.
        </literal_block>
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
        <literal_block>
            Directive block contains one paragraph, no blank line before.
        </literal_block>
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
