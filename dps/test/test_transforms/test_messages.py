#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/02/22 01:58:02 $
:Copyright: This module has been placed in the public domain.

Tests for dps.transforms.universal.Messages.
"""

import DPSTestSupport
from dps.transforms.universal import Messages
from dps.transforms.references import Substitutions
import UnitTestFolder
try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser


def suite():
    parser = Parser()
    s = DPSTestSupport.TransformTestSuite(parser)
    s.generateTests(totest)
    return s

totest = {}

totest['system_message_sections'] = ((Substitutions, Messages,), [
["""\
This |unknown substitution| will generate a system message, thanks to
the ``Substitutions`` transform. The ``Messages`` transform will
generate a "System Messages" section.

(A second copy of the system message is tacked on to the end of the
doctree by the test framework.)
""",
"""\
<document>
    <paragraph>
        This \n\
        <problematic>
            unknown substitution
         will generate a system message, thanks to
        the \n\
        <literal>
            Substitutions
         transform. The \n\
        <literal>
            Messages
         transform will
        generate a "System Messages" section.
    <paragraph>
        (A second copy of the system message is tacked on to the end of the
        doctree by the test framework.)
    <section class="system_messages">
        <title>
            Docutils System Messages
        <system_message level="3" type="ERROR">
            <paragraph>
                Undefined substitution referenced: "unknown substitution".
    <system_message level="3" type="ERROR">
        <paragraph>
            Undefined substitution referenced: "unknown substitution".
"""],
])


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
