#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.15 $
:Date: $Date: 2002/02/20 04:25:08 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['emphasis'] = [
["""\
*emphasis*
""",
"""\
<document>
    <paragraph>
        <emphasis>
            emphasis
"""],
["""\
*emphasized sentence
across lines*
""",
"""\
<document>
    <paragraph>
        <emphasis>
            emphasized sentence
            across lines
"""],
["""\
*emphasis
""",
"""\
<document>
    <paragraph>
        *emphasis
    <system_message level="2" type="WARNING">
        <paragraph>
            Inline emphasis start-string without end-string at line 1.
"""],
["""\
'*emphasis*' but not '*' or '"*"' or  x*2* or 2*x* or \\*args or *
or *the\\* *stars\\\\\\* *inside*

(however, '*args' will trigger a warning and may be problematic)

what about *this**?
""",
"""\
<document>
    <paragraph>
        '
        <emphasis>
            emphasis
        ' but not '*' or '"*"' or  x*2* or 2*x* or *args or *
        or \n\
        <emphasis>
            the* *stars\\* *inside
    <paragraph>
        (however, '*args' will trigger a warning and may be problematic)
    <system_message level="2" type="WARNING">
        <paragraph>
            Inline emphasis start-string without end-string at line 4.
    <paragraph>
        what about \n\
        <emphasis>
            this*
        ?
"""],
["""\
Emphasized asterisk: *\\**

Emphasized double asterisk: *\\***
""",
"""\
<document>
    <paragraph>
        Emphasized asterisk: \n\
        <emphasis>
            *
    <paragraph>
        Emphasized double asterisk: \n\
        <emphasis>
            **
"""],
]

totest['strong'] = [
["""\
**strong**
""",
"""\
<document>
    <paragraph>
        <strong>
            strong
"""],
["""\
(**strong**) but not (**) or '(** ' or x**2 or \\**kwargs or **

(however, '**kwargs' will trigger a warning and may be problematic)
""",
"""\
<document>
    <paragraph>
        (
        <strong>
            strong
        ) but not (**) or '(** ' or x**2 or **kwargs or **
    <paragraph>
        (however, '**kwargs' will trigger a warning and may be problematic)
    <system_message level="2" type="WARNING">
        <paragraph>
            Inline strong start-string without end-string at line 3.
"""],
["""\
Strong asterisk: *****

Strong double asterisk: ******
""",
"""\
<document>
    <paragraph>
        Strong asterisk: \n\
        <strong>
            *
    <paragraph>
        Strong double asterisk: \n\
        <strong>
            **
"""],
]

totest['literal'] = [
["""\
``literal``
""",
"""\
<document>
    <paragraph>
        <literal>
            literal
"""],
["""\
``\\literal``
""",
"""\
<document>
    <paragraph>
        <literal>
            \\literal
"""],
["""\
``lite\\ral``
""",
"""\
<document>
    <paragraph>
        <literal>
            lite\\ral
"""],
["""\
``literal\\``
""",
"""\
<document>
    <paragraph>
        <literal>
            literal\\
"""],
["""\
``literal ``TeX quotes'' & \\backslash`` but not "``" or ``

(however, ``standalone TeX quotes'' will trigger a warning
and may be problematic)
""",
"""\
<document>
    <paragraph>
        <literal>
            literal ``TeX quotes'' & \\backslash
         but not "``" or ``
    <paragraph>
        (however, ``standalone TeX quotes'' will trigger a warning
        and may be problematic)
    <system_message level="2" type="WARNING">
        <paragraph>
            Inline literal start-string without end-string at line 3.
"""],
["""\
Find the ```interpreted text``` in this paragraph!
""",
"""\
<document>
    <paragraph>
        Find the \n\
        <literal>
            `interpreted text`
         in this paragraph!
"""],
]

totest['interpreted'] = [
["""\
`interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted>
            interpreted
"""],
["""\
:role:`interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted position="prefix" role="role">
            interpreted
"""],
["""\
`interpreted`:role:
""",
"""\
<document>
    <paragraph>
        <interpreted position="suffix" role="role">
            interpreted
"""],
["""\
:role:`:not-role: interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted position="prefix" role="role">
            :not-role: interpreted
"""],
["""\
:very.long-role_name:`interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted position="prefix" role="very.long-role_name">
            interpreted
"""],
["""\
`interpreted` but not \\`interpreted` [`] or ({[`] or [`]}) or `
""",
"""\
<document>
    <paragraph>
        <interpreted>
            interpreted
         but not `interpreted` [`] or ({[`] or [`]}) or `
"""],
["""\
`interpreted`-text `interpreted`: text `interpreted`:text `text`'s interpreted
""",
"""\
<document>
    <paragraph>
        <interpreted>
            interpreted
        -text \n\
        <interpreted>
            interpreted
        : text \n\
        <interpreted>
            interpreted
        :text \n\
        <interpreted>
            text
        's interpreted
"""],
]

totest['references'] = [
["""\
ref_
""",
"""\
<document>
    <paragraph>
        <reference refname="ref">
            ref
"""],
["""\
ref__
""",
"""\
<document>
    <paragraph>
        <reference anonymous="1">
            ref
"""],
["""\
ref_, r_, r_e-f_, and anonymousref__, but not _ref_ or -ref_
""",
"""\
<document>
    <paragraph>
        <reference refname="ref">
            ref
        , \n\
        <reference refname="r">
            r
        , \n\
        <reference refname="r_e-f">
            r_e-f
        , and \n\
        <reference anonymous="1">
            anonymousref
        , but not _ref_ or -ref_
"""],
]

totest['phrase_references'] = [
["""\
`phrase reference`_
""",
"""\
<document>
    <paragraph>
        <reference refname="phrase reference">
            phrase reference
"""],
["""\
`anonymous reference`__
""",
"""\
<document>
    <paragraph>
        <reference anonymous="1">
            anonymous reference
"""],
["""\
`phrase reference
across lines`_
""",
"""\
<document>
    <paragraph>
        <reference refname="phrase reference across lines">
            phrase reference
            across lines
"""],
["""\
`phrase\`_ reference`_
""",
"""\
<document>
    <paragraph>
        <reference refname="phrase`_ reference">
            phrase`_ reference
"""],
["""\
Invalid phrase reference:

:role:`phrase reference`_
""",
"""\
<document>
    <paragraph>
        Invalid phrase reference:
    <paragraph>
        :role:`phrase reference`_
    <system_message level="2" type="WARNING">
        <paragraph>
            Mismatch: inline interpreted text start-string and role with phrase-reference end-string at line 3.
"""],
["""\
Invalid phrase reference:

`phrase reference`:role:_
""",
"""\
<document>
    <paragraph>
        Invalid phrase reference:
    <paragraph>
        <interpreted>
            phrase reference
        :role:_
"""],
]

totest['inline_targets'] = [
["""\
_`target`

Here is _`another target` in some text. And _`yet
another target`, spanning lines.

_`Here is  a    TaRgeT` with case and spacial difficulties.
""",
"""\
<document>
    <paragraph>
        <target id="id1" name="target">
            target
    <paragraph>
        Here is \n\
        <target id="id2" name="another target">
            another target
         in some text. And \n\
        <target id="id3" name="yet another target">
            yet
            another target
        , spanning lines.
    <paragraph>
        <target id="id4" name="here is a target">
            Here is  a    TaRgeT
         with case and spacial difficulties.
"""],
["""\
But this isn't a _target; targets require backquotes.

And _`this`_ is just plain confusing.
""",
"""\
<document>
    <paragraph>
        But this isn't a _target; targets require backquotes.
    <paragraph>
        And _`this`_ is just plain confusing.
    <system_message level="2" type="WARNING">
        <paragraph>
            Inline target start-string without end-string at line 3.
"""],
]

totest['footnote_reference'] = [
["""\
[footnote]_
""",
"""\
<document>
    <paragraph>
        <footnote_reference refname="footnote">
            footnote
"""],
["""\
[footnote]_ and [foot-note]_ and [foot.note]_ and [1]_ but not [foot note]_
""",
"""\
<document>
    <paragraph>
        <footnote_reference refname="footnote">
            footnote
         and \n\
        <footnote_reference refname="foot-note">
            foot-note
         and \n\
        <footnote_reference refname="foot.note">
            foot.note
         and \n\
        <footnote_reference refname="1">
            1
         but not [foot note]_
"""],
]

totest['substitution_references'] = [
["""\
|subref|
""",
"""\
<document>
    <paragraph>
        <substitution_reference refname="subref">
            subref
"""],
["""\
|subref|_ and |subref|__
""",
"""\
<document>
    <paragraph>
        <reference refname="subref">
            <substitution_reference refname="subref">
                subref
         and \n\
        <reference anonymous="1">
            <substitution_reference refname="subref">
                subref
"""],
["""\
|substitution reference|
""",
"""\
<document>
    <paragraph>
        <substitution_reference refname="substitution reference">
            substitution reference
"""],
["""\
|substitution
reference|
""",
"""\
<document>
    <paragraph>
        <substitution_reference refname="substitution reference">
            substitution
            reference
"""],
]

totest['standalone_hyperlink'] = [
["""\
http://www.standalone.hyperlink.com

http:/one-slash-only.absolute.path

http://[1080:0:0:0:8:800:200C:417A]/IPv6address.html

http://[3ffe:2a00:100:7031::1]

mailto:someone@somewhere.com

news:comp.lang.python

An email address in a sentence: someone@somewhere.com.

ftp://ends.with.a.period.

(a.question.mark@end?)
""",
"""\
<document>
    <paragraph>
        <reference refuri="http://www.standalone.hyperlink.com">
            http://www.standalone.hyperlink.com
    <paragraph>
        <reference refuri="http:/one-slash-only.absolute.path">
            http:/one-slash-only.absolute.path
    <paragraph>
        <reference refuri="http://[1080:0:0:0:8:800:200C:417A]/IPv6address.html">
            http://[1080:0:0:0:8:800:200C:417A]/IPv6address.html
    <paragraph>
        <reference refuri="http://[3ffe:2a00:100:7031::1]">
            http://[3ffe:2a00:100:7031::1]
    <paragraph>
        <reference refuri="mailto:someone@somewhere.com">
            mailto:someone@somewhere.com
    <paragraph>
        <reference refuri="news:comp.lang.python">
            news:comp.lang.python
    <paragraph>
        An email address in a sentence: \n\
        <reference refuri="mailto:someone@somewhere.com">
            someone@somewhere.com
        .
    <paragraph>
        <reference refuri="ftp://ends.with.a.period">
            ftp://ends.with.a.period
        .
    <paragraph>
        (
        <reference refuri="mailto:a.question.mark@end">
            a.question.mark@end
        ?)
"""],
["""\
None of these are standalone hyperlinks (their "schemes"
are not recognized): signal:noise, a:b.
""",
"""\
<document>
    <paragraph>
        None of these are standalone hyperlinks (their "schemes"
        are not recognized): signal:noise, a:b.
"""],
]

totest['miscellaneous'] = [
["""\
__This__ should be left alone.
""",
"""\
<document>
    <paragraph>
        __This__ should be left alone.
"""],
]


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
