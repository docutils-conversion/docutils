#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.7 $
:Date: $Date: 2001/10/31 05:48:00 $
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
    <system_warning level="1">
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
        or 
        <emphasis>
            the* *stars\\* *inside
    <paragraph>
        (however, '*args' will trigger a warning and may be problematic)
    <system_warning level="1">
        <paragraph>
            Inline emphasis start-string without end-string at line 4.
    <paragraph>
        what about 
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
        Emphasized asterisk: 
        <emphasis>
            *
    <paragraph>
        Emphasized double asterisk: 
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
    <system_warning level="1">
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
        Strong asterisk: 
        <strong>
            *
    <paragraph>
        Strong double asterisk: 
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
    <system_warning level="1">
        <paragraph>
            Inline literal start-string without end-string at line 3.
"""],
["""\
Find the ```interpreted text``` in this paragraph!
""",
"""\
<document>
    <paragraph>
        Find the 
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
        -text 
        <interpreted>
            interpreted
        : text 
        <interpreted>
            interpreted
        :text 
        <interpreted>
            text
        's interpreted
"""],
]

totest['links'] = [
["""\
link_
""",
"""\
<document>
    <paragraph>
        <reference refname="link">
            link
"""],
["""\
link__
""",
"""\
<document>
    <paragraph>
        <reference anonymous="1" refname="link">
            link
"""],
["""\
link_, l_, l_i-n_k_, and anonymouslink__, but not _link_ or -link_
""",
"""\
<document>
    <paragraph>
        <reference refname="link">
            link
        , 
        <reference refname="l">
            l
        , 
        <reference refname="l_i-n_k">
            l_i-n_k
        , and 
        <reference anonymous="1" refname="anonymouslink">
            anonymouslink
        , but not _link_ or -link_
"""],
]

totest['phrase_links'] = [
["""\
`phrase link`_
""",
"""\
<document>
    <paragraph>
        <reference refname="phrase link">
            phrase link
"""],
["""\
`anonymous link`__
""",
"""\
<document>
    <paragraph>
        <reference anonymous="1" refname="anonymous link">
            anonymous link
"""],
["""\
`phrase link
across lines`_
""",
"""\
<document>
    <paragraph>
        <reference refname="phrase link across lines">
            phrase link
            across lines
"""],
["""\
`phrase\`_ link`_
""",
"""\
<document>
    <paragraph>
        <reference refname="phrase`_ link">
            phrase`_ link
"""],
["""\
Invalid phrase link:

:role:`phrase link`_
""",
"""\
<document>
    <paragraph>
        Invalid phrase link:
    <paragraph>
        :role:`phrase link`_
    <system_warning level="1">
        <paragraph>
            Mismatch: inline interpreted text start-string and role with phrase-link end-string at line 3.
"""],
["""\
Invalid phrase link:

`phrase link`:role:_
""",
"""\
<document>
    <paragraph>
        Invalid phrase link:
    <paragraph>
        <interpreted>
            phrase link
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
        <target name="target">
            target
    <paragraph>
        Here is 
        <target name="another target">
            another target
         in some text. And 
        <target name="yet another target">
            yet
            another target
        , spanning lines.
    <paragraph>
        <target name="here is a target">
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
    <system_warning level="1">
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
         and 
        <footnote_reference refname="foot-note">
            foot-note
         and 
        <footnote_reference refname="foot.note">
            foot.note
         and 
        <footnote_reference refname="1">
            1
         but not [foot note]_
"""],
]

totest['standalone_hyperlink'] = [
["""\
http://www.standalone.hyperlink.com

http:/one-slash-only.absolute.path

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
        <reference refuri="mailto:someone@somewhere.com">
            mailto:someone@somewhere.com
    <paragraph>
        <reference refuri="news:comp.lang.python">
            news:comp.lang.python
    <paragraph>
        An email address in a sentence: 
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

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
