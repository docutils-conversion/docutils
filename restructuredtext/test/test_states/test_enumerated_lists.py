#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:03:34 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['enumerated_lists'] = [
["""\
1. Item one.

2. Item two.

3. Item three.
""",
"""\
<document>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item>
            <paragraph>
                Item one.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item two.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item three.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
No blank lines betwen items:

1. Item one.
2. Item two.
3. Item three.
""",
"""\
<document>
    <paragraph>
        No blank lines betwen items:
    </paragraph>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item>
            <paragraph>
                Item one.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item two.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item three.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
1.
empty item above, no blank line
""",
"""\
<document>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item/>
    </enumerated_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
        </paragraph>
    </system_warning>
    <paragraph>
        empty item above, no blank line
    </paragraph>
</document>
"""],
["""\
Scrambled:

3. Item three.
2. Item two.
1. Item one.
""",
"""\
<document>
    <paragraph>
        Scrambled:
    </paragraph>
    <system_warning level="0">
        <paragraph>
            Enumerated list start value not ordinal-1 at line 3: '3' (ordinal 3)
        </paragraph>
    </system_warning>
    <enumerated_list enumtype="arabic" prefix="" start="3" suffix=".">
        <list_item>
            <paragraph>
                Item three.
            </paragraph>
        </list_item>
    </enumerated_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
        </paragraph>
    </system_warning>
    <system_warning level="0">
        <paragraph>
            Enumerated list start value not ordinal-1 at line 4: '2' (ordinal 2)
        </paragraph>
    </system_warning>
    <enumerated_list enumtype="arabic" prefix="" start="2" suffix=".">
        <list_item>
            <paragraph>
                Item two.
            </paragraph>
        </list_item>
    </enumerated_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 5.
        </paragraph>
    </system_warning>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item>
            <paragraph>
                Item one.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
Skipping item 3:

1. Item 1.
2. Item 2.
4. Item 4.
""",
"""\
<document>
    <paragraph>
        Skipping item 3:
    </paragraph>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item>
            <paragraph>
                Item 1.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item 2.
            </paragraph>
        </list_item>
    </enumerated_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
        </paragraph>
    </system_warning>
    <system_warning level="0">
        <paragraph>
            Enumerated list start value not ordinal-1 at line 5: '4' (ordinal 4)
        </paragraph>
    </system_warning>
    <enumerated_list enumtype="arabic" prefix="" start="4" suffix=".">
        <list_item>
            <paragraph>
                Item 4.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
Start with non-ordinal-1:

0. Item zero.
1. Item one.
2. Item two.
3. Item three.

And again:

2. Item two.
3. Item three.
""",
"""\
<document>
    <paragraph>
        Start with non-ordinal-1:
    </paragraph>
    <system_warning level="0">
        <paragraph>
            Enumerated list start value not ordinal-1 at line 3: '0' (ordinal 0)
        </paragraph>
    </system_warning>
    <enumerated_list enumtype="arabic" prefix="" start="0" suffix=".">
        <list_item>
            <paragraph>
                Item zero.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item one.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item two.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item three.
            </paragraph>
        </list_item>
    </enumerated_list>
    <paragraph>
        And again:
    </paragraph>
    <system_warning level="0">
        <paragraph>
            Enumerated list start value not ordinal-1 at line 10: '2' (ordinal 2)
        </paragraph>
    </system_warning>
    <enumerated_list enumtype="arabic" prefix="" start="2" suffix=".">
        <list_item>
            <paragraph>
                Item two.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item three.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
1. Item one: line 1,
   line 2.
2. Item two: line 1,
   line 2.
3. Item three: paragraph 1, line 1,
   line 2.

   Paragraph 2.
""",
"""\
<document>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item>
            <paragraph>
                Item one: line 1,
                line 2.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item two: line 1,
                line 2.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item three: paragraph 1, line 1,
                line 2.
            </paragraph>
            <paragraph>
                Paragraph 2.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
Different enumeration sequences:

1. Item 1.
2. Item 2.
3. Item 3.

A. Item A.
B. Item B.
C. Item C.

a. Item a.
b. Item b.
c. Item c.

I. Item I.
II. Item II.
III. Item III.

i. Item i.
ii. Item ii.
iii. Item iii.
""",
"""\
<document>
    <paragraph>
        Different enumeration sequences:
    </paragraph>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item>
            <paragraph>
                Item 1.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item 2.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item 3.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="upperalpha" prefix="" start="A" suffix=".">
        <list_item>
            <paragraph>
                Item A.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item B.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item C.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="loweralpha" prefix="" start="a" suffix=".">
        <list_item>
            <paragraph>
                Item a.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item b.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item c.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="upperroman" prefix="" start="I" suffix=".">
        <list_item>
            <paragraph>
                Item I.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item II.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item III.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="lowerroman" prefix="" start="i" suffix=".">
        <list_item>
            <paragraph>
                Item i.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item ii.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item iii.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
Bad Roman numerals:

i. i
ii. ii
iii. iii
iiii. iiii

(I) I
(IVXLCDM) IVXLCDM
""",
"""\
<document>
    <paragraph>
        Bad Roman numerals:
    </paragraph>
    <enumerated_list enumtype="lowerroman" prefix="" start="i" suffix=".">
        <list_item>
            <paragraph>
                i
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                ii
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                iii
            </paragraph>
        </list_item>
    </enumerated_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
        </paragraph>
    </system_warning>
    <system_warning level="2">
        <paragraph>
            Enumerated list start value invalid at line 6: 'iiii' (sequence 'lowerroman')
        </paragraph>
    </system_warning>
    <block_quote>
        <paragraph>
            iiii
        </paragraph>
    </block_quote>
    <enumerated_list enumtype="upperroman" prefix="(" start="I" suffix=")">
        <list_item>
            <paragraph>
                I
            </paragraph>
        </list_item>
    </enumerated_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 9.
        </paragraph>
    </system_warning>
    <system_warning level="2">
        <paragraph>
            Enumerated list start value invalid at line 9: 'IVXLCDM' (sequence 'upperroman')
        </paragraph>
    </system_warning>
    <block_quote>
        <paragraph>
            IVXLCDM
        </paragraph>
    </block_quote>
</document>
"""],
["""\
Potentially ambiguous cases:

A. Item A.
B. Item B.
C. Item C.

I. Item I.
II. Item II.
III. Item III.

a. Item a.
b. Item b.
c. Item c.

i. Item i.
ii. Item ii.
iii. Item iii.

Phew! Safe!
""",
"""\
<document>
    <paragraph>
        Potentially ambiguous cases:
    </paragraph>
    <enumerated_list enumtype="upperalpha" prefix="" start="A" suffix=".">
        <list_item>
            <paragraph>
                Item A.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item B.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item C.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="upperroman" prefix="" start="I" suffix=".">
        <list_item>
            <paragraph>
                Item I.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item II.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item III.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="loweralpha" prefix="" start="a" suffix=".">
        <list_item>
            <paragraph>
                Item a.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item b.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item c.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="lowerroman" prefix="" start="i" suffix=".">
        <list_item>
            <paragraph>
                Item i.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item ii.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item iii.
            </paragraph>
        </list_item>
    </enumerated_list>
    <paragraph>
        Phew! Safe!
    </paragraph>
</document>
"""],
["""\
Definitely ambiguous:

A. Item A.
B. Item B.
C. Item C.
D. Item D.
E. Item E.
F. Item F.
G. Item G.
H. Item H.
I. Item I.
II. Item II.
III. Item III.

a. Item a.
b. Item b.
c. Item c.
d. Item d.
e. Item e.
f. Item f.
g. Item g.
h. Item h.
i. Item i.
ii. Item ii.
iii. Item iii.
""",
"""\
<document>
    <paragraph>
        Definitely ambiguous:
    </paragraph>
    <enumerated_list enumtype="upperalpha" prefix="" start="A" suffix=".">
        <list_item>
            <paragraph>
                Item A.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item B.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item C.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item D.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item E.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item F.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item G.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item H.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item I.
            </paragraph>
        </list_item>
    </enumerated_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
        </paragraph>
    </system_warning>
    <system_warning level="0">
        <paragraph>
            Enumerated list start value not ordinal-1 at line 12: 'II' (ordinal 2)
        </paragraph>
    </system_warning>
    <enumerated_list enumtype="upperroman" prefix="" start="II" suffix=".">
        <list_item>
            <paragraph>
                Item II.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item III.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="loweralpha" prefix="" start="a" suffix=".">
        <list_item>
            <paragraph>
                Item a.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item b.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item c.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item d.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item e.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item f.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item g.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item h.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item i.
            </paragraph>
        </list_item>
    </enumerated_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 16.
        </paragraph>
    </system_warning>
    <system_warning level="0">
        <paragraph>
            Enumerated list start value not ordinal-1 at line 24: 'ii' (ordinal 2)
        </paragraph>
    </system_warning>
    <enumerated_list enumtype="lowerroman" prefix="" start="ii" suffix=".">
        <list_item>
            <paragraph>
                Item ii.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item iii.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
Different enumeration formats:

1. Item 1.
2. Item 2.
3. Item 3.

1) Item 1).
2) Item 2).
3) Item 3).

(1) Item (1).
(2) Item (2).
(3) Item (3).
""",
"""\
<document>
    <paragraph>
        Different enumeration formats:
    </paragraph>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item>
            <paragraph>
                Item 1.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item 2.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item 3.
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=")">
        <list_item>
            <paragraph>
                Item 1).
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item 2).
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item 3).
            </paragraph>
        </list_item>
    </enumerated_list>
    <enumerated_list enumtype="arabic" prefix="(" start="1" suffix=")">
        <list_item>
            <paragraph>
                Item (1).
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item (2).
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                Item (3).
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
["""\
Nested enumerated lists:

1. Item 1.

   A) Item A).
   B) Item B).
   C) Item C).

2. Item 2.

   (a) Item (a).

       I) Item I).
       II) Item II).
       III) Item III).

   (b) Item (b).

   (c) Item (c).

       (i) Item (i).
       (ii) Item (ii).
       (iii) Item (iii).

3. Item 3.
""",
"""\
<document>
    <paragraph>
        Nested enumerated lists:
    </paragraph>
    <enumerated_list enumtype="arabic" prefix="" start="1" suffix=".">
        <list_item>
            <paragraph>
                Item 1.
            </paragraph>
            <enumerated_list enumtype="upperalpha" prefix="" start="A" suffix=")">
                <list_item>
                    <paragraph>
                        Item A).
                    </paragraph>
                </list_item>
                <list_item>
                    <paragraph>
                        Item B).
                    </paragraph>
                </list_item>
                <list_item>
                    <paragraph>
                        Item C).
                    </paragraph>
                </list_item>
            </enumerated_list>
        </list_item>
        <list_item>
            <paragraph>
                Item 2.
            </paragraph>
            <enumerated_list enumtype="loweralpha" prefix="(" start="a" suffix=")">
                <list_item>
                    <paragraph>
                        Item (a).
                    </paragraph>
                    <enumerated_list enumtype="upperroman" prefix="" start="I" suffix=")">
                        <list_item>
                            <paragraph>
                                Item I).
                            </paragraph>
                        </list_item>
                        <list_item>
                            <paragraph>
                                Item II).
                            </paragraph>
                        </list_item>
                        <list_item>
                            <paragraph>
                                Item III).
                            </paragraph>
                        </list_item>
                    </enumerated_list>
                </list_item>
                <list_item>
                    <paragraph>
                        Item (b).
                    </paragraph>
                </list_item>
                <list_item>
                    <paragraph>
                        Item (c).
                    </paragraph>
                    <enumerated_list enumtype="lowerroman" prefix="(" start="i" suffix=")">
                        <list_item>
                            <paragraph>
                                Item (i).
                            </paragraph>
                        </list_item>
                        <list_item>
                            <paragraph>
                                Item (ii).
                            </paragraph>
                        </list_item>
                        <list_item>
                            <paragraph>
                                Item (iii).
                            </paragraph>
                        </list_item>
                    </enumerated_list>
                </list_item>
            </enumerated_list>
        </list_item>
        <list_item>
            <paragraph>
                Item 3.
            </paragraph>
        </list_item>
    </enumerated_list>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
