#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.17 $
:Date: $Date: 2002/03/11 03:37:55 $
:Copyright: This module has been placed in the public domain.

Miscellaneous utilities for the documentation utilities.
"""

import sys
import nodes


class SystemMessage(Exception):

    def __init__(self, system_message):
        Exception.__init__(self, system_message.astext())


class Reporter:

    """
    Info/warning/error reporter and ``system_message`` element generator.

    Five levels of system messages are defined, along with corresponding
    methods: `debug()`, `info()`, `warning()`, `error()`, and `severe()`.

    There is typically one Reporter object per process. A Reporter object is
    instantiated with thresholds for generating warnings and errors (raising
    exceptions), a switch to turn debug output on or off, and an I/O stream
    for warnings. These are stored in the default reporting category, ''
    (zero-length string).

    Multiple reporting categories [#]_ may be set, each with its own warning
    and error thresholds, debugging switch, and warning stream. Categories are
    hierarchically-named strings that look like attribute references: 'spam',
    'spam.eggs', 'neeeow.wum.ping'. The 'spam' category is the ancestor of
    'spam.bacon.eggs'. Unset categories inherit stored values from their
    closest ancestor category that has been set.

    When a system message is generated, the stored values from its category
    (or ancestor if unset) are retrieved. The system message level is compared
    to the thresholds stored in the category, and a warning or error is
    generated as appropriate. Debug messages are produced iff the stored debug
    switch is on. Message output is sent to the stored warning stream.

    .. [#]_ The concept of "categories" was inspired by the log4j project:
       http://jakarta.apache.org/log4j/.
    """

    levels = 'DEBUG INFO WARNING ERROR SEVERE'.split()
    """List of names for system message levels, indexed by level."""

    def __init__(self, warninglevel, errorlevel, stream=None, debug=0):
        """
        Initialize the `ConditionSet` forthe `Reporter`'s default category.

        :Parameters:

            - `warninglevel`: The level at or above which warning output will
              be sent to `stream`.
            - `errorlevel`: The level at or above which `SystemMessage`
              exceptions will be raised.
            - `debug`: Show debug (level=0) system messages?
            - `stream`: Where warning output is sent (`None` implies
              `sys.stderr`).
        """

        if stream is None:
            stream = sys.stderr

        self.categories = {'': ConditionSet(debug, warninglevel, errorlevel,
                                            stream)}
        """Mapping of category names to conditions. Default category is ''."""

    def setconditions(self, category, warninglevel, errorlevel,
                      stream=None, debug=0):
        if stream is None:
            stream = sys.stderr
        self.categories[category] = ConditionSet(debug, warninglevel,
                                                 errorlevel, stream)

    def unsetconditions(self, category):
        if category and self.categories.has_key(category):
            del self.categories[category]

    __delitem__ = unsetconditions

    def getconditions(self, category):
        while not self.categories.has_key(category):
            category = category[:category.rfind('.') + 1][:-1]
        return self.categories[category]

    __getitem__ = getconditions

    def system_message(self, level, comment=None, category='',
                       *children, **attributes):
        """
        Return a system_message object.

        Raise an exception or generate a warning if appropriate.
        """
        msg = nodes.system_message(comment, level=level,
                                   type=self.levels[level],
                                   *children, **attributes)
        debug, warninglevel, errorlevel, stream = self[category].astuple()
        if level >= warninglevel or debug and level == 0:
            if category:
                print >>stream, 'Reporter "%s":' % category, msg.astext()
            else:
                print >>stream, 'Reporter:', msg.astext()
        if level >= errorlevel:
            raise SystemMessage(msg)
        return msg

    def debug(self, comment=None, category='', *children, **attributes):
        """
        Level-0, "DEBUG": an internal reporting issue. Typically, there is no
        effect on the processing. Level-0 system messages are handled
        separately from the others.
        """
        return self.system_message(
              0, comment, category, *children, **attributes)

    def info(self, comment=None, category='', *children, **attributes):
        """
        Level-1, "INFO": a minor issue that can be ignored. Typically there is
        no effect on processing, and level-1 system messages are not reported.
        """
        return self.system_message(
              1, comment, category, *children, **attributes)

    def warning(self, comment=None, category='', *children, **attributes):
        """
        Level-2, "WARNING": an issue that should be addressed. If ignored,
        there may be unpredictable problems with the output.
        """
        return self.system_message(
              2, comment, category, *children, **attributes)

    def error(self, comment=None, category='', *children, **attributes):
        """
        Level-3, "ERROR": an error that should be addressed. If ignored, the
        output will contain errors.
        """
        return self.system_message(
              3, comment, category, *children, **attributes)

    def severe(self, comment=None, category='', *children, **attributes):
        """
        Level-4, "SEVERE": a severe error that must be addressed. If ignored,
        the output will contain severe errors. Typically level-4 system
        messages are turned into exceptions which halt processing.
        """
        return self.system_message(
              4, comment, category, *children, **attributes)


class ConditionSet:

    """
    A set of thresholds, switches, and streams corresponding to one `Reporter`
    category.
    """

    def __init__(self, debug, warninglevel, errorlevel, stream):
        self.debug = debug
        self.warninglevel = warninglevel
        self.errorlevel = errorlevel
        self.stream = stream

    def astuple(self):
        return (self.debug, self.warninglevel, self.errorlevel,
                self.stream)


class AttributeParsingError(Exception): pass
class BadAttributeLineError(AttributeParsingError): pass
class BadAttributeDataError(AttributeParsingError): pass
class DuplicateAttributeError(AttributeParsingError): pass


def parseattributes(lines, attributespec):
    """
    Return a dictionary mapping attribute names to converted values.

    :Parameters:
        - `lines`: List of one-line strings of the form::

            ['[name1=value1 name2=value2]', '[name3="value 3"]']

        - `attributespec`: Dictionary mapping known attribute names to a
          conversion function such as `int` or `float`.

    :Exceptions:
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

    :Exceptions:
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
        attlist += extract_name_value(line)
    return attlist

def extract_name_value(line):
    """
    Return a list of (name, value) from a line of the form "name=value ...".

    :Exception:
        `BadAttributeDataError` for invalid attribute data (missing name,
        missing data, bad quotes, etc.).
    """
    attlist = []
    while line:
        equals = line.find('=')
        if equals == -1:
            raise BadAttributeDataError('missing "="')
        attname = line[:equals].strip()
        if equals == 0 or not attname:
            raise BadAttributeDataError(
                  'missing attribute name before "="')
        line = line[equals+1:].lstrip()
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

    :Exceptions:
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

def newdocument(languagecode='en', warninglevel=2, errorlevel=4,
                stream=None, debug=0):
    reporter = Reporter(warninglevel, errorlevel, stream, debug)
    document = nodes.document(languagecode=languagecode, reporter=reporter)
    return document
