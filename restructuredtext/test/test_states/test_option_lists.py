#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/09/13 02:40:46 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['option_lists'] = [
["""\
Short options:

-a       option a

-b file  option b

-cname   option c
""",
"""\
<document>
    <paragraph>
        Short options:
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
            <description>
                <paragraph>
                    option a
        <option_list_item>
            <option>
                <short_option>
                    -b
                <option_argument>
                    file
            <description>
                <paragraph>
                    option b
        <option_list_item>
            <option>
                <short_option>
                    -c
                <option_argument>
                    name
            <description>
                <paragraph>
                    option c
"""],
["""\
Long options:

--aaaa       option aaaa
--bbbb=file  option bbbb
--cccc name  option cccc
--d-e-f-g    option d-e-f-g
--h_i_j_k    option h_i_j_k
""",
"""\
<document>
    <paragraph>
        Long options:
    <option_list>
        <option_list_item>
            <option>
                <long_option>
                    --aaaa
            <description>
                <paragraph>
                    option aaaa
        <option_list_item>
            <option>
                <long_option>
                    --bbbb
                <option_argument>
                    file
            <description>
                <paragraph>
                    option bbbb
        <option_list_item>
            <option>
                <long_option>
                    --cccc
                <option_argument>
                    name
            <description>
                <paragraph>
                    option cccc
        <option_list_item>
            <option>
                <long_option>
                    --d-e-f-g
            <description>
                <paragraph>
                    option d-e-f-g
        <option_list_item>
            <option>
                <long_option>
                    --h_i_j_k
            <description>
                <paragraph>
                    option h_i_j_k
"""],
["""\
VMS/DOS-style options:

/A        option A
/B file   option B
/Cstring  option C
""",
"""\
<document>
    <paragraph>
        VMS/DOS-style options:
    <option_list>
        <option_list_item>
            <option>
                <vms_option>
                    /A
            <description>
                <paragraph>
                    option A
        <option_list_item>
            <option>
                <vms_option>
                    /B
                <option_argument>
                    file
            <description>
                <paragraph>
                    option B
        <option_list_item>
            <option>
                <vms_option>
                    /C
                <option_argument>
                    string
            <description>
                <paragraph>
                    option C
"""],
["""\
Mixed short, long, and VMS/DOS options:

-a           option a
--bbbb=file  option bbbb
/C           option C
--dddd name  option dddd
-e string    option e
/F file      option F
""",
"""\
<document>
    <paragraph>
        Mixed short, long, and VMS/DOS options:
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
            <description>
                <paragraph>
                    option a
        <option_list_item>
            <option>
                <long_option>
                    --bbbb
                <option_argument>
                    file
            <description>
                <paragraph>
                    option bbbb
        <option_list_item>
            <option>
                <vms_option>
                    /C
            <description>
                <paragraph>
                    option C
        <option_list_item>
            <option>
                <long_option>
                    --dddd
                <option_argument>
                    name
            <description>
                <paragraph>
                    option dddd
        <option_list_item>
            <option>
                <short_option>
                    -e
                <option_argument>
                    string
            <description>
                <paragraph>
                    option e
        <option_list_item>
            <option>
                <vms_option>
                    /F
                <option_argument>
                    file
            <description>
                <paragraph>
                    option F
"""],
["""\
Aliased options:

-a, --aaaa, /A                 option a, aaaa, A
-b file, --bbbb=file, /B file  option b, bbbb, B
""",
"""\
<document>
    <paragraph>
        Aliased options:
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
            <option>
                <long_option>
                    --aaaa
            <option>
                <vms_option>
                    /A
            <description>
                <paragraph>
                    option a, aaaa, A
        <option_list_item>
            <option>
                <short_option>
                    -b
                <option_argument>
                    file
            <option>
                <long_option>
                    --bbbb
                <option_argument>
                    file
            <option>
                <vms_option>
                    /B
                <option_argument>
                    file
            <description>
                <paragraph>
                    option b, bbbb, B
"""],
["""\
Multiple lines in descriptions, aligned:

-a       option a, line 1
         line 2
-b file  option b, line 1
         line 2
""",
"""\
<document>
    <paragraph>
        Multiple lines in descriptions, aligned:
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
            <description>
                <paragraph>
                    option a, line 1
                    line 2
        <option_list_item>
            <option>
                <short_option>
                    -b
                <option_argument>
                    file
            <description>
                <paragraph>
                    option b, line 1
                    line 2
"""],
["""\
Multiple lines in descriptions, not aligned:

-a  option a, line 1
    line 2
-b file  option b, line 1
    line 2
""",
"""\
<document>
    <paragraph>
        Multiple lines in descriptions, not aligned:
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
            <description>
                <paragraph>
                    option a, line 1
                    line 2
        <option_list_item>
            <option>
                <short_option>
                    -b
                <option_argument>
                    file
            <description>
                <paragraph>
                    option b, line 1
                    line 2
"""],
["""\
Descriptions begin on next line:

-a
    option a, line 1
    line 2
-b file
    option b, line 1
    line 2
""",
"""\
<document>
    <paragraph>
        Descriptions begin on next line:
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
            <description>
                <paragraph>
                    option a, line 1
                    line 2
        <option_list_item>
            <option>
                <short_option>
                    -b
                <option_argument>
                    file
            <description>
                <paragraph>
                    option b, line 1
                    line 2
"""],
["""\
Multiple body elements in descriptions:

-a  option a, para 1

    para 2
-b file
    option b, para 1

    para 2
""",
"""\
<document>
    <paragraph>
        Multiple body elements in descriptions:
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
            <description>
                <paragraph>
                    option a, para 1
                <paragraph>
                    para 2
        <option_list_item>
            <option>
                <short_option>
                    -b
                <option_argument>
                    file
            <description>
                <paragraph>
                    option b, para 1
                <paragraph>
                    para 2
"""],
["""\
--option
empty item above, no blank line
""",
"""\
<document>
    <option_list>
        <option_list_item>
            <option>
                <long_option>
                    --option
            <description>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
    <paragraph>
        empty item above, no blank line
"""],
["""\
Some edge cases:

--option=arg arg  too many arguments

--option=arg=arg  too many arguments

-aletter arg      too many arguments (-a letter)

/Aletter arg      too many arguments (/A letter)

-a=b              can't use = for short arguments

/A=b              can't use = for DOS/VMS arguments?

--option=         argument missing

--=argument       option missing

--                everything missing

-                 this should be a bullet list item
""",
"""\
<document>
    <paragraph>
        Some edge cases:
    <paragraph>
        --option=arg arg  too many arguments
    <paragraph>
        --option=arg=arg  too many arguments
    <paragraph>
        -aletter arg      too many arguments (-a letter)
    <paragraph>
        /Aletter arg      too many arguments (/A letter)
    <paragraph>
        -a=b              can't use = for short arguments
    <paragraph>
        /A=b              can't use = for DOS/VMS arguments?
    <paragraph>
        --option=         argument missing
    <paragraph>
        --=argument       option missing
    <paragraph>
        --                everything missing
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                this should be a bullet list item
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
