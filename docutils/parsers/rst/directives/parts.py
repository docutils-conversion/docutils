# Author: David Goodger, Dmitry Jemerov
# Contact: goodger@users.sourceforge.net
# Revision: $Revision$
# Date: $Date$
# Copyright: This module has been placed in the public domain.

"""
Directives for document parts.
"""

__docformat__ = 'reStructuredText'

from docutils import nodes, languages
from docutils.transforms import parts
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives


class Contents(Directive):

    """
    Table of contents.

    The table of contents is generated in two passes: initial parse and
    transform.  During the initial parse, a 'pending' element is generated
    which acts as a placeholder, storing the TOC title and any options
    internally.  At a later stage in the processing, the 'pending' element is
    replaced by a 'topic' element, a title and the table of contents proper.
    """

    backlinks_values = ('top', 'entry', 'none')

    def backlinks(arg):
        value = directives.choice(arg, Contents.backlinks_values)
        if value == 'none':
            return None
        else:
            return value

    required_arguments = 0
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'depth': directives.nonnegative_int,
                   'local': directives.flag,
                   'backlinks': backlinks,
                   'class': directives.class_option}
    
    def run(self):
        if not (self.state_machine.match_titles
                or isinstance(self.state_machine.node, nodes.sidebar)):
            error = self.state_machine.reporter.error(
                'The "%s" directive may not be used within topics or body '
                'elements.' % self.name, nodes.literal_block(
                self.block_text, self.block_text), line=self.lineno)
            return [error]
        document = self.state_machine.document
        language = languages.get_language(document.settings.language_code)
        if self.arguments:
            title_text = self.arguments[0]
            text_nodes, messages = self.state.inline_text(title_text,
                                                          self.lineno)
            title = nodes.title(title_text, '', *text_nodes)
        else:
            messages = []
            if self.options.has_key('local'):
                title = None
            else:
                title = nodes.title('', language.labels['contents'])
        topic = nodes.topic(classes=['contents'])
        topic['classes'] += self.options.get('class', [])
        if self.options.has_key('local'):
            topic['classes'].append('local')
        if title:
            name = title.astext()
            topic += title
        else:
            name = language.labels['contents']
        name = nodes.fully_normalize_name(name)
        if not document.has_name(name):
            topic['names'].append(name)
        document.note_implicit_target(topic)
        pending = nodes.pending(parts.Contents, rawsource=self.block_text)
        pending.details.update(self.options)
        document.note_pending(pending)
        topic += pending
        return [topic] + messages


class Sectnum(Directive):

    """Automatic section numbering."""

    option_spec = {'depth': int,
                   'start': int,
                   'prefix': directives.unchanged_required,
                   'suffix': directives.unchanged_required}

    def run(self):
        pending = nodes.pending(parts.SectNum)
        pending.details.update(self.options)
        self.state_machine.document.note_pending(pending)
        return [pending]


def header_footer(node, name, arguments, options, content, lineno,
                  content_offset, block_text, state, state_machine):
    """Contents of document header or footer."""
    if not content:
        warning = state_machine.reporter.warning(
            'Content block expected for the "%s" directive; none found.'
            % name, nodes.literal_block(block_text, block_text),
            line=lineno)
        node.append(nodes.paragraph(
            '', 'Problem with the "%s" directive: no content supplied.' % name))
        return [warning]
    text = '\n'.join(content)
    state.nested_parse(content, content_offset, node)
    return []

def header(name, arguments, options, content, lineno,
           content_offset, block_text, state, state_machine):
    decoration = state_machine.document.get_decoration()
    node = decoration.get_header()
    return header_footer(node, name, arguments, options, content, lineno,
                         content_offset, block_text, state, state_machine)

header.content = 1

def footer(name, arguments, options, content, lineno,
           content_offset, block_text, state, state_machine):
    decoration = state_machine.document.get_decoration()
    node = decoration.get_footer()
    return header_footer(node, name, arguments, options, content, lineno,
                         content_offset, block_text, state, state_machine)

footer.content = 1
