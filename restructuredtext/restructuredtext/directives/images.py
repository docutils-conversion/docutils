#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/12 04:07:07 $
:Copyright: This module has been placed in the public domain.

Directives for figures and simple images.
"""

__docformat__ = 'reStructuredText'

__all__ = ['image', 'figure']


from restructuredtext import states
from dps import nodes


def image(match, typename, data, state, statemachine):
    blankfinish = statemachine.nextlineblank()
    lineno = statemachine.abslineno()
    if not data:
        error = statemachine.memo.errorist.error(
              'Missing image URI argument at line %s.' % lineno,
              [nodes.literal_block(match.string, match.string)])
        return [error], blankfinish
    tokens = data.split()
    attributes = {'uri': tokens[0]}
    for token in tokens[1:]:
        parts = token.split('=')
        if parts[0].lower() not in ('height', 'width', 'scale'):
            error = statemachine.memo.errorist.error(
                  'Unknown image attribute "%s" at line %s.'
                  % (parts[0], lineno),
                  [nodes.literal_block(match.string, match.string)])
            return [error], blankfinish
        if len(parts) != 2:
            error = statemachine.memo.errorist.error(
                  'Invalid image attribute expression at line %s: "%s".'
                  % (lineno, token),
                  [nodes.literal_block(match.string, match.string)])
            return [error], blankfinish
        name = parts[0].lower()
        if attributes.has_key(name):
            error = statemachine.memo.errorist.error(
                  'Duplicate image attribute name at line %s: "%s"'
                  % (lineno, name),
                  [nodes.literal_block(match.string, match.string)])
            return [error], blankfinish
        try:
            value = int(parts[1])
        except:
            error = statemachine.memo.errorist.error(
                  'Invalid image attribute value for "%s" at line %s: "%s" is '
                  'not an integer.' % (name, lineno, value),
                  [nodes.literal_block(match.string, match.string)])
            return [error], blankfinish
        attributes[name.lower()] = value
    imagenode = nodes.image(data, **attributes)
    return [imagenode], blankfinish

def figure(match, typename, data, state, statemachine):
    (imagenode,), blankfinish = image(match, typename, data, state,
                                      statemachine)
    indented, indent, lineoffset, blankfinish \
          = statemachine.getfirstknownindented(len(match.string))
    text = '\n'.join(indented)
    if not isinstance(imagenode, nodes.image):
        if indented:
            error = self.statemachine.memo.errorist.error(
                  'Rendering the figure block as a literal block.')
            literalblock = nodes.literal_block(text, text)
            nodelist = [imagenode, error, literalblock]
            return nodelist, blankfinish
        else:
            return [imagenode], blankfinish
    figurenode = nodes.figure('', imagenode)
    if not text:
        return [figurenode], blankfinish
    node = nodes._Element()
    state.nestedparse(indented, lineoffset, node)
    firstnode = node[0]
    if isinstance(firstnode, nodes.paragraph):
        caption = nodes.caption(firstnode.rawsource, '', *firstnode.children)
        figurenode += caption
    elif not (isinstance(firstnode, nodes.comment) and len(firstnode) == 0):
        error = self.statemachine.memo.errorist.error(
              'Figure caption must be a paragraph or empty comment. '
              'Rendering the figure block as a literal block.')
        literalblock = nodes.literal_block(text, text)
        nodelist = [figurenode, error, literalblock]
        return nodelist, blankfinish
    if len(node) > 1:
        figurenode += nodes.legend('', *node[1:])
    return [figurenode], blankfinish
