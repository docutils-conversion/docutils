#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:07:43 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['targets'] = [
["""\
.. _target:

(internal hyperlink)
""",
"""\
<document>
    <target name="target"/>
    <paragraph>
        (internal hyperlink)
    </paragraph>
</document>
"""],
["""\
.. _one-liner: http://structuredtext.sourceforge.net

.. _starts-on-this-line: http://
                         structuredtext.
                         sourceforge.net

.. _entirely-below:
   http://structuredtext.
   sourceforge.net
""",
"""\
<document>
    <target name="one-liner">
        http://structuredtext.sourceforge.net
    </target>
    <target name="starts-on-this-line">
        http://structuredtext.sourceforge.net
    </target>
    <target name="entirely-below">
        http://structuredtext.sourceforge.net
    </target>
</document>
"""],
["""\
.. _target: Not a proper hyperlink target
""",
"""\
<document>
    <system_warning level="1">
        <paragraph>
            Hyperlink target at line 1 contains whitespace. Perhaps a footnote was intended?
        </paragraph>
        <literal_block>
            .. _target: Not a proper hyperlink target
        </literal_block>
    </system_warning>
</document>
"""],
["""\
.. _a long target name:

.. _`a target name: including a colon (quoted)`:

.. _a target name\: including a colon (escaped):
""",
"""\
<document>
    <target name="a long target name"/>
    <target name="a target name: including a colon (quoted)"/>
    <target name="a target name: including a colon (escaped)"/>
</document>
"""],
["""\
.. _target: http://www.python.org/

(indirect external hyperlink)
""",
"""\
<document>
    <target name="target">
        http://www.python.org/
    </target>
    <paragraph>
        (indirect external hyperlink)
    </paragraph>
</document>
"""],
["""\
Duplicate indirect links (different URIs):

.. _target: first

.. _target: second
""",
"""\
<document>
    <paragraph>
        Duplicate indirect links (different URIs):
    </paragraph>
    <target dupname="target">
        first
    </target>
    <system_warning level="1">
        <paragraph>
            Duplicate indirect link name: "target"
        </paragraph>
    </system_warning>
    <target name="target">
        second
    </target>
</document>
"""],
["""\
Duplicate indirect links (same URIs):

.. _target: first

.. _target: first
""",
"""\
<document>
    <paragraph>
        Duplicate indirect links (same URIs):
    </paragraph>
    <target dupname="target">
        first
    </target>
    <system_warning level="0">
        <paragraph>
            Duplicate indirect link name: "target"
        </paragraph>
    </system_warning>
    <target name="target">
        first
    </target>
</document>
"""],
["""\
Duplicate implicit links.

Title
=====

Paragraph.

Title
=====

Paragraph.
""",
"""\
<document>
    <paragraph>
        Duplicate implicit links.
    </paragraph>
    <section dupname="title">
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
    <section dupname="title">
        <title>
            Title
        </title>
        <system_warning level="0">
            <paragraph>
                Duplicate implicit link name: "title"
            </paragraph>
        </system_warning>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
Duplicate implicit/explicit links.

Title
=====

.. _title:

Paragraph.
""",
"""\
<document>
    <paragraph>
        Duplicate implicit/explicit links.
    </paragraph>
    <section dupname="title">
        <title>
            Title
        </title>
        <system_warning level="0">
            <paragraph>
                Duplicate implicit link name: "title"
            </paragraph>
        </system_warning>
        <target name="title"/>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
Duplicate explicit links.

.. _title:

First.

.. _title:

Second.

.. _title:

Third.
""",
"""\
<document>
    <paragraph>
        Duplicate explicit links.
    </paragraph>
    <target dupname="title"/>
    <paragraph>
        First.
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Duplicate explicit link name: "title"
        </paragraph>
    </system_warning>
    <target dupname="title"/>
    <paragraph>
        Second.
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Duplicate explicit link name: "title"
        </paragraph>
    </system_warning>
    <target dupname="title"/>
    <paragraph>
        Third.
    </paragraph>
</document>
"""],
["""\
Duplicate targets:

Target
======

Implicit section header target.

.. [target] Implicit footnote target.

.. _target:

Explicit internal target.

.. _target: Explicit_indirect_target.
""",
"""\
<document>
    <paragraph>
        Duplicate targets:
    </paragraph>
    <section dupname="target">
        <title>
            Target
        </title>
        <paragraph>
            Implicit section header target.
        </paragraph>
        <footnote dupname="target">
            <label>
                target
            </label>
            <system_warning level="0">
                <paragraph>
                    Duplicate implicit link name: "target"
                </paragraph>
            </system_warning>
            <paragraph>
                Implicit footnote target.
            </paragraph>
        </footnote>
        <system_warning level="0">
            <paragraph>
                Duplicate implicit link name: "target"
            </paragraph>
        </system_warning>
        <target dupname="target"/>
        <paragraph>
            Explicit internal target.
        </paragraph>
        <system_warning level="1">
            <paragraph>
                Duplicate indirect link name: "target"
            </paragraph>
        </system_warning>
        <target name="target">
            Explicit_indirect_target.
        </target>
    </section>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
