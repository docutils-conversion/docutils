#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.8 $
:Date: $Date: 2002/03/12 03:09:12 $
:Copyright: This module has been placed in the public domain.

Directives for figures and simple images.
"""

__docformat__ = 'reStructuredText'

__all__ = ['image', 'figure']


import sys
try:
    from restructuredtext import states
except ImportError:
    from dps.parsers.restructuredtext import states
from dps import nodes, utils

def unchanged(arg):
    return arg

imageattributes = {'alt': unchanged, 'height': int, 'width': int, 'scale': int}

def image(match, typename, data, state, statemachine, attributes):
    lineno = statemachine.abslineno()
    lineoffset = statemachine.lineoffset
    datablock, indent, offset, blankfinish = \
          statemachine.getfirstknownindented(match.end(), uptoblank=1)
    if not datablock:
        error = statemachine.memo.reporter.error(
              'Missing image URI argument at line %s.' % lineno, '',
              nodes.literal_block(match.string, match.string))
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
              'Image URI at line %s contains whitespace.' % lineno, '',
              nodes.literal_block(blocktext, blocktext))
        return [error], blankfinish
    try:
        attributes.update(utils.parseattributes(attlines, imageattributes))
    except KeyError, detail:
        error = statemachine.memo.reporter.error(
              'Unknown image attribute at line %s: "%s".' % (lineno, detail),
              '', nodes.literal_block(blocktext, blocktext))
        return [error], blankfinish
    except ValueError, detail:
        error = statemachine.memo.reporter.error(
              'Invalid image attribute value at line %s: %s.'
              % (lineno, detail), '',
              nodes.literal_block(blocktext, blocktext))
        return [error], blankfinish
    except utils.AttributeParsingError, detail:
        error = statemachine.memo.reporter.error(
              'Invalid image attribute data at line %s: %s.'
              % (lineno, detail), '',
              nodes.literal_block(blocktext, blocktext))
        return [error], blankfinish
    attributes['uri'] = reference
    imagenode = nodes.image(blocktext, **attributes)
    return [imagenode], blankfinish

def figure(match, typename, data, state, statemachine, attributes):
    lineoffset = statemachine.lineoffset
    (imagenode,), blankfinish = image(match, typename, data, state,
                                      statemachine, attributes)
    indented, indent, offset, blankfinish \
          = statemachine.getfirstknownindented(sys.maxint)
    blocktext = '\n'.join(statemachine.inputlines[lineoffset:
                                                  statemachine.lineoffset+1])
    if isinstance(imagenode, nodes.system_message):
        if indented:
            imagenode[-1] = nodes.literal_block(blocktext, blocktext)
        return [imagenode], blankfinish
    figurenode = nodes.figure('', imagenode)
    if indented:
        node = nodes.Element()          # anonymous container for parsing
        state.nestedparse(indented, lineoffset, node)
        firstnode = node[0]
        if isinstance(firstnode, nodes.paragraph):
            caption = nodes.caption(firstnode.rawsource, '',
                                    *firstnode.children)
            figurenode += caption
        elif not (isinstance(firstnode, nodes.comment) and len(firstnode) == 0):
            error = statemachine.memo.reporter.error(
                  'Figure caption must be a paragraph or empty comment.', '',
                  nodes.literal_block(blocktext, blocktext))
            return [figurenode, error], blankfinish
        if len(node) > 1:
            figurenode += nodes.legend('', *node[1:])
    return [figurenode], blankfinish
