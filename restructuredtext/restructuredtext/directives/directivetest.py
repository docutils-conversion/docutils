#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.5 $
:Date: $Date: 2002/02/06 02:27:10 $
:Copyright: This module has been placed in the public domain.

Test directive implementation.
"""

__docformat__ = 'reStructuredText'

__all__ = ['directive_test_function']


from restructuredtext import states
from dps import nodes


def directive_test_function(match, typename, data, state, statemachine,
                            attributes):
    try:
        statemachine.nextline()
        indented, indent, offset, blankfinish = statemachine.getindented()
        text = '\n'.join(indented)
    except IndexError:
        text = ''
        blankfinish = 1
    if text:
        info = statemachine.memo.reporter.info(
              'Directive processed. Type="%s", data="%s", directive block:'
              % (typename, data), [nodes.literal_block(text, text)])
    else:
        info = statemachine.memo.reporter.info(
              'Directive processed. Type="%s", data="%s", directive block: None'
              % (typename, data))
    return [info], blankfinish
