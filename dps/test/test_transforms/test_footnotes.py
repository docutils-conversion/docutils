#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/01/29 02:17:52 $
:Copyright: This module has been placed in the public domain.

Tests for dps.transforms.references.Footnotes.
"""

import DPSTestSupport
from dps.transforms.references import Footnotes
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

totest['footnotes'] = ((Footnotes,), [
["""\
[label]_

.. [label] text
""",
"""\
<document>
    <paragraph>
        <footnote_reference refname="label">
            label
    <footnote name="label">
        <label>
            label
        <paragraph>
            text
"""],
["""\
[#autolabel]_

.. [#autolabel] text
""",
"""\
<document>
    <paragraph>
        <footnote_reference auto="1" refname="autolabel">
            1
    <footnote auto="1" name="autolabel">
        <label>
            1
        <paragraph>
            text
"""],                                   # @@@ remove "auto" atts?
["""\
autonumber: [#]_

.. [#] text
""",
"""\
<document>
    <paragraph>
        autonumber: \n\
        <footnote_reference auto="1" refname="1">
            1
    <footnote auto="1" name="1">
        <label>
            1
        <paragraph>
            text
"""],
["""\
[#]_ is the first auto-numbered footnote reference.
[#]_ is the second auto-numbered footnote reference.

.. [#] Auto-numbered footnote 1.
.. [#] Auto-numbered footnote 2.
.. [#] Auto-numbered footnote 3.

[#]_ is the third auto-numbered footnote reference.
""",
"""\
<document>
    <paragraph>
        <footnote_reference auto="1" refname="1">
            1
         is the first auto-numbered footnote reference.
        <footnote_reference auto="1" refname="2">
            2
         is the second auto-numbered footnote reference.
    <footnote auto="1" name="1">
        <label>
            1
        <paragraph>
            Auto-numbered footnote 1.
    <footnote auto="1" name="2">
        <label>
            2
        <paragraph>
            Auto-numbered footnote 2.
    <footnote auto="1" name="3">
        <label>
            3
        <paragraph>
            Auto-numbered footnote 3.
    <paragraph>
        <footnote_reference auto="1" refname="3">
            3
         is the third auto-numbered footnote reference.
"""],
["""\
[#third]_ is a reference to the third auto-numbered footnote.

.. [#first] First auto-numbered footnote.
.. [#second] Second auto-numbered footnote.
.. [#third] Third auto-numbered footnote.

[#second]_ is a reference to the second auto-numbered footnote.
[#first]_ is a reference to the first auto-numbered footnote.
[#third]_ is another reference to the third auto-numbered footnote.

Here are some internal cross-references to the implicit targets
generated by the footnotes: first_, second_, third_.
""",
"""\
<document>
    <paragraph>
        <footnote_reference auto="1" refname="third">
            3
         is a reference to the third auto-numbered footnote.
    <footnote auto="1" name="first">
        <label>
            1
        <paragraph>
            First auto-numbered footnote.
    <footnote auto="1" name="second">
        <label>
            2
        <paragraph>
            Second auto-numbered footnote.
    <footnote auto="1" name="third">
        <label>
            3
        <paragraph>
            Third auto-numbered footnote.
    <paragraph>
        <footnote_reference auto="1" refname="second">
            2
         is a reference to the second auto-numbered footnote.
        <footnote_reference auto="1" refname="first">
            1
         is a reference to the first auto-numbered footnote.
        <footnote_reference auto="1" refname="third">
            3
         is another reference to the third auto-numbered footnote.
    <paragraph>
        Here are some internal cross-references to the implicit targets
        generated by the footnotes: \n\
        <reference refname="first">
            first
        , \n\
        <reference refname="second">
            second
        , \n\
        <reference refname="third">
            third
        .
"""],
["""\
Mixed anonymous and labelled auto-numbered footnotes:

[#four]_ should be 4, [#]_ should be 1,
[#]_ should be 3, [#]_ is one too many,
[#two]_ should be 2, and [#six]_ doesn't exist.

.. [#] Auto-numbered footnote 1.
.. [#two] Auto-numbered footnote 2.
.. [#] Auto-numbered footnote 3.
.. [#four] Auto-numbered footnote 4.
.. [#five] Auto-numbered footnote 5.
.. [#five] Auto-numbered footnote 5 again (duplicate).
""",
"""\
<document>
    <paragraph>
        Mixed anonymous and labelled auto-numbered footnotes:
    <paragraph>
        <footnote_reference auto="1" refname="four">
            4
         should be 4, \n\
        <footnote_reference auto="1" refname="1">
            1
         should be 1,
        <footnote_reference auto="1" refname="3">
            3
         should be 3, \n\
        <footnote_reference auto="1">
         is one too many,
        <footnote_reference auto="1" refname="two">
            2
         should be 2, and \n\
        <footnote_reference auto="1" refname="six">
         doesn't exist.
    <footnote auto="1" name="1">
        <label>
            1
        <paragraph>
            Auto-numbered footnote 1.
    <footnote auto="1" name="two">
        <label>
            2
        <paragraph>
            Auto-numbered footnote 2.
    <footnote auto="1" name="3">
        <label>
            3
        <paragraph>
            Auto-numbered footnote 3.
    <footnote auto="1" name="four">
        <label>
            4
        <paragraph>
            Auto-numbered footnote 4.
    <footnote auto="1" dupname="five">
        <label>
            5
        <paragraph>
            Auto-numbered footnote 5.
    <footnote auto="1" dupname="five">
        <label>
            6
        <system_warning level="1">
            <paragraph>
                Duplicate explicit target name: "five"
        <paragraph>
            Auto-numbered footnote 5 again (duplicate).
    <system_warning level="2">
        <paragraph>
            Too many autonumbered footnote references: only 2 corresponding footnotes available.
"""],
["""\
Mixed auto-numbered and manual footnotes:

.. [1] manually numbered
.. [#] auto-numbered
.. [#label] autonumber-labeled
""",
"""\
<document>
    <paragraph>
        Mixed auto-numbered and manual footnotes:
    <footnote dupname="1">
        <label>
            1
        <paragraph>
            manually numbered
    <footnote auto="1" dupname="1">
        <label>
            1
        <paragraph>
            auto-numbered
        <system_warning level="1">
            <paragraph>
                Duplicate explicit target name: "1"
    <footnote auto="1" name="label">
        <label>
            2
        <paragraph>
            autonumber-labeled
"""],
["""\
A labeled autonumbered footnote referece: [#footnote]_.

An unlabeled autonumbered footnote referece: [#]_.

.. [#] Unlabeled autonumbered footnote.
.. [#footnote] Labeled autonumbered footnote.
   Note that the footnotes are not in the same
   order as the references.
""",
"""\
<document>
    <paragraph>
        A labeled autonumbered footnote referece: \n\
        <footnote_reference auto="1" refname="footnote">
            2
        .
    <paragraph>
        An unlabeled autonumbered footnote referece: \n\
        <footnote_reference auto="1" refname="1">
            1
        .
    <footnote auto="1" name="1">
        <label>
            1
        <paragraph>
            Unlabeled autonumbered footnote.
    <footnote auto="1" name="footnote">
        <label>
            2
        <paragraph>
            Labeled autonumbered footnote.
            Note that the footnotes are not in the same
            order as the references.
"""],
])


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
