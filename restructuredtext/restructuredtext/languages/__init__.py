#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/02/06 02:25:41 $
:Copyright: This module has been placed in the public domain.

This package contains modules for language-dependent features of
reStructuredText.
"""

__docformat__ = 'reStructuredText'

__all__ = ['getlanguage']

_languages = {}

def getlanguage(languagecode):
    if _languages.has_key(languagecode):
        return _languages[languagecode]
    module = __import__(languagecode, globals(), locals())
    _languages[languagecode] = module
    return module
