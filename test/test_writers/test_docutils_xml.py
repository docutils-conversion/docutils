#!/usr/bin/env python

# Author: Felix Wiemann
# Contact: Felix_Wiemann@ososo.de
# Revision: $Revision$
# Date: $Date$
# Copyright: This module has been placed in the public domain.

"""
Test for docutils XML writer.
"""

import unittest

import docutils
import docutils.core
from __init__ import DocutilsTestSupport


class DocutilsXMLTestCase(unittest.TestCase):

    input = 'Test\n====\n\nSubsection\n----------\n\nTest\n\n----------\n\nTest.'
    xmldecl = '<?xml version="1.0" encoding="iso-8859-1"?>\n'
    doctypedecl = '<!DOCTYPE document PUBLIC "+//IDN docutils.sourceforge.net//DTD Docutils Generic//EN//XML" "http://docutils.sourceforge.net/spec/docutils.dtd">\n'
    generatedby = '<!-- Generated by Docutils %s -->\n' % docutils.__version__
    bodynormal = '<document id="test" name="test" source="&lt;string&gt;"><title>Test</title><subtitle id="subsection" name="subsection">Subsection</subtitle><paragraph>Test</paragraph><transition/><paragraph>Test.</paragraph></document>'
    bodynormal = '<document id="test" name="test" source="&lt;string&gt;"><title>Test</title><subtitle id="subsection" name="subsection">Subsection</subtitle><paragraph>Test</paragraph><transition/><paragraph>Test.</paragraph></document>'
    bodynewlines = '<document id="test" name="test" source="&lt;string&gt;">\n<title>\nTest\n</title>\n<subtitle id="subsection" name="subsection">\nSubsection\n</subtitle>\n<paragraph>\nTest\n</paragraph>\n<transition/>\n<paragraph>\nTest.\n</paragraph>\n</document>\n'
    bodyindents = '<document id="test" name="test" source="&lt;string&gt;">\n    <title>\n        Test\n    </title>\n    <subtitle id="subsection" name="subsection">\n        Subsection\n    </subtitle>\n    <paragraph>\n        Test\n    </paragraph>\n    <transition/>\n    <paragraph>\n        Test.\n    </paragraph>\n</document>\n'

    def test_publish(self):
        settings = {'output_encoding': 'iso-8859-1', '_disable_config': 1}
        for settings['newlines'] in 0, 1:
            for settings['indents'] in 0, 1:
                for settings['xml_declaration'] in 0, 1:
                    for settings['doctype_declaration'] in 0, 1:

                        expected = ''
                        if settings['xml_declaration']:
                            expected += self.xmldecl
                        if settings['doctype_declaration']:
                            expected += self.doctypedecl
                        expected += self.generatedby
                        if settings['indents']:
                            expected += self.bodyindents
                        elif settings['newlines']:
                            expected += self.bodynewlines
                        else:
                            expected += self.bodynormal

                        s = docutils.SettingsSpec()
                        s.settings_default_overrides = settings
                        self.assertEqual(docutils.core.publish_string
                                         (source=self.input,
                                          reader_name='standalone',
                                          writer_name='docutils_xml',
                                          settings_spec=s),
                                         expected)


if __name__ == '__main__':
    unittest.main()
