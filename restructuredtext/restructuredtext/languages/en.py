#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.7 $
:Date: $Date: 2002/02/12 02:27:47 $
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
      'warning': 'warning',
      'meta': 'meta',
      'imagemap': 'imagemap'}
"""English name to registered (in directives/__init__.py) directive name
mapping."""
