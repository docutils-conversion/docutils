#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/17 04:11:02 $
:Copyright: This module has been placed in the public domain.

Test module for utils.py.
"""

import unittest, StringIO
from DPSTestSupport import utils
try:
    import mypdb as pdb
except:
    import pdb
pdb.tracenow = 0


class ReporterTests(unittest.TestCase):

    stream = StringIO.StringIO()
    reporter = utils.Reporter(1, 3, stream)

    def setUp(self):
        self.stream.seek(0)
        self.stream.truncate()

    def test_level0(self):
        sw = self.reporter.system_warning(0, 'a little reminder')
        self.assertEquals(sw.pformat(), """\
<system_warning level="0">
    <paragraph>
        a little reminder
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_level1(self):
        sw = self.reporter.system_warning(1, 'a warning')
        self.assertEquals(sw.pformat(), """\
<system_warning level="1">
    <paragraph>
        a warning
""")
        self.assertEquals(self.stream.getvalue(),
                          'Warning: [level 1] a warning\n')

    def test_level2(self):
        sw = self.reporter.system_warning(2, 'an error')
        self.assertEquals(sw.pformat(), """\
<system_warning level="2">
    <paragraph>
        an error
""")
        self.assertEquals(self.stream.getvalue(),
                          'Warning: [level 2] an error\n')

    def test_level3(self):
        self.assertRaises(utils.SystemWarning, self.reporter.system_warning, 3,
                          'a severe error, raises an exception')
        self.assertEquals(self.stream.getvalue(), '')


class QuietReporterTests(unittest.TestCase):

    stream = StringIO.StringIO()
    reporter = utils.Reporter(4, 4, stream)

    def setUp(self):
        self.stream.seek(0)
        self.stream.truncate()

    def test_information(self):
        sw = self.reporter.information('an informational message')
        self.assertEquals(sw.pformat(), """\
<system_warning level="0">
    <paragraph>
        an informational message
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_warning(self):
        sw = self.reporter.warning('a warning')
        self.assertEquals(sw.pformat(), """\
<system_warning level="1">
    <paragraph>
        a warning
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_error(self):
        sw = self.reporter.error('an error')
        self.assertEquals(sw.pformat(), """\
<system_warning level="2">
    <paragraph>
        an error
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_severe(self):
        sw = self.reporter.severe('a severe error')
        self.assertEquals(sw.pformat(), """\
<system_warning level="3">
    <paragraph>
        a severe error
""")
        self.assertEquals(self.stream.getvalue(), '')


if __name__ == '__main__':
    unittest.main()
