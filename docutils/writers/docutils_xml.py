# $Id$
# Author: David Goodger, Paul Tremblay, Guenter Milde
# Maintainer: docutils-develop@lists.sourceforge.net
# Copyright: This module has been placed in the public domain.

"""
Simple document tree Writer, writes Docutils XML according to
https://docutils.sourceforge.io/docs/ref/docutils.dtd.
"""

__docformat__ = 'reStructuredText'

from io import StringIO
import xml.sax.saxutils

import docutils
from docutils import frontend, writers, nodes


class RawXmlError(docutils.ApplicationError): pass


class Writer(writers.Writer):

    supported = ('xml',)
    """Formats this writer supports."""

    settings_spec = (
        '"Docutils XML" Writer Options',
        None,
        (('Generate XML with newlines before and after tags.',
          ['--newlines'],
          {'action': 'store_true', 'validator': frontend.validate_boolean}),
         ('Generate XML with indents and newlines.',
          ['--indents'],  # TODO use integer value for number of spaces?
          {'action': 'store_true', 'validator': frontend.validate_boolean}),
         ('Omit the XML declaration.  Use with caution.',
          ['--no-xml-declaration'],
          {'dest': 'xml_declaration', 'default': 1, 'action': 'store_false',
           'validator': frontend.validate_boolean}),
         ('Omit the DOCTYPE declaration.',
          ['--no-doctype'],
          {'dest': 'doctype_declaration', 'default': 1,
           'action': 'store_false', 'validator': frontend.validate_boolean}),))

    settings_defaults = {'output_encoding_error_handler': 'xmlcharrefreplace'}

    config_section = 'docutils_xml writer'
    config_section_dependencies = ('writers',)

    output = None
    """Final translated form of `document`."""

    def __init__(self):
        writers.Writer.__init__(self)
        self.translator_class = XMLTranslator

    def translate(self):
        self.visitor = visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.output = ''.join(visitor.output)


class XMLTranslator(nodes.GenericNodeVisitor):

    xml_declaration = '<?xml version="1.0" encoding="%s"?>\n'
    # TODO: add stylesheet options similar to HTML and LaTeX writers?
    # xml_stylesheet = '<?xml-stylesheet type="text/xsl" href="%s"?>\n'
    doctype = (
        '<!DOCTYPE document PUBLIC'
        ' "+//IDN docutils.sourceforge.net//DTD Docutils Generic//EN//XML"'
        ' "http://docutils.sourceforge.net/docs/ref/docutils.dtd">\n')
    generator = '<!-- Generated by Docutils %s -->\n'

    xmlparser = xml.sax.make_parser()
    """SAX parser instance to check/extract raw XML."""
    xmlparser.setFeature(
        "http://xml.org/sax/features/external-general-entities", True)

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)

        # Reporter
        self.warn = self.document.reporter.warning
        self.error = self.document.reporter.error

        # Settings
        self.settings = settings = document.settings
        self.indent = self.newline = ''
        if settings.newlines:
            self.newline = '\n'
        if settings.indents:
            self.newline = '\n'
            self.indent = '    '  # TODO make this configurable?
        self.level = 0       # indentation level
        self.in_simple = 0   # level of nesting inside mixed-content elements
        self.fixed_text = 0  # level of nesting inside FixedText elements

        # Output
        self.output = []
        if settings.xml_declaration:
            self.output.append(
                self.xml_declaration % settings.output_encoding)
        if settings.doctype_declaration:
            self.output.append(self.doctype)
        self.output.append(self.generator % docutils.__version__)

        # initialize XML parser
        self.the_handle = TestXml()
        self.xmlparser.setContentHandler(self.the_handle)

    # generic visit and depart methods
    # --------------------------------

    simple_nodes = (nodes.TextElement,
                    nodes.image, nodes.colspec, nodes.transition)

    def default_visit(self, node):
        """Default node visit method."""
        if not self.in_simple:
            self.output.append(self.indent*self.level)
        self.output.append(node.starttag(xml.sax.saxutils.quoteattr))
        self.level += 1
        # @@ make nodes.literal an instance of FixedTextElement?
        if isinstance(node, (nodes.FixedTextElement, nodes.literal)):
            self.fixed_text += 1
        if isinstance(node, self.simple_nodes):
            self.in_simple += 1
        if not self.in_simple:
            self.output.append(self.newline)

    def default_departure(self, node):
        """Default node depart method."""
        self.level -= 1
        if not self.in_simple:
            self.output.append(self.indent*self.level)
        self.output.append(node.endtag())
        if isinstance(node, (nodes.FixedTextElement, nodes.literal)):
            self.fixed_text -= 1
        if isinstance(node, self.simple_nodes):
            self.in_simple -= 1
        if not self.in_simple:
            self.output.append(self.newline)

    # specific visit and depart methods
    # ---------------------------------

    def visit_Text(self, node):
        text = xml.sax.saxutils.escape(node.astext())
        # indent text if we are not in a FixedText element:
        if not self.fixed_text:
            text = text.replace('\n', '\n'+self.indent*self.level)
        self.output.append(text)

    def depart_Text(self, node):
        pass

    def visit_raw(self, node):
        if 'xml' not in node.get('format', '').split():
            # skip other raw content?
            # raise nodes.SkipNode
            self.default_visit(node)
            return
        # wrap in <raw> element
        self.default_visit(node)      # or not?
        xml_string = node.astext()
        self.output.append(xml_string)
        self.default_departure(node)  # or not?
        # Check validity of raw XML:
        try:
            self.xmlparser.parse(StringIO(xml_string))
        except xml.sax._exceptions.SAXParseException as error:
            col_num = self.the_handle.locator.getColumnNumber()
            line_num = self.the_handle.locator.getLineNumber()
            srcline = node.line
            if not isinstance(node.parent, nodes.TextElement):
                srcline += 2  # directive content start line
            msg = 'Invalid raw XML in column %d, line offset %d:\n%s' % (
                   col_num, line_num, node.astext())
            self.warn(msg, source=node.source, line=srcline+line_num-1)
        raise nodes.SkipNode  # content already processed


class TestXml(xml.sax.handler.ContentHandler):

    def setDocumentLocator(self, locator):
        self.locator = locator
