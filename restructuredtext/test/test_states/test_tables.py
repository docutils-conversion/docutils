#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/01 17:01:59 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite(id=__file__)
    s.generateTests(totest)
    return s

totest = {}

totest['tables'] = [
["""\
+-------------------------------------+
| A table with one cell and one line. |
+-------------------------------------+

XXX Temporarily parsing tables as literal blocks.
""",
"""\
<document>
    <literal_block>
        +-------------------------------------+
        | A table with one cell and one line. |
        +-------------------------------------+
    </literal_block>
    <paragraph>
        XXX Temporarily parsing tables as literal blocks.
    </paragraph>
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
    <literal_block>
        +-----------------------+
        | A table with one cell |
        | and two lines.        |
        +-----------------------+
    </literal_block>
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
    <literal_block>
        +------------------------+
        | A well-formed | table. |
        +------------------------+
    </literal_block>
    <literal_block>
        +------------------------+
        | This +----------+ too! |
        +------------------------+
    </literal_block>
</document>
"""],
["""\
+--------------+--------------+
| A table with | two columns. |
+--------------+--------------+
""",
"""\
<document>
    <literal_block>
        +--------------+--------------+
        | A table with | two columns. |
        +--------------+--------------+
    </literal_block>
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
    <literal_block>
        +--------------+
        | A table with |
        +--------------+
        | two rows.    |
        +--------------+
    </literal_block>
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
    <literal_block>
        +--------------+-------------+
        | A table with | two columns |
        +--------------+-------------+
        | and          | two rows.   |
        +--------------+-------------+
    </literal_block>
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
    <literal_block>
        +--------------+---------------+
        | A table with | two columns,  |
        +--------------+---------------+
        | two rows, and a column span. |
        +------------------------------+
    </literal_block>
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
    <literal_block>
        +--------------------------+
        | A table with three rows, |
        +------------+-------------+
        | and two    | columns.    |
        +------------+-------------+
        | First and last rows      |
        | contains column spans.   |
        +--------------------------+
    </literal_block>
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
    <literal_block>
        +--------------+--------------+
        | A table with | two columns, |
        +--------------+ and a row    |
        | two rows,    | span.        |
        +--------------+--------------+
    </literal_block>
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
    <literal_block>
        +------------+-------------+---------------+
        | A table    | two rows in | and row spans |
        | with three +-------------+ to left and   |
        | columns,   | the middle, | right.        |
        +------------+-------------+---------------+
    </literal_block>
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
    <literal_block>
        +-----------+-------------------------+
        | W/NW cell | N/NE cell               |
        |           +-------------+-----------+
        |           | Middle cell | E/SE cell |
        +-----------+-------------+           |
        | S/SE cell               |           |
        +-------------------------+-----------+
    </literal_block>
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
    <literal_block>
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
    </literal_block>
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
    <literal_block>
        +-----------------+--------+
        | A simple table  | cell 2 |
        +-----------------+--------+
        | cell 3          | cell 4 |
        +-----------------+--------+
    </literal_block>
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
    <literal_block>
        +-----------------+--------+
        | A simple table  | cell 2 |
        +-----------------+--------+
        | cell 3          | cell 4 |
        +-----------------+--------+
    </literal_block>
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
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
