#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.11 $
:Date: $Date: 2002/01/30 04:47:02 $
:Copyright: This module has been placed in the public domain.

"""

import sys
import nodes


class SystemWarning(Exception):

    def __init__(self, system_warning):
        Exception.__init__(self, system_warning.astext())


class Reporter:

    def __init__(self, warninglevel, errorlevel, warningstream=None):
        self.warninglevel = warninglevel
        """The level at or above which warning output will be sent to
        `self.stream`."""

        self.errorlevel = errorlevel
        """The level at or above which `SystemWarning` exceptions will be
        raised."""

        if warningstream is None:
            warningstream = sys.stderr
 
        self.stream = warningstream
        """Where warning output is sent."""

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


class AttributeParsingError(Exception): pass
class BadAttributeLineError(AttributeParsingError): pass
class BadAttributeDataError(AttributeParsingError): pass
class DuplicateAttributeError(AttributeParsingError): pass


def newdocument(languagecode='en', warninglevel=1, errorlevel=3,
                warningstream=None):
    reporter = Reporter(warninglevel, errorlevel)
    document = nodes.document(languagecode='en', reporter=reporter)
    return document

def parseattributes(lines, attributespec):
    """
    Return a dictionary mapping attribute names to converted values.

    :Parameters:
        - `lines`: List of one-line strings of the form::
          
            ['[name1=value1 name2=value2]', '[name3="value 3"]']

        - `attributespec`: Dictionary mapping known attribute names to a
          conversion function such as `int` or `float`.

    :Raises:
        - `KeyError` for unknown attribute names.
        - `ValueError` for invalid attribute values (raised by conversion
           function).
        - `DuplicateAttributeError` for duplicate attributes.
        - `BadAttributeLineError` for input lines not enclosed in brackets.
        - `BadAttributeDataError` for invalid attribute data (missing name,
          missing data, bad quotes, etc.).
    """
    attlist = extractattributes(lines)
    attdict = assembleattributes(attlist, attributespec)
    return attdict

def extractattributes(lines):
    """
    Return a list of attribute (name, value) pairs.

    :Parameter:
        `lines`: List of one-line strings of the form::

            ['[name1=value1 name2=value2]', '[name3="value 3"]']

    :Raises:
        - `BadAttributeLineError` for input lines not enclosed in brackets.
        - `BadAttributeDataError` for invalid attribute data (missing name,
          missing data, bad quotes, etc.).
    """
    attlist = []
    for line in lines:
        line = line.strip()
        if line[:1] != '[' or line[-1:] != ']':
            raise BadAttributeLineError(
                  'input line not enclosed in "[" and "]"')
        line = line[1:-1].strip()
        while line:
            equals = line.find('=')
            if equals == -1:
                raise BadAttributeDataError('missing "="')
            elif equals == 0:
                raise BadAttributeDataError(
                      'missing attribute name before "="')
            attname = line[:equals]
            line = line[equals+1:]
            if not line:
                raise BadAttributeDataError(
                      'missing value after "%s="' % attname)
            if line[0] in '\'"':
                endquote = line.find(line[0], 1)
                if endquote == -1:
                    raise BadAttributeDataError(
                          'attribute "%s" missing end quote (%s)'
                          % (attname, line[0]))
                if len(line) > endquote + 1 and line[endquote + 1].strip():
                    raise BadAttributeDataError(
                          'attribute "%s" end quote (%s) not followed by '
                          'whitespace' % (attname, line[0]))
                data = line[1:endquote]
                line = line[endquote+1:].lstrip()
            else:
                space = line.find(' ')
                if space == -1:
                    data = line
                    line = ''
                else:
                    data = line[:space]
                    line = line[space+1:].lstrip()
            attlist.append((attname.lower(), data))
    return attlist

def assembleattributes(attlist, attributespec):
    """
    Return a mapping of attribute names to values.

    :Parameters:
        - `attlist`: A list of (name, value) pairs (the output of
          `extractattributes()`).
        - `attributespec`: Dictionary mapping known attribute names to a
          conversion function such as `int` or `float`.

    :Raises:
        - `KeyError` for unknown attribute names.
        - `DuplicateAttributeError` for duplicate attributes.
        - `ValueError` for invalid attribute values (raised by conversion
           function).
    """
    attributes = {}
    for name, value in attlist:
        convertor = attributespec[name] # raises KeyError if unknown
        if attributes.has_key(name):
            raise DuplicateAttributeError('duplicate attribute "%s"' % name)
        attributes[name] = convertor(value) # raises ValueError if invalud
    return attributes

def normname(name):
    """Return a case- and whitespace-normalized name."""
    return ' '.join(name.lower().split())
