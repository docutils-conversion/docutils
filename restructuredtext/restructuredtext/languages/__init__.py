#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/10 04:46:13 $
:Copyright: This module has been placed in the public domain.

This package contains modules for language-dependent features of
reStructuredText.
"""

__docformat__ = 'reStructuredText'

__all__ = ['language']

_languages = {}

def language(languagecode):
    if _languages.has_key(languagecode):
        return _languages[languagecode]
    try:
        module = __import__(languagecode, globals(), locals())
    except:
        raise
    _languages[languagecode] = module
    return module
