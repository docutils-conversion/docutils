#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.4 $
:Date: $Date: 2001/09/07 01:46:04 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['tables'] = [
["""\
+-------------------------------------+
| A table with one cell and one line. |
+-------------------------------------+
""",
"""\
<document>
    <table>
        <tgroup cols="1">
            <colspec colwidth="37"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A table with one cell and one line.
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+-----------------------+
| A table with one cell |
| and two lines.        |
+-----------------------+
""",
"""\
<document>
    <table>
        <tgroup cols="1">
            <colspec colwidth="23"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A table with one cell
                            and two lines.
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+-----------------------+
| A malformed table. |
+-----------------------+
""",
"""\
<document>
    <system_warning level="2">
        <paragraph>
            Malformed table at line 1; formatting as a literal block.
        </paragraph>
    </system_warning>
    <literal_block>
        +-----------------------+
        | A malformed table. |
        +-----------------------+
    </literal_block>
</document>
"""],
["""\
+------------------------+
| A well-formed | table. |
+------------------------+

+------------------------+
| This +----------+ too! |
+------------------------+
""",
"""\
<document>
    <table>
        <tgroup cols="1">
            <colspec colwidth="24"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A well-formed | table.
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
    <table>
        <tgroup cols="1">
            <colspec colwidth="24"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            This +----------+ too!
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+--------------+--------------+
| A table with | two columns. |
+--------------+--------------+
""",
"""\
<document>
    <table>
        <tgroup cols="2">
            <colspec colwidth="14"/>
            <colspec colwidth="14"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A table with
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            two columns.
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+--------------+
| A table with |
+--------------+
| two rows.    |
+--------------+
""",
"""\
<document>
    <table>
        <tgroup cols="1">
            <colspec colwidth="14"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A table with
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            two rows.
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+--------------+-------------+
| A table with | two columns |
+--------------+-------------+
| and          | two rows.   |
+--------------+-------------+
""",
"""\
<document>
    <table>
        <tgroup cols="2">
            <colspec colwidth="14"/>
            <colspec colwidth="13"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A table with
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            two columns
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            and
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            two rows.
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+--------------+---------------+
| A table with | two columns,  |
+--------------+---------------+
| two rows, and a column span. |
+------------------------------+
""",
"""\
<document>
    <table>
        <tgroup cols="2">
            <colspec colwidth="14"/>
            <colspec colwidth="15"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A table with
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            two columns,
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry morecols="1">
                        <paragraph>
                            two rows, and a column span.
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+--------------------------+
| A table with three rows, |
+------------+-------------+
| and two    | columns.    |
+------------+-------------+
| First and last rows      |
| contains column spans.   |
+--------------------------+
""",
"""\
<document>
    <table>
        <tgroup cols="2">
            <colspec colwidth="12"/>
            <colspec colwidth="13"/>
            <tbody>
                <row>
                    <entry morecols="1">
                        <paragraph>
                            A table with three rows,
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            and two
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            columns.
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry morecols="1">
                        <paragraph>
                            First and last rows
                            contains column spans.
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+--------------+--------------+
| A table with | two columns, |
+--------------+ and a row    |
| two rows,    | span.        |
+--------------+--------------+
""",
"""\
<document>
    <table>
        <tgroup cols="2">
            <colspec colwidth="14"/>
            <colspec colwidth="14"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A table with
                        </paragraph>
                    </entry>
                    <entry morerows="1">
                        <paragraph>
                            two columns,
                            and a row
                            span.
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            two rows,
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+------------+-------------+---------------+
| A table    | two rows in | and row spans |
| with three +-------------+ to left and   |
| columns,   | the middle, | right.        |
+------------+-------------+---------------+
""",
"""\
<document>
    <table>
        <tgroup cols="3">
            <colspec colwidth="12"/>
            <colspec colwidth="13"/>
            <colspec colwidth="15"/>
            <tbody>
                <row>
                    <entry morerows="1">
                        <paragraph>
                            A table
                            with three
                            columns,
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            two rows in
                        </paragraph>
                    </entry>
                    <entry morerows="1">
                        <paragraph>
                            and row spans
                            to left and
                            right.
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            the middle,
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
Complex spanning pattern (no edge knows all rows/cols):

+-----------+-------------------------+
| W/NW cell | N/NE cell               |
|           +-------------+-----------+
|           | Middle cell | E/SE cell |
+-----------+-------------+           |
| S/SE cell               |           |
+-------------------------+-----------+
""",
"""\
<document>
    <paragraph>
        Complex spanning pattern (no edge knows all rows/cols):
    </paragraph>
    <table>
        <tgroup cols="3">
            <colspec colwidth="11"/>
            <colspec colwidth="13"/>
            <colspec colwidth="11"/>
            <tbody>
                <row>
                    <entry morerows="1">
                        <paragraph>
                            W/NW cell
                        </paragraph>
                    </entry>
                    <entry morecols="1">
                        <paragraph>
                            N/NE cell
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            Middle cell
                        </paragraph>
                    </entry>
                    <entry morerows="1">
                        <paragraph>
                            E/SE cell
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry morecols="1">
                        <paragraph>
                            S/SE cell
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+------------------------+------------+----------+----------+
| Header row, column 1   | Header 2   | Header 3 | Header 4 |
+========================+============+==========+==========+
| body row 1, column 1   | column 2   | column 3 | column 4 |
+------------------------+------------+----------+----------+
| body row 2             | Cells may span columns.          |
+------------------------+------------+---------------------+
| body row 3             | Cells may  | - Table cells       |
+------------------------+ span rows. | - contain           |
| body row 4             |            | - body elements.    |
+------------------------+------------+---------------------+
""",
"""\
<document>
    <table>
        <tgroup cols="4">
            <colspec colwidth="24"/>
            <colspec colwidth="12"/>
            <colspec colwidth="10"/>
            <colspec colwidth="10"/>
            <thead>
                <row>
                    <entry>
                        <paragraph>
                            Header row, column 1
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            Header 2
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            Header 3
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            Header 4
                        </paragraph>
                    </entry>
                </row>
            </thead>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            body row 1, column 1
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            column 2
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            column 3
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            column 4
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            body row 2
                        </paragraph>
                    </entry>
                    <entry morecols="2">
                        <paragraph>
                            Cells may span columns.
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            body row 3
                        </paragraph>
                    </entry>
                    <entry morerows="1">
                        <paragraph>
                            Cells may
                            span rows.
                        </paragraph>
                    </entry>
                    <entry morecols="1" morerows="1">
                        <bullet_list bullet="-">
                            <list_item>
                                <paragraph>
                                    Table cells
                                </paragraph>
                            </list_item>
                            <list_item>
                                <paragraph>
                                    contain
                                </paragraph>
                            </list_item>
                            <list_item>
                                <paragraph>
                                    body elements.
                                </paragraph>
                            </list_item>
                        </bullet_list>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            body row 4
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
["""\
+-----------------+--------+
| A simple table  | cell 2 |
+-----------------+--------+
| cell 3          | cell 4 |
+-----------------+--------+
No blank line after table.
""",
"""\
<document>
    <table>
        <tgroup cols="2">
            <colspec colwidth="17"/>
            <colspec colwidth="8"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A simple table
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            cell 2
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            cell 3
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            cell 4
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
    <system_warning level="1">
        <paragraph>
            Blank line required after table at line 6.
        </paragraph>
    </system_warning>
    <paragraph>
        No blank line after table.
    </paragraph>
</document>
"""],
["""\
+-----------------+--------+
| A simple table  | cell 2 |
+-----------------+--------+
| cell 3          | cell 4 |
+-----------------+--------+
    Unexpected indent and no blank line after table.
""",
"""\
<document>
    <table>
        <tgroup cols="2">
            <colspec colwidth="17"/>
            <colspec colwidth="8"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            A simple table
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            cell 2
                        </paragraph>
                    </entry>
                </row>
                <row>
                    <entry>
                        <paragraph>
                            cell 3
                        </paragraph>
                    </entry>
                    <entry>
                        <paragraph>
                            cell 4
                        </paragraph>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
    <system_warning level="2">
        <paragraph>
            Unexpected indentation at line 6.
        </paragraph>
    </system_warning>
    <system_warning level="1">
        <paragraph>
            Blank line required after table at line 6.
        </paragraph>
    </system_warning>
    <block_quote>
        <paragraph>
            Unexpected indent and no blank line after table.
        </paragraph>
    </block_quote>
</document>
"""],
["""\
+--------------+-------------+
| A bad table. |             |
+--------------+             |
| Cells must be rectangles.  |
+----------------------------+
""",
"""\
<document>
    <system_warning level="2">
        <paragraph>
            Malformed table at line 1; formatting as a literal block.
            Malformed table; parse incomplete.
        </paragraph>
    </system_warning>
    <literal_block>
        +--------------+-------------+
        | A bad table. |             |
        +--------------+             |
        | Cells must be rectangles.  |
        +----------------------------+
    </literal_block>
</document>
"""],
["""\
+------------------------------+
| This table contains another. |
|                              |
| +-------------------------+  |
| | A table within a table. |  |
| +-------------------------+  |
+------------------------------+
""",
"""\
<document>
    <table>
        <tgroup cols="1">
            <colspec colwidth="30"/>
            <tbody>
                <row>
                    <entry>
                        <paragraph>
                            This table contains another.
                        </paragraph>
                        <table>
                            <tgroup cols="1">
                                <colspec colwidth="25"/>
                                <tbody>
                                    <row>
                                        <entry>
                                            <paragraph>
                                                A table within a table.
                                            </paragraph>
                                        </entry>
                                    </row>
                                </tbody>
                            </tgroup>
                        </table>
                    </entry>
                </row>
            </tbody>
        </tgroup>
    </table>
</document>
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
