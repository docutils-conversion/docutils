#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/02/21 03:41:31 $
:Copyright: This module has been placed in the public domain.

Simple HyperText Markup Language document tree Writer.

The output uses the HTML 4.01 strict.dtd and contains a minimum of formatting
information. A cascading style sheet "default.css" is required for proper
viewing with a browser.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Writer']


from dps import writers, nodes, languages


class Writer(writers.Writer):

    output = None
    """Final translated form of `document`."""

    def translate(self):
        visitor = HTMLTranslator(self.document)
        self.document.walkabout(visitor)
        self.output = visitor.astext()

    def record(self):
        self.recordfile(self.output, self.destination)


class HTMLTranslator(nodes.NodeVisitor):

    def __init__(self, doctree):
        nodes.NodeVisitor.__init__(self, doctree)
        self.language = languages.getlanguage(doctree.languagecode)
        self.head = ['<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN"'
                     ' "http://www.w3.org/TR/html4/strict.dtd">\n',
                     '<HTML LANG="%s">\n<HEAD>\n' % doctree.languagecode,
                     '<LINK REL="StyleSheet" HREF="default.css"'
                     ' TYPE="text/css">']
        self.body = ['</HEAD>\n<BODY>\n']
        self.foot = ['</BODY>\n</HTML>\n']
        self.sectionlevel = 0

    def astext(self):
        return ''.join(self.head + self.body + self.foot)

    def encode(self, text):
        """Encode special characters in `text` & return."""
        text = text.replace("&", "&amp;")
        text = text.replace("<", "&lt;")
        text = text.replace('"', "&quot;")
        text = text.replace(">", "&gt;")
        return text

    def starttag(self, node, tagname, suffix='\n', **attrs):
        attlist = attrs.items()
        for att in ('id', 'class'):
            if node.has_key(att):
                attlist.append((att, node[att]))
        attlist.sort()
        return '<%s>%s' % (' '.join([tagname.upper()] +
                                    ['%s="%s"' % (n.upper(), self.encode(v))
                                     for n, v in attlist]),
                           suffix)

    def visit_Text(self, node):
        self.body.append(self.encode(node.astext()))

    def depart_Text(self, node):
        pass

    def visit_abstract(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='abstract'))
        self.body.append('<H3>'
                         + self.language.bibliographic_labels['abstract']
                         + '</H3>\n')

    def depart_abstract(self, node):
        self.body.append('</DIV>\n')

    def visit_attention(self, node):
        pass

    def depart_attention(self, node):
        pass

    def visit_author(self, node):
        self.head.append(self.starttag(node, 'meta', name='author',
                                       content=node.astext()))

    def depart_author(self, node):
        pass

    def visit_authors(self, node):
        pass

    def depart_authors(self, node):
        pass

    def visit_block_quote(self, node):
        pass

    def depart_block_quote(self, node):
        pass

    def visit_bullet_list(self, node):
        self.body.append(self.starttag(node, 'ul',
                                       CLASS='bullet'+node['bullet']))

    def depart_bullet_list(self, node):
        self.body.append('</UL>\n')

    def visit_caption(self, node):
        pass

    def depart_caption(self, node):
        pass

    def visit_caution(self, node):
        pass

    def depart_caution(self, node):
        pass

    def visit_classifier(self, node):
        self.body.append(' <SPAN CLASS="classifier_delimiter">:</SPAN> ')
        self.body.append(self.starttag(node, 'span', '', CLASS='classifier'))

    def depart_classifier(self, node):
        self.body.append('</SPAN>')

    def visit_colspec(self, node):
        pass

    def depart_colspec(self, node):
        pass

    def visit_comment(self, node):
        self.body.append('<!-- ')

    def depart_comment(self, node):
        self.body.append(' -->\n')

    def visit_contact(self, node):
        pass

    def depart_contact(self, node):
        pass

    def visit_copyright(self, node):
        self.head.append(self.starttag(node, 'meta', name='copyright',
                                       content=node.astext()))

    def depart_copyright(self, node):
        pass

    def visit_danger(self, node):
        pass

    def depart_danger(self, node):
        pass

    def visit_date(self, node):
        self.head.append(self.starttag(node, 'meta', name='date',
                                       content=node.astext()))

    def depart_date(self, node):
        pass

    def visit_definition(self, node):
        self.body.append('</TERM>\n')
        self.body.append(self.starttag(node, 'dd'))

    def depart_definition(self, node):
        self.body.append('</DD>\n')

    def visit_definition_list(self, node):
        self.body.append(self.starttag(node, 'dl'))

    def depart_definition_list(self, node):
        self.body.append('</DL>\n')

    def visit_definition_list_item(self, node):
        pass

    def depart_definition_list_item(self, node):
        pass

    def visit_description(self, node):
        pass

    def depart_description(self, node):
        pass

    def visit_docinfo(self, node):
        # @@@ as a table?
        pass

    def depart_docinfo(self, node):
        pass

    def visit_doctest_block(self, node):
        pass

    def depart_doctest_block(self, node):
        pass

    def visit_document(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='document'))

    def depart_document(self, node):
        self.body.append('</DIV>\n')

    def visit_emphasis(self, node):
        self.body.append('<EM>')

    def depart_emphasis(self, node):
        self.body.append('</EM>')

    def visit_entry(self, node):
        pass

    def depart_entry(self, node):
        pass

    def visit_enumerated_list(self, node):
        pass

    def depart_enumerated_list(self, node):
        pass

    def visit_error(self, node):
        pass

    def depart_error(self, node):
        pass

    def visit_field(self, node):
        pass

    def depart_field(self, node):
        pass

    def visit_field_argument(self, node):
        pass

    def depart_field_argument(self, node):
        pass

    def visit_field_body(self, node):
        pass

    def depart_field_body(self, node):
        pass

    def visit_field_list(self, node):
        pass

    def depart_field_list(self, node):
        pass

    def visit_field_name(self, node):
        pass

    def depart_field_name(self, node):
        pass

    def visit_figure(self, node):
        pass

    def depart_figure(self, node):
        pass

    def visit_footnote(self, node):
        pass

    def depart_footnote(self, node):
        pass

    def visit_footnote_reference(self, node):
        pass

    def depart_footnote_reference(self, node):
        pass

    def visit_hint(self, node):
        pass

    def depart_hint(self, node):
        pass

    def visit_image(self, node):
        attrs = node.attributes.copy()
        attrs['src'] = attrs['uri']
        del attrs['uri']
        if not attrs.has_key('alt'):
            attrs['alt'] = attrs['src']
        self.body.append(self.starttag(node, 'img', '', **attrs))

    def depart_image(self, node):
        pass

    def visit_important(self, node):
        pass

    def depart_important(self, node):
        pass

    def visit_interpreted(self, node):
        self.body.append('<SPAN class="interpreted">')

    def depart_interpreted(self, node):
        self.body.append('</SPAN>')

    def visit_label(self, node):
        pass

    def depart_label(self, node):
        pass

    def visit_legend(self, node):
        pass

    def depart_legend(self, node):
        pass

    def visit_list_item(self, node):
        self.body.append(self.starttag(node, 'li'))

    def depart_list_item(self, node):
        self.body.append('</LI>\n')

    def visit_literal(self, node):
        self.body.append('<CODE>')

    def depart_literal(self, node):
        self.body.append('</CODE>')

    def visit_literal_block(self, node):
        pass

    def depart_literal_block(self, node):
        pass

    def visit_long_option(self, node):
        pass

    def depart_long_option(self, node):
        pass

    def visit_meta(self, node):
        self.head.append(self.starttag(node, 'meta', **node.attributes))

    def depart_meta(self, node):
        pass

    def visit_note(self, node):
        pass

    def depart_note(self, node):
        pass

    def visit_option(self, node):
        pass

    def depart_option(self, node):
        pass

    def visit_option_argument(self, node):
        pass

    def depart_option_argument(self, node):
        pass

    def visit_option_list(self, node):
        pass

    def depart_option_list(self, node):
        pass

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        pass

    def visit_organization(self, node):
        pass

    def depart_organization(self, node):
        pass

    def visit_paragraph(self, node):
        self.body.append(self.starttag(node, 'p', ''))

    def depart_paragraph(self, node):
        self.body.append('</P>\n')

    def visit_problematic(self, node):
        self.body.append(self.starttag(node, 'span', '', CLASS='problematic'))

    def depart_problematic(self, node):
        self.body.append('</SPAN>')

    def visit_reference(self, node):
        pass

    def depart_reference(self, node):
        pass

    def visit_revision(self, node):
        pass

    def depart_revision(self, node):
        pass

    def visit_row(self, node):
        pass

    def depart_row(self, node):
        pass

    def visit_section(self, node):
        self.sectionlevel += 1
        self.body.append(self.starttag(node, 'div', CLASS='section'))

    def depart_section(self, node):
        self.sectionlevel -= 1
        self.body.append('</DIV>\n')

    def visit_short_option(self, node):
        pass

    def depart_short_option(self, node):
        pass

    def visit_status(self, node):
        pass

    def depart_status(self, node):
        pass

    def visit_strong(self, node):
        self.body.append('<STRONG>')

    def depart_strong(self, node):
        self.body.append('</STRONG>')

    def visit_substitution_definition(self, node):
        raise nodes.SkipChildren

    def depart_substitution_definition(self, node):
        pass

    def visit_substitution_reference(self, node):
        pass

    def depart_substitution_reference(self, node):
        pass

    def visit_subtitle(self, node):
        self.body.append(self.starttag(node, 'H2', '', CLASS='subtitle'))

    def depart_subtitle(self, node):
        self.body.append('</H1>\n')

    def visit_system_message(self, node):
        pass

    def depart_system_message(self, node):
        pass

    def visit_table(self, node):
        pass

    def depart_table(self, node):
        pass

    def visit_target(self, node):
        pass

    def depart_target(self, node):
        pass

    def visit_tbody(self, node):
        pass

    def depart_tbody(self, node):
        pass

    def visit_term(self, node):
        self.body.append(self.starttag(node, 'dt', ''))

    def depart_term(self, node):
        # leave the end tag to visit_definition, in case there's a classifier
        pass

    def visit_tgroup(self, node):
        pass

    def depart_tgroup(self, node):
        pass

    def visit_thead(self, node):
        pass

    def depart_thead(self, node):
        pass

    def visit_tip(self, node):
        pass

    def depart_tip(self, node):
        pass

    def visit_title(self, node):
        if self.sectionlevel == 0:
            self.head.append('<TITLE>%s</TITLE>\n' % self.encode(node.astext()))
            self.body.append(self.starttag(node, 'H1', '', CLASS='title'))
        else:
            self.body.append(self.starttag(node, 'H%s' % self.sectionlevel, ''))
            # @@@ >H6?

    def depart_title(self, node):
        if self.sectionlevel == 0:
            self.body.append('</H1>\n')
        else:
            self.body.append('</H%s>\n' % self.sectionlevel) # @@@ >H6?

    def visit_transition(self, node):
        self.body.append('<HR>\n')

    def depart_transition(self, node):
        pass

    def visit_version(self, node):
        pass

    def depart_version(self, node):
        pass

    def visit_vms_option(self, node):
        pass

    def depart_vms_option(self, node):
        pass

    def visit_warning(self, node):
        pass

    def depart_warning(self, node):
        pass
