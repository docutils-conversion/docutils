#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/09/07 02:03:14 $
:Copyright: This module has been placed in the public domain.

"""

import sys
import nodes


class SystemWarning(Exception):

    def __init__(self, system_warning):
        Exception.__init__(self, system_warning.astext())


class Errorist:

    def __init__(self, warninglevel, errorlevel, warningstream=sys.stderr):
        self.warninglevel = warninglevel
        self.errorlevel = errorlevel
        self.stream = warningstream

    def system_warning(self, level, comment=None, children=[]):
        """
        Return a system_warning object.

        Raise an exception or generate a warning if appropriate.
        """
        sw = nodes.system_warning(comment, level=level, *children)
        if level >= self.errorlevel:
            raise SystemWarning(sw)
        if level >= self.warninglevel:
            print >>self.stream, 'Warning:', sw.astext()
        return sw

    def information(self, comment=None, children=[]):
        return self.system_warning(0, comment, children)

    def warning(self, comment=None, children=[]):
        return self.system_warning(1, comment, children)

    def error(self, comment=None, children=[]):
        return self.system_warning(2, comment, children)

    def severe(self, comment=None, children=[]):
        return self.system_warning(3, comment, children)

    def strong_system_warning(self, admonition, comment, sourcetext=None):
        p = nodes.paragraph()
        p += nodes.strong('', admonition)
        p += nodes.Text(': ' + comment)
        children = [p]
        if sourcetext:
            children.append(nodes.literal_block('', sourcetext))
        return self.system_warning(3, children=children)


languages = {}

def language(languagecode):
    if languages.has_key(languagecode):
        return languages[languagecode]
    try:
        module = getattr(__import__('dps.languages', globals(), locals(),
                                    [languagecode]),
                         languagecode)
    except:
        raise
    languages[languagecode] = module
    return module
