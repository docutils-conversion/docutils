#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/11/09 23:18:25 $
:Copyright: This module has been placed in the public domain.

Test directive implementation.
"""

__docformat__ = 'reStructuredText'

__all__ = ['directive_test_function']


from restructuredtext import states
from dps import nodes


def directive_test_function(match, typename, data, state, statemachine):
    atts = {'type': typename}
    if data:
        atts['data'] = data
    try:
        statemachine.nextline()
        indented, indent, offset, blankfinish = statemachine.getindented()
        text = '\n'.join(indented)
    except IndexError:
        text = ''
        blankfinish = 1
    directivenode = nodes.directive(text, text, **atts)
    return [directivenode], blankfinish
