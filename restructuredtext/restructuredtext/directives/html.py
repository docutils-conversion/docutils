#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2002/02/20 04:21:45 $
:Copyright: This module has been placed in the public domain.

Directives for typically HTML-specific constructs.
"""

__docformat__ = 'reStructuredText'

__all__ = ['meta', 'imagemap']


from dps import nodes, utils
try:
    from restructuredtext import states
except ImportError:
    from dps.parsers.restructuredtext import states


def meta(match, typename, data, state, statemachine, attributes):
    block, indent, offset, blankfinish = \
          statemachine.getfirstknownindented(match.end(), uptoblank=1)
    node = nodes.Element()
    if block:
        newlineoffset, blankfinish = state.nestedlistparse(
              block, offset, node, initialstate='MetaBody',
              blankfinish=blankfinish, statemachinekwargs=metaSMkwargs)
        if (newlineoffset - offset) != len(block): # incomplete parse of block?
            msg = statemachine.memo.reporter.error(
                  'Invalid meta directive at line %s.'
                  % statemachine.abslineno())
            node += msg
    else:
        msg = statemachine.memo.reporter.error(
              'Empty meta directive at line %s.' % statemachine.abslineno())
        node += msg
    return node.getchildren(), blankfinish

def imagemap(match, typename, data, state, statemachine, attributes):
    return [], 0


class MetaBody(states.SpecializedBody):

    class meta(nodes.Special, nodes.PreBibliographic, nodes.Element):
        """HTML-specific "meta" element."""
        pass

    def fieldmarker(self, match, context, nextstate):
        """Meta element."""
        node, blankfinish = self.parsemeta(match)
        self.statemachine.node += node
        return [], nextstate, []

    def parsemeta(self, match):
        name, args = self.parsefieldmarker(match)
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        node = self.meta()
        node['content'] = ' '.join(indented)
        try:
            attname, val = utils.extract_name_value(name)[0]
            node[attname.lower()] = val
        except utils.AttributeParsingError:
            node['name'] = name
        for arg in args:
            try:
                attname, val = utils.extract_name_value(arg)[0]
                node[attname.lower()] = val
            except utils.AttributeParsingError, detail:
                msg = self.statemachine.memo.reporter.error(
                      'Error parsing meta tag attribute "%s": %s'
                      % (arg, detail))
                self.statemachine.node += msg
        return node, blankfinish


metaSMkwargs = {'stateclasses': (MetaBody,)}
