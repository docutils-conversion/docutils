#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.4 $
:Date: $Date: 2001/09/12 04:02:18 $
:Copyright: This module has been placed in the public domain.

This package contains directive implementation modules.
"""

__docformat__ = 'reStructuredText'

__all__ = ['directive']

_directive_registry = {
      'restructuredtext-test-directive': ('directivetest',
                                          'directive_test_function'),
      'image': ('images', 'image'),
      'figure': ('images', 'figure'),
      'note': ('admonitions', 'note'),
      'tip': ('admonitions', 'tip'),
      'warning': ('admonitions', 'warning'),
      'error': ('admonitions', 'error'),
      'caution': ('admonitions', 'caution'),
      'danger': ('admonitions', 'danger'),
      'important': ('admonitions', 'important'),}
"""Mapping of directive name to (module name, function name). The directive
'name' is canonical & must be lowercase; language-dependent names are defined
in the language package."""

_modules = {}
"""Cache of imported directive modules."""

_directives = {}
"""Cache of imported directive functions."""

def directive(directivename, languagemodule):
    normname = directivename.lower()
    if _directives.has_key(normname):
        return _directives[normname]
    try:
        canonicalname = languagemodule.directives[normname]
        modulename, functionname = _directive_registry[canonicalname]
    except KeyError:
        return None
    if _modules.has_key(modulename):
        module = _modules[modulename]
    else:
        try:
            module = __import__(modulename, globals(), locals())
        except ImportError:
            return None
    try:
        function = getattr(module, functionname)
    except AttributeError:
        return None
    return function
