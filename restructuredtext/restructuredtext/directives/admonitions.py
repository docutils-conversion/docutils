#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/12 04:05:41 $
:Copyright: This module has been placed in the public domain.

Admonition directives.
"""

__docformat__ = 'reStructuredText'

__all__ = ['note', 'tip', 'warning', 'error', 'caution', 'danger', 'important']


from restructuredtext import states
from dps import nodes


def admonition(nodeclass, match, typename, data, state, statemachine):
    indented, indent, lineoffset, blankfinish \
          = statemachine.getfirstknownindented(match.end())
    text = '\n'.join(indented)
    admonitionnode = nodeclass(text)
    if text:
        state.nestedparse(indented, lineoffset, admonitionnode)
    return [admonitionnode], blankfinish

def note(*args, **kwargs):
    return admonition(nodes.note, *args, **kwargs)

def tip(*args, **kwargs):
    return admonition(nodes.tip, *args, **kwargs)

def warning(*args, **kwargs):
    return admonition(nodes.warning, *args, **kwargs)

def error(*args, **kwargs):
    return admonition(nodes.error, *args, **kwargs)

def caution(*args, **kwargs):
    return admonition(nodes.caution, *args, **kwargs)

def danger(*args, **kwargs):
    return admonition(nodes.danger, *args, **kwargs)

def important(*args, **kwargs):
    return admonition(nodes.important, *args, **kwargs)
