#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/11/06 00:53:40 $
:Copyright: This module has been placed in the public domain.

Directives for figures and simple images.
"""

__docformat__ = 'reStructuredText'

__all__ = ['image', 'figure']


import sys
from restructuredtext import states
from dps import nodes


def image(match, typename, data, state, statemachine):
    lineno = statemachine.abslineno()
    lineoffset = statemachine.lineoffset
    datablock, indent, offset, blankfinish = \
          statemachine.getfirstknownindented(match.end(), uptoblank=1)
    if not datablock:
        error = statemachine.memo.reporter.error(
              'Missing image URI argument at line %s.' % lineno,
              [nodes.literal_block(match.string, match.string)])
        return [error], blankfinish
    blocktext = '\n'.join(statemachine.inputlines[lineoffset:
                                                  lineoffset+len(datablock)])
    tokens = []
    if datablock[-1][0] == '[' and datablock[-1][-1] == ']':
        tokens = datablock.pop()[1:-1].split()
    reference = ''.join([line.strip() for line in datablock])
    if reference.find(' ') != -1:
        warning = statemachine.memo.reporter.warning(
              'Image URI at line %s contains whitespace.' % lineno)
        warning += nodes.literal_block(blocktext, blocktext)
        return [warning], blankfinish
    attributes = {'uri': reference}
    for token in tokens:
        parts = token.split('=')
        if parts[0].lower() not in ('height', 'width', 'scale'):
            error = statemachine.memo.reporter.error(
                  'Unknown image attribute "%s" at line %s.'
                  % (parts[0], lineno),
                  [nodes.literal_block(match.string, match.string)])
            return [error], blankfinish
        if len(parts) != 2:
            error = statemachine.memo.reporter.error(
                  'Invalid image attribute expression at line %s: "%s".'
                  % (lineno, token),
                  [nodes.literal_block(match.string, match.string)])
            return [error], blankfinish
        name = parts[0].lower()
        if attributes.has_key(name):
            error = statemachine.memo.reporter.error(
                  'Duplicate image attribute name at line %s: "%s"'
                  % (lineno, name),
                  [nodes.literal_block(match.string, match.string)])
            return [error], blankfinish
        try:
            value = int(parts[1])
        except:
            error = statemachine.memo.reporter.error(
                  'Invalid image attribute value for "%s" at line %s: "%s" is '
                  'not an integer.' % (name, lineno, parts[1]),
                  [nodes.literal_block(match.string, match.string)])
            return [error], blankfinish
        attributes[name.lower()] = value
    imagenode = nodes.image(data, **attributes)
    return [imagenode], blankfinish

def figure(match, typename, data, state, statemachine):
    lineoffset = statemachine.lineoffset
    (imagenode,), blankfinish = image(match, typename, data, state,
                                      statemachine)
    indented, indent, offset, blankfinish \
          = statemachine.getfirstknownindented(sys.maxint)
    blocktext = '\n'.join(statemachine.inputlines[lineoffset:
                                                  statemachine.lineoffset+1])
    blocktext = match.string + '\n'.join(indented[1:])
    text = '\n'.join(indented)
    if not isinstance(imagenode, nodes.image):
        if indented:
            error = statemachine.memo.reporter.error(
                  'Rendering the figure block as a literal block.')
            literalblock = nodes.literal_block(text, text)
            nodelist = [imagenode, error, literalblock]
            return nodelist, blankfinish
        else:
            return [imagenode], blankfinish
    figurenode = nodes.figure('', imagenode)
    if not text:
        return [figurenode], blankfinish
    node = nodes.Element()              # anonymous container for parsing
    state.nestedparse(indented, lineoffset, node)
    firstnode = node[0]
    if isinstance(firstnode, nodes.paragraph):
        caption = nodes.caption(firstnode.rawsource, '', *firstnode.children)
        figurenode += caption
    elif not (isinstance(firstnode, nodes.comment) and len(firstnode) == 0):
        error = self.statemachine.memo.reporter.error(
              'Figure caption must be a paragraph or empty comment. '
              'Rendering the figure block as a literal block.')
        literalblock = nodes.literal_block(text, text)
        nodelist = [figurenode, error, literalblock]
        return nodelist, blankfinish
    if len(node) > 1:
        figurenode += nodes.legend('', *node[1:])
    return [figurenode], blankfinish
