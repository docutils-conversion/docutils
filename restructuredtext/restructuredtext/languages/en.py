#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.6 $
:Date: $Date: 2002/01/16 06:18:23 $
:Copyright: This module has been placed in the public domain.

English-language mappings for language-dependent features of
reStructuredText.
"""

__docformat__ = 'reStructuredText'

__all__ = ['directives']


from dps import nodes


directives = {
      'restructuredtext-test-directive': 'restructuredtext-test-directive',
      'image': 'image',
      'figure': 'figure',
      'attention': 'attention',
      'caution': 'caution',
      'danger': 'danger',
      'error': 'error',
      'important': 'important',
      'note': 'note',
      'tip': 'tip',
      'hint': 'hint',
      'warning': 'warning',}
"""English name to registered (in directives/__init__.py) directive name
mapping."""
