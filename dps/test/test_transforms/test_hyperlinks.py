#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.8 $
:Date: $Date: 2002/03/28 04:32:22 $
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
totest['exhaustive_hyperlinks'] = ((Hyperlinks,), [
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
    <target id="direct" name="direct" refuri="http://direct">
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
    <target id="indirect" name="indirect" refuri="http://indirect">
    <target id="xtarget" name="xtarget" refuri="http://indirect">
"""],
["""\
.. _direct:

direct_ internal
""",
"""\
<document>
    <target id="direct" name="direct">
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
    <target id="ztarget" name="ztarget">
    <paragraph>
        <reference refname="ztarget">
            indirect
         internal
    <target id="indirect2" name="indirect2" refname="ztarget">
    <target id="indirect" name="indirect" refname="ztarget">
"""],
["""\
Implicit
--------

indirect_ internal

.. _indirect: implicit_
""",
"""\
<document>
    <section id="implicit" name="implicit">
        <title>
            Implicit
        <paragraph>
            <reference refname="implicit">
                indirect
             internal
        <target id="indirect" name="indirect" refname="implicit">
"""],
["""\
Implicit
--------

Duplicate implicit targets.

Implicit
--------

indirect_ internal

.. _indirect: implicit_
""",
"""\
<document>
    <section dupname="implicit" id="implicit">
        <title>
            Implicit
        <paragraph>
            Duplicate implicit targets.
    <section dupname="implicit" id="id1">
        <title>
            Implicit
        <system_message level="1" refid="id1" type="INFO">
            <paragraph>
                Duplicate implicit target name: "implicit".
        <paragraph>
            <reference refname="implicit">
                indirect
             internal
        <target id="indirect" name="indirect" refname="implicit">
    <system_message level="2" type="WARNING">
        <paragraph>
            Indirect hyperlink target "indirect" refers to target "implicit", which does not exist.
"""],
["""\
`direct external`__

__ http://direct
""",
"""\
<document>
    <paragraph>
        <reference anonymous="1" refuri="http://direct">
            direct external
    <target anonymous="1" id="id1" name="_:1:_" refuri="http://direct">
"""],
["""\
`indirect external`__

__ xtarget_
.. _xtarget: http://indirect
""",
"""\
<document>
    <paragraph>
        <reference anonymous="1" refuri="http://indirect">
            indirect external
    <target anonymous="1" id="id1" name="_:1:_" refuri="http://indirect">
    <target id="xtarget" name="xtarget" refuri="http://indirect">
"""],
["""\
__

`direct internal`__
""",
"""\
<document>
    <target anonymous="1" id="id1" name="_:1:_">
    <paragraph>
        <reference anonymous="1" refname="_:1:_">
            direct internal
"""],
["""\
.. _ztarget:

`indirect internal`__

__ ztarget_
""",
"""\
<document>
    <target id="ztarget" name="ztarget">
    <paragraph>
        <reference anonymous="1" refname="ztarget">
            indirect internal
    <target anonymous="1" id="id1" name="_:1:_" refname="ztarget">
"""],
["""\
.. _ztarget:

First

.. _ztarget:

Second

`indirect internal`__

__ ztarget_
""",
"""\
<document>
    <target dupname="ztarget" id="ztarget">
    <paragraph>
        First
    <system_message level="2" refid="id1" type="WARNING">
        <paragraph>
            Duplicate explicit target name: "ztarget".
    <target dupname="ztarget" id="id1">
    <paragraph>
        Second
    <paragraph>
        <reference anonymous="1" refname="ztarget">
            indirect internal
    <target anonymous="1" id="id2" name="_:1:_" refname="ztarget">
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
    <target id="internal-hyperlink" name="internal hyperlink">
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
    <target id="chained" name="chained">
    <target id="internal-hyperlink" name="internal hyperlink">
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
    <target id="external-hyperlink" name="external hyperlink" refuri="http://uri">
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
    <target id="external-hyperlink" name="external hyperlink" refuri="http://uri">
    <target id="indirect-target" name="indirect target" refuri="http://uri">
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
    <target id="chained" name="chained" refuri="http://uri">
    <target id="external-hyperlink" name="external hyperlink" refuri="http://uri">
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
    <target id="external-hyperlink" name="external hyperlink" refuri="http://uri">
    <target id="indirect-hyperlink" name="indirect hyperlink" refuri="http://uri">
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
    <target id="external-hyperlink" name="external hyperlink" refuri="http://uri">
    <target id="chained" name="chained" refuri="http://uri">
    <target id="indirect-hyperlink" name="indirect hyperlink" refuri="http://uri">
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
    <target anonymous="1" id="id1" name="_:1:_" refuri="http://full">
    <target anonymous="1" id="id2" name="_:2:_" refuri="http://simplified">
    <target anonymous="1" id="id3" name="_:3:_" refuri="http://simplified">
    <target id="external" name="external" refuri="http://indirect.external">
    <target anonymous="1" id="id4" name="_:4:_" refuri="http://indirect.external">
    <target anonymous="1" id="id5" name="_:5:_">
    <paragraph>
        <reference anonymous="1" refuri="http://full">
            Full syntax anonymous external hyperlink reference
        ,
        <reference anonymous="1" refuri="http://simplified">
            chained anonymous external reference
        ,
        <reference anonymous="1" refuri="http://simplified">
            simplified syntax anonymous external hyperlink reference
        ,
        <reference anonymous="1" refuri="http://indirect.external">
            indirect anonymous hyperlink reference
        ,
        <reference anonymous="1" refname="_:5:_">
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
    <target dupname="target" id="target" refuri="first">
    <system_message level="2" refid="id1" type="WARNING">
        <paragraph>
            Duplicate explicit target name: "target".
    <target dupname="target" id="id1" refuri="second">
"""],
])


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
