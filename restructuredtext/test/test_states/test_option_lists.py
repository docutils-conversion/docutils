#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/09/02 14:05:53 $
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
                </short_option>
            </option>
            <description>
                <paragraph>
                    option a
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <short_option>
                    -b
                </short_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option b
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <short_option>
                    -c
                </short_option>
                <option_argument>
                    name
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option c
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <long_option>
                    --aaaa
                </long_option>
            </option>
            <description>
                <paragraph>
                    option aaaa
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <long_option>
                    --bbbb
                </long_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option bbbb
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <long_option>
                    --cccc
                </long_option>
                <option_argument>
                    name
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option cccc
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <long_option>
                    --d-e-f-g
                </long_option>
            </option>
            <description>
                <paragraph>
                    option d-e-f-g
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <long_option>
                    --h_i_j_k
                </long_option>
            </option>
            <description>
                <paragraph>
                    option h_i_j_k
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <vms_option>
                    /A
                </vms_option>
            </option>
            <description>
                <paragraph>
                    option A
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <vms_option>
                    /B
                </vms_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option B
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <vms_option>
                    /C
                </vms_option>
                <option_argument>
                    string
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option C
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
                </short_option>
            </option>
            <description>
                <paragraph>
                    option a
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <long_option>
                    --bbbb
                </long_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option bbbb
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <vms_option>
                    /C
                </vms_option>
            </option>
            <description>
                <paragraph>
                    option C
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <long_option>
                    --dddd
                </long_option>
                <option_argument>
                    name
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option dddd
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <short_option>
                    -e
                </short_option>
                <option_argument>
                    string
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option e
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <vms_option>
                    /F
                </vms_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option F
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
                </short_option>
            </option>
            <option>
                <long_option>
                    --aaaa
                </long_option>
            </option>
            <option>
                <vms_option>
                    /A
                </vms_option>
            </option>
            <description>
                <paragraph>
                    option a, aaaa, A
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <short_option>
                    -b
                </short_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <option>
                <long_option>
                    --bbbb
                </long_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <option>
                <vms_option>
                    /B
                </vms_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option b, bbbb, B
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
                </short_option>
            </option>
            <description>
                <paragraph>
                    option a, line 1
                    line 2
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <short_option>
                    -b
                </short_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option b, line 1
                    line 2
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
                </short_option>
            </option>
            <description>
                <paragraph>
                    option a, line 1
                    line 2
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <short_option>
                    -b
                </short_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option b, line 1
                    line 2
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
                </short_option>
            </option>
            <description>
                <paragraph>
                    option a, line 1
                    line 2
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <short_option>
                    -b
                </short_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option b, line 1
                    line 2
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
    </paragraph>
    <option_list>
        <option_list_item>
            <option>
                <short_option>
                    -a
                </short_option>
            </option>
            <description>
                <paragraph>
                    option a, para 1
                </paragraph>
                <paragraph>
                    para 2
                </paragraph>
            </description>
        </option_list_item>
        <option_list_item>
            <option>
                <short_option>
                    -b
                </short_option>
                <option_argument>
                    file
                </option_argument>
            </option>
            <description>
                <paragraph>
                    option b, para 1
                </paragraph>
                <paragraph>
                    para 2
                </paragraph>
            </description>
        </option_list_item>
    </option_list>
</document>
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
                </long_option>
            </option>
            <description/>
        </option_list_item>
    </option_list>
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
    </paragraph>
    <paragraph>
        --option=arg arg  too many arguments
    </paragraph>
    <paragraph>
        --option=arg=arg  too many arguments
    </paragraph>
    <paragraph>
        -aletter arg      too many arguments (-a letter)
    </paragraph>
    <paragraph>
        /Aletter arg      too many arguments (/A letter)
    </paragraph>
    <paragraph>
        -a=b              can't use = for short arguments
    </paragraph>
    <paragraph>
        /A=b              can't use = for DOS/VMS arguments?
    </paragraph>
    <paragraph>
        --option=         argument missing
    </paragraph>
    <paragraph>
        --=argument       option missing
    </paragraph>
    <paragraph>
        --                everything missing
    </paragraph>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                this should be a bullet list item
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
