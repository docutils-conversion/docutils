#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.4 $
:Date: $Date: 2002/02/15 22:45:58 $
:Copyright: This module has been placed in the public domain.

Tests for dps.transforms.references.Hyperlinks.
"""

import DPSTestSupport
from dps.transforms.references import Hyperlinks
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

# Exhaustive listing of hyperlink variations: every combination of
# target/reference, direct/indirect, internal/external, and named/anonymous.
totest['enumerated_hyperlinks'] = ((Hyperlinks,), [
["""\
direct_ external

.. _direct: http://direct
""",
"""\
<document>
    <paragraph>
        <reference refuri="http://direct">
            direct
         external
    <target name="direct" refuri="http://direct">
"""],
["""\
indirect_ external

.. _indirect: xtarget_
.. _xtarget: http://indirect
""",
"""\
<document>
    <paragraph>
        <reference refuri="http://indirect">
            indirect
         external
    <target name="indirect" refuri="http://indirect">
    <target name="xtarget" refuri="http://indirect">
"""],
["""\
.. _direct:

direct_ internal
""",
"""\
<document>
    <target name="direct">
    <paragraph>
        <reference refname="direct">
            direct
         internal
"""],
["""\
.. _ztarget:

indirect_ internal

.. _indirect2: ztarget_
.. _indirect: indirect2_
""",
"""\
<document>
    <target name="ztarget">
    <paragraph>
        <reference refname="ztarget">
            indirect
         internal
    <target name="indirect2" refname="ztarget">
    <target name="indirect" refname="ztarget">
"""],
["""\
`direct external`__

__ http://direct
""",
"""\
<document>
    <paragraph>
        <reference refuri="http://direct">
            direct external
    <target name="_:1:_" refuri="http://direct">
"""],
["""\
`indirect external`__

__ xtarget_
.. _xtarget: http://indirect
""",
"""\
<document>
    <paragraph>
        <reference refuri="http://indirect">
            indirect external
    <target name="_:1:_" refuri="http://indirect">
    <target name="xtarget" refuri="http://indirect">
"""],
["""\
__

`direct internal`__
""",
"""\
<document>
    <target name="_:1:_">
    <paragraph>
        <reference refname="_:1:_">
            direct internal
"""],
["""\
.. _ztarget:

`indirect internal`__

__ ztarget_
""",
"""\
<document>
    <target name="ztarget">
    <paragraph>
        <reference refname="ztarget">
            indirect internal
    <target name="_:1:_" refname="ztarget">
"""],
])

totest['hyperlinks'] = ((Hyperlinks,), [
["""\
.. _internal hyperlink:

This paragraph referenced.

By this `internal hyperlink`_ referemce.
""",
"""\
<document>
    <target name="internal hyperlink">
    <paragraph>
        This paragraph referenced.
    <paragraph>
        By this \n\
        <reference refname="internal hyperlink">
            internal hyperlink
         referemce.
"""],
["""\
.. _chained:
.. _internal hyperlink:

This paragraph referenced.

By this `internal hyperlink`_ referemce
as well as by this chained_ reference.

The results of the transform are not visible at the XML level.
""",
"""\
<document>
    <target name="chained">
    <target name="internal hyperlink">
    <paragraph>
        This paragraph referenced.
    <paragraph>
        By this \n\
        <reference refname="internal hyperlink">
            internal hyperlink
         referemce
        as well as by this \n\
        <reference refname="chained">
            chained
         reference.
    <paragraph>
        The results of the transform are not visible at the XML level.
"""],
["""\
.. _external hyperlink: http://uri

`External hyperlink`_ reference.
""",
"""\
<document>
    <target name="external hyperlink" refuri="http://uri">
    <paragraph>
        <reference refuri="http://uri">
            External hyperlink
         reference.
"""],
["""\
.. _external hyperlink: http://uri
.. _indirect target: `external hyperlink`_
""",
"""\
<document>
    <target name="external hyperlink" refuri="http://uri">
    <target name="indirect target" refuri="http://uri">
    <system_message level="1" type="INFO">
        <paragraph>
            External hyperlink target "indirect target" is not referenced.
"""],
["""\
.. _chained:
.. _external hyperlink: http://uri

`External hyperlink`_ reference
and a chained_ reference too.
""",
"""\
<document>
    <target name="chained" refuri="http://uri">
    <target name="external hyperlink" refuri="http://uri">
    <paragraph>
        <reference refuri="http://uri">
            External hyperlink
         reference
        and a \n\
        <reference refuri="http://uri">
            chained
         reference too.
"""],
["""\
.. _external hyperlink: http://uri
.. _indirect hyperlink: `external hyperlink`_

`Indirect hyperlink`_ reference.
""",
"""\
<document>
    <target name="external hyperlink" refuri="http://uri">
    <target name="indirect hyperlink" refuri="http://uri">
    <paragraph>
        <reference refuri="http://uri">
            Indirect hyperlink
         reference.
"""],
["""\
.. _external hyperlink: http://uri
.. _chained:
.. _indirect hyperlink: `external hyperlink`_

Chained_ `indirect hyperlink`_ reference.
""",
"""\
<document>
    <target name="external hyperlink" refuri="http://uri">
    <target name="chained" refuri="http://uri">
    <target name="indirect hyperlink" refuri="http://uri">
    <paragraph>
        <reference refuri="http://uri">
            Chained
         \n\
        <reference refuri="http://uri">
            indirect hyperlink
         reference.
"""],
["""\
.. __: http://full
__
__ http://simplified
.. _external: http://indirect.external
__ external_
__

`Full syntax anonymous external hyperlink reference`__,
`chained anonymous external reference`__,
`simplified syntax anonymous external hyperlink reference`__,
`indirect anonymous hyperlink reference`__,
`internal anonymous hyperlink reference`__.
""",
"""\
<document>
    <target name="_:1:_" refuri="http://full">
    <target name="_:2:_" refuri="http://simplified">
    <target name="_:3:_" refuri="http://simplified">
    <target name="external" refuri="http://indirect.external">
    <target name="_:4:_" refuri="http://indirect.external">
    <target name="_:5:_">
    <paragraph>
        <reference refuri="http://full">
            Full syntax anonymous external hyperlink reference
        ,
        <reference refuri="http://simplified">
            chained anonymous external reference
        ,
        <reference refuri="http://simplified">
            simplified syntax anonymous external hyperlink reference
        ,
        <reference refuri="http://indirect.external">
            indirect anonymous hyperlink reference
        ,
        <reference refname="_:5:_">
            internal anonymous hyperlink reference
        .
"""],
["""\
Duplicate external target_'s (different URIs):

.. _target: first

.. _target: second
""",
"""\
<document>
    <paragraph>
        Duplicate external \n\
        <reference refname="target">
            target
        's (different URIs):
    <target dupname="target" refuri="first">
    <system_message level="2" type="WARNING">
        <paragraph>
            Duplicate explicit target name: "target"
    <target dupname="target" refuri="second">
"""],
])


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
