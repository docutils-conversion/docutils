#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2002/02/06 03:11:35 $
:Copyright: This module has been placed in the public domain.

Test module for utils.py.
"""

import unittest, StringIO, sys
from DPSTestSupport import utils
try:
    import mypdb as pdb
except:
    import pdb
pdb.tracenow = 0


class ReporterTests(unittest.TestCase):

    stream = StringIO.StringIO()
    reporter = utils.Reporter(2, 4, stream, 1)

    def setUp(self):
        self.stream.seek(0)
        self.stream.truncate()

    def test_level0(self):
        sw = self.reporter.system_warning(0, 'debug output')
        self.assertEquals(sw.pformat(), """\
<system_warning level="0" type="DEBUG">
    <paragraph>
        debug output
""")
        self.assertEquals(self.stream.getvalue(),
                          'Reporter: DEBUG [level 0] debug output\n')

    def test_level1(self):
        sw = self.reporter.system_warning(1, 'a little reminder')
        self.assertEquals(sw.pformat(), """\
<system_warning level="1" type="INFO">
    <paragraph>
        a little reminder
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_level2(self):
        sw = self.reporter.system_warning(2, 'a warning')
        self.assertEquals(sw.pformat(), """\
<system_warning level="2" type="WARNING">
    <paragraph>
        a warning
""")
        self.assertEquals(self.stream.getvalue(),
                          'Reporter: WARNING [level 2] a warning\n')

    def test_level3(self):
        sw = self.reporter.system_warning(3, 'an error')
        self.assertEquals(sw.pformat(), """\
<system_warning level="3" type="ERROR">
    <paragraph>
        an error
""")
        self.assertEquals(self.stream.getvalue(),
                          'Reporter: ERROR [level 3] an error\n')

    def test_level4(self):
        self.assertRaises(utils.SystemWarning, self.reporter.system_warning, 4,
                          'a severe error, raises an exception')
        self.assertEquals(self.stream.getvalue(), 'Reporter: SEVERE [level 4] '
                          'a severe error, raises an exception\n')


class QuietReporterTests(unittest.TestCase):

    stream = StringIO.StringIO()
    reporter = utils.Reporter(5, 5, stream, 0)

    def setUp(self):
        self.stream.seek(0)
        self.stream.truncate()

    def test_debug(self):
        sw = self.reporter.debug('a debug message')
        self.assertEquals(sw.pformat(), """\
<system_warning level="0" type="DEBUG">
    <paragraph>
        a debug message
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_info(self):
        sw = self.reporter.info('an informational message')
        self.assertEquals(sw.pformat(), """\
<system_warning level="1" type="INFO">
    <paragraph>
        an informational message
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_warning(self):
        sw = self.reporter.warning('a warning')
        self.assertEquals(sw.pformat(), """\
<system_warning level="2" type="WARNING">
    <paragraph>
        a warning
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_error(self):
        sw = self.reporter.error('an error')
        self.assertEquals(sw.pformat(), """\
<system_warning level="3" type="ERROR">
    <paragraph>
        an error
""")
        self.assertEquals(self.stream.getvalue(), '')

    def test_severe(self):
        sw = self.reporter.severe('a severe error')
        self.assertEquals(sw.pformat(), """\
<system_warning level="4" type="SEVERE">
    <paragraph>
        a severe error
""")
        self.assertEquals(self.stream.getvalue(), '')


class ReporterCategoryTests(unittest.TestCase):

    stream = StringIO.StringIO()

    def setUp(self):
        self.stream.seek(0)
        self.stream.truncate()
        self.reporter = utils.Reporter(2, 4, self.stream, 1)
        self.reporter.setcategory('lemon', 1, 3, self.stream, 0)

    def test_getset(self):
        self.reporter.setcategory('test', 5, 5, None, 0)
        self.assertEquals(self.reporter.getcategory('other'),
                          (1, 2, 4, self.stream))
        self.assertEquals(self.reporter.getcategory('test'),
                          (0, 5, 5, sys.stderr))
        self.assertEquals(self.reporter.getcategory('test.dummy'),
                          (0, 5, 5, sys.stderr))
        self.reporter.setcategory('test.dummy.spam', 1, 2, self.stream, 1)
        self.assertEquals(self.reporter.getcategory('test.dummy.spam'),
                          (1, 1, 2, self.stream))
        self.assertEquals(self.reporter.getcategory('test.dummy'),
                          (0, 5, 5, sys.stderr))
        self.assertEquals(self.reporter.getcategory('test.dummy.spam.eggs'),
                          (1, 1, 2, self.stream))
        self.reporter.unsetcategory('test.dummy.spam')
        self.assertEquals(self.reporter.getcategory('test.dummy.spam.eggs'),
                          (0, 5, 5, sys.stderr))

    def test_debug(self):
        sw = self.reporter.debug('debug output', category='lemon.curry')
        self.assertEquals(self.stream.getvalue(), '')
        sw = self.reporter.debug('debug output')
        self.assertEquals(self.stream.getvalue(),
                          'Reporter: DEBUG [level 0] debug output\n')

    def test_info(self):
        sw = self.reporter.info('some info')
        self.assertEquals(self.stream.getvalue(), '')
        sw = self.reporter.info('some info', category='lemon.curry')
        self.assertEquals(
              self.stream.getvalue(),
              'Reporter "lemon.curry": INFO [level 1] some info\n')

    def test_warning(self):
        sw = self.reporter.warning('a warning')
        self.assertEquals(self.stream.getvalue(),
                          'Reporter: WARNING [level 2] a warning\n')
        sw = self.reporter.warning('a warning', category='lemon.curry')
        self.assertEquals(self.stream.getvalue(), """\
Reporter: WARNING [level 2] a warning
Reporter "lemon.curry": WARNING [level 2] a warning
""")

    def test_error(self):
        sw = self.reporter.error('an error')
        self.assertEquals(self.stream.getvalue(),
                          'Reporter: ERROR [level 3] an error\n')
        self.assertRaises(utils.SystemWarning, self.reporter.error,
                          'an error', category='lemon.curry')
        self.assertEquals(self.stream.getvalue(), """\
Reporter: ERROR [level 3] an error
Reporter "lemon.curry": ERROR [level 3] an error
""")

    def test_severe(self):
        self.assertRaises(utils.SystemWarning, self.reporter.severe,
                          'a severe error')
        self.assertEquals(self.stream.getvalue(),
                          'Reporter: SEVERE [level 4] a severe error\n')
        self.assertRaises(utils.SystemWarning, self.reporter.severe,
                          'a severe error', category='lemon.curry')
        self.assertEquals(self.stream.getvalue(), """\
Reporter: SEVERE [level 4] a severe error
Reporter "lemon.curry": SEVERE [level 4] a severe error
""")


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
