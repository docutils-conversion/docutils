#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.4 $
:Date: $Date: 2001/11/15 03:07:17 $
:Copyright: This module has been placed in the public domain.

Directives for figures and simple images.
"""

__docformat__ = 'reStructuredText'

__all__ = ['image', 'figure']


import sys
from restructuredtext import states
from dps import nodes, utils

def unchanged(arg):
    return arg

imageattributes = {'alt': unchanged, 'height': int, 'width': int, 'scale': int}

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
    for i in range(len(datablock)):
        if datablock[i][:1] == '[' and datablock[i].rstrip()[-1:] == ']':
            attlines = datablock[i:]
            datablock = datablock[:i]
            break
    else:
        attlines = []
    reference = ''.join([line.strip() for line in datablock])
    if reference.find(' ') != -1:
        error = statemachine.memo.reporter.error(
              'Image URI at line %s contains whitespace.' % lineno)
        error += nodes.literal_block(blocktext, blocktext)
        return [error], blankfinish
    try:
        attributes = utils.parseattributes(attlines, imageattributes)
    except KeyError, detail:
        error = statemachine.memo.reporter.error(
              'Unknown image attribute at line %s: "%s".' % (lineno, detail))
        error += nodes.literal_block(blocktext, blocktext)
        return [error], blankfinish
    except ValueError, detail:
        error = statemachine.memo.reporter.error(
              'Invalid image attribute value at line %s: %s.'
              % (lineno, detail))
        error += nodes.literal_block(blocktext, blocktext)
        return [error], blankfinish
    except utils.AttributeParsingError, detail:
        error = statemachine.memo.reporter.error(
              'Invalid image attribute data at line %s: %s.'
              % (lineno, detail))
        error += nodes.literal_block(blocktext, blocktext)
        return [error], blankfinish
    attributes['uri'] = reference
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
