#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/04 04:11:01 $
:Copyright: This module has been placed in the public domain.

Tests for states.py.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.TableParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

totest['tables'] = [
["""\
+-------------------------------------+
| A table with one cell and one line. |
+-------------------------------------+
""",
[(0, 0, 2, 38, ['A table with one cell and one line.'])],
()],
["""\
+--------------+--------------+
| A table with | two columns. |
+--------------+--------------+
""",
[(0, 0, 2, 15, ['A table with']),
 (0, 15, 2, 30, ['two columns.'])],
()],
["""\
+--------------+-------------+
| A table with | two columns |
+--------------+-------------+
| and          | two rows.   |
+--------------+-------------+
""",
[(0, 0, 2, 15, ['A table with']),
 (0, 15, 2, 29, ['two columns']),
 (2, 0, 4, 15, ['and']),
 (2, 15, 4, 29, ['two rows.'])],
()],
["""\
+--------------------------+
| A table with three rows, |
+------------+-------------+
| and two    | columns.    |
+------------+-------------+
| First and last rows      |
| contain column spans.    |
+--------------------------+
""",
[(0, 0, 2, 27, ['A table with three rows,']),
 (2, 0, 4, 13, ['and two']),
 (2, 13, 4, 27, ['columns.']),
 (4, 0, 7, 27, ['First and last rows', 'contain column spans.'])],
()],
["""\
+------------+-------------+---------------+
| A table    | two rows in | and row spans |
| with three +-------------+ to left and   |
| columns,   | the middle, | right.        |
+------------+-------------+---------------+
""",
[(0, 0, 4, 13, ['A table', 'with three', 'columns,']),
 (0, 13, 2, 27, ['two rows in']),
 (0, 27, 4, 43, ['and row spans', 'to left and', 'right.']),
 (2, 13, 4, 27, ['the middle,'])],
()],
["""\
+------------+-------------+---------------+
| A table |  | two rows in | and funny     |
| with 3  +--+-------------+-+ stuff.      |
| columns,   | the middle, | |             |
+------------+-------------+---------------+
""",
[(0, 0, 4, 13, ['A table |', 'with 3  +--', 'columns,']),
 (0, 13, 2, 27, ['two rows in']),
 (0, 27, 4, 43, [' and funny', '-+ stuff.', ' |']),
 (2, 13, 4, 27, ['the middle,'])],
()],
["""\
+-----------+-------------------------+
| W/NW cell | N/NE cell               |
|           +-------------+-----------+
|           | Middle cell | E/SE cell |
+-----------+-------------+           |
| S/SE cell               |           |
+-------------------------+-----------+
""",
[(0, 0, 4, 12, ['W/NW cell', '', '']),
 (0, 12, 2, 38, ['N/NE cell']),
 (2, 12, 4, 26, ['Middle cell']),
 (2, 26, 6, 38, ['E/SE cell', '', '']),
 (4, 0, 6, 26, ['S/SE cell'])],
()],
["""\
+--------------+-------------+
| A bad table. |             |
+--------------+             |
| Cells must be rectangles.  |
+----------------------------+
""",
'MarkupError: Malformed table; parse incomplete.',
()],
["""\
+-------------------------------+
| A table with two header rows, |
+------------+------------------+
| the first  | with a span.     |
+============+==================+
| Two body   | rows,            |
+------------+------------------+
| the second with a span.       |
+-------------------------------+
""",
[(0, 0, 2, 32, ['A table with two header rows,']),
 (2, 0, 4, 13, ['the first']),
 (2, 13, 4, 32, ['with a span.']),
 (4, 0, 6, 13, ['Two body']),
 (4, 13, 6, 32, ['rows,']),
 (6, 0, 8, 32, ['the second with a span.'])],
()],
["""\
+-------------------------------+
| A table with two head/body    |
+=============+=================+
| row         | separators.     |
+=============+=================+
| That's bad. |                 |
+-------------+-----------------+
""",
'MarkupError: Multiple head/body row separators in table '
'(at line offset 2 and 4); only one allowed.',
()],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
