#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2001/11/15 02:58:43 $
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


class AttributeParserTests(unittest.TestCase):

    def test_extractattributes(self):
        self.assertRaises(utils.BadAttributeLineError,
                          utils.extractattributes, ['hello'])
        self.assertRaises(utils.BadAttributeDataError,
                          utils.extractattributes, ['[hello]'])
        self.assertRaises(utils.BadAttributeDataError,
                          utils.extractattributes, ['[=hello]'])
        self.assertRaises(utils.BadAttributeDataError,
                          utils.extractattributes, ['[hello=]'])
        self.assertRaises(utils.BadAttributeDataError,
                          utils.extractattributes, ['[hello="]'])
        self.assertRaises(utils.BadAttributeDataError,
                          utils.extractattributes, ['[hello="something]'])
        self.assertRaises(utils.BadAttributeDataError,
                          utils.extractattributes,
                          ['[hello="something"else]'])
        output = utils.extractattributes("""\
[att1=val1 att2=val2 att3="value number '3'"]
[att4=val4]""".splitlines())
        self.assertEquals(output, [('att1', 'val1'), ('att2', 'val2'),
                                   ('att3', "value number '3'"),
                                   ('att4', 'val4')])

    attributespec = {'a': int, 'bbb': float, 'cdef': lambda x: x}

    def test_assembleattributes(self):
        input = utils.extractattributes(['[a=1 bbb=2.0 cdef=hol%s]'
                                              % chr(224)])
        self.assertEquals(
              utils.assembleattributes(input, self.attributespec),
              {'a': 1, 'bbb': 2.0, 'cdef': ('hol%s' % chr(224))})
        input = utils.extractattributes(['[a=1 b=2.0 c=hol%s]'
                                              % chr(224)])
        self.assertRaises(KeyError, utils.assembleattributes,
                          input, self.attributespec)
        input = utils.extractattributes(['[a=1 bbb=two cdef=hol%s]'
                                              % chr(224)])
        self.assertRaises(ValueError, utils.assembleattributes,
                          input, self.attributespec)

    def test_parseattributes(self):
        input = ['[a=1 bbb=2.0 cdef=hol%s]' % chr(224)]
        self.assertEquals(
              utils.parseattributes(input, self.attributespec),
              {'a': 1, 'bbb': 2.0, 'cdef': ('hol%s' % chr(224))})


if __name__ == '__main__':
    unittest.main()
