#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:05:04 $
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
        </emphasis>
    </paragraph>
</document>
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
        </emphasis>
    </paragraph>
</document>
"""],
["""\
*emphasis
""",
"""\
<document>
    <paragraph>
        *emphasis
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Inline emphasis start-string without end-string at line 1.
        </paragraph>
    </system_warning>
</document>
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
        </emphasis>
        ' but not '*' or '"*"' or  x*2* or 2*x* or *args or *
        or 
        <emphasis>
            the* *stars\\* *inside
        </emphasis>
    </paragraph>
    <paragraph>
        (however, '*args' will trigger a warning and may be problematic)
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Inline emphasis start-string without end-string at line 4.
        </paragraph>
    </system_warning>
    <paragraph>
        what about 
        <emphasis>
            this*
        </emphasis>
        ?
    </paragraph>
</document>
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
        </emphasis>
    </paragraph>
    <paragraph>
        Emphasized double asterisk: 
        <emphasis>
            **
        </emphasis>
    </paragraph>
</document>
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
        </strong>
    </paragraph>
</document>
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
        </strong>
        ) but not (**) or '(** ' or x**2 or **kwargs or **
    </paragraph>
    <paragraph>
        (however, '**kwargs' will trigger a warning and may be problematic)
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Inline strong start-string without end-string at line 3.
        </paragraph>
    </system_warning>
</document>
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
        </strong>
    </paragraph>
    <paragraph>
        Strong double asterisk: 
        <strong>
            **
        </strong>
    </paragraph>
</document>
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
        </literal>
    </paragraph>
</document>
"""],
["""\
``\\literal``
""",
"""\
<document>
    <paragraph>
        <literal>
            \\literal
        </literal>
    </paragraph>
</document>
"""],
["""\
``lite\\ral``
""",
"""\
<document>
    <paragraph>
        <literal>
            lite\\ral
        </literal>
    </paragraph>
</document>
"""],
["""\
``literal\\``
""",
"""\
<document>
    <paragraph>
        <literal>
            literal\\
        </literal>
    </paragraph>
</document>
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
        </literal>
         but not "``" or ``
    </paragraph>
    <paragraph>
        (however, ``standalone TeX quotes'' will trigger a warning
        and may be problematic)
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Inline literal start-string without end-string at line 3.
        </paragraph>
    </system_warning>
</document>
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
        </literal>
         in this paragraph!
    </paragraph>
</document>
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
        </interpreted>
    </paragraph>
</document>
"""],
["""\
:role:`interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted position="prefix" role="role">
            interpreted
        </interpreted>
    </paragraph>
</document>
"""],
["""\
`interpreted`:role:
""",
"""\
<document>
    <paragraph>
        <interpreted position="suffix" role="role">
            interpreted
        </interpreted>
    </paragraph>
</document>
"""],
["""\
:role:`:not-role: interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted position="prefix" role="role">
            :not-role: interpreted
        </interpreted>
    </paragraph>
</document>
"""],
["""\
:very.long-role_name:`interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted position="prefix" role="very.long-role_name">
            interpreted
        </interpreted>
    </paragraph>
</document>
"""],
["""\
`interpreted` but not \\`interpreted` [`] or ({[`] or [`]}) or `
""",
"""\
<document>
    <paragraph>
        <interpreted>
            interpreted
        </interpreted>
         but not `interpreted` [`] or ({[`] or [`]}) or `
    </paragraph>
</document>
"""],
["""\
`interpreted`-text `interpreted`: text `interpreted`:text `text`'s interpreted
""",
"""\
<document>
    <paragraph>
        <interpreted>
            interpreted
        </interpreted>
        -text 
        <interpreted>
            interpreted
        </interpreted>
        : text 
        <interpreted>
            interpreted
        </interpreted>
        :text 
        <interpreted>
            text
        </interpreted>
        's interpreted
    </paragraph>
</document>
"""],
]

totest['link'] = [
["""\
link_
""",
"""\
<document>
    <paragraph>
        <link refname="link">
            link
        </link>
    </paragraph>
</document>
"""],
["""\
link_, l_, and l_i-n_k_, but not _link_ or -link_ or link__
""",
"""\
<document>
    <paragraph>
        <link refname="link">
            link
        </link>
        , 
        <link refname="l">
            l
        </link>
        , and 
        <link refname="l_i-n_k">
            l_i-n_k
        </link>
        , but not _link_ or -link_ or link__
    </paragraph>
</document>
"""],
]

totest['phrase_link'] = [
["""\
`phrase link`_
""",
"""\
<document>
    <paragraph>
        <link refname="phrase link">
            phrase link
        </link>
    </paragraph>
</document>
"""],
["""\
`phrase link
across lines`_
""",
"""\
<document>
    <paragraph>
        <link refname="phrase link across lines">
            phrase link
            across lines
        </link>
    </paragraph>
</document>
"""],
["""\
`phrase\`_ link`_
""",
"""\
<document>
    <paragraph>
        <link refname="phrase`_ link">
            phrase`_ link
        </link>
    </paragraph>
</document>
"""],
["""\
Invalid phrase link:

:role:`phrase link`_
""",
"""\
<document>
    <paragraph>
        Invalid phrase link:
    </paragraph>
    <paragraph>
        :role:`phrase link`_
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Mismatch: inline interpreted text start-string and role with phrase-link end-string at line 3.
        </paragraph>
    </system_warning>
</document>
"""],
["""\
Invalid phrase link:

`phrase link`:role:_
""",
"""\
<document>
    <paragraph>
        Invalid phrase link:
    </paragraph>
    <paragraph>
        <interpreted>
            phrase link
        </interpreted>
        :role:_
    </paragraph>
</document>
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
        </footnote_reference>
    </paragraph>
</document>
"""],
["""\
[footnote]_ and [foot-note]_ and [foot.note]_ and [1]_ but not [foot note]_
""",
"""\
<document>
    <paragraph>
        <footnote_reference refname="footnote">
            footnote
        </footnote_reference>
         and 
        <footnote_reference refname="foot-note">
            foot-note
        </footnote_reference>
         and 
        <footnote_reference refname="foot.note">
            foot.note
        </footnote_reference>
         and 
        <footnote_reference refname="1">
            1
        </footnote_reference>
         but not [foot note]_
    </paragraph>
</document>
"""],
]

totest['standalone_hyperlink'] = [
["""\
http://www.standalone.hyperlink.com

one-slash-only:/absolute.path

mailto:someone@somewhere.com

news:comp.lang.python

An email address in a sentence: someone@somewhere.com.

ftp://ends.with.a.period.

(a.question.mark@end?)
""",
"""\
<document>
    <paragraph>
        <link refuri="http://www.standalone.hyperlink.com">
            http://www.standalone.hyperlink.com
        </link>
    </paragraph>
    <paragraph>
        <link refuri="one-slash-only:/absolute.path">
            one-slash-only:/absolute.path
        </link>
    </paragraph>
    <paragraph>
        <link refuri="mailto:someone@somewhere.com">
            mailto:someone@somewhere.com
        </link>
    </paragraph>
    <paragraph>
        <link refuri="news:comp.lang.python">
            news:comp.lang.python
        </link>
    </paragraph>
    <paragraph>
        An email address in a sentence: 
        <link refuri="mailto:someone@somewhere.com">
            someone@somewhere.com
        </link>
        .
    </paragraph>
    <paragraph>
        <link refuri="ftp://ends.with.a.period">
            ftp://ends.with.a.period
        </link>
        .
    </paragraph>
    <paragraph>
        (
        <link refuri="mailto:a.question.mark@end">
            a.question.mark@end
        </link>
        ?)
    </paragraph>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
