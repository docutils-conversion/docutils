#!/usr/bin/env python
#
# I used to have a much prettier version of this script, but
# inadvertently deleted it. Oops. Here's a quick, ugly, grotty hack
# as a temporary replacement. --gtk

"""\
quicktest.py: quickly test the restructuredtext parser.

Usage::

    quicktest.py [-p|-q|-r|-t|-x] [-q] [filename]

``filename`` is the name of the file to use as input (default is stdin).

Options:

-p, --pretty  output pretty pseudo-xml: no '&abc;' entities (default)
-q, --quiet   don't print delimeters (except test wrappers)
-r, --rawxml  output raw xml
-t, --test    output in test format as per test_states.py
-x, --xml     output pretty xml (indented)
"""

"""
:Author: Garth Kidd
:Contact: garth@deadlybloodyserious.com
:Revision: $Revision: 1.5 $
:Date: $Date: 2001/08/25 02:14:30 $
:Copyright: This module has been placed in the public domain.

"""

import sys
import getopt
from StringIO import StringIO

try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser

def usage():
    print __doc__

def _pretty(input, document):
    return document.pprint()

def _xml(document, indent):
    writer = StringIO()
    document.asdom().writexml(writer, '', indent, '\n')
    return writer.getvalue()

def _rawxml(input, document):
    return _xml(document, '')

def _prettyxml(input, document):
    return _xml(document, '    ')

def _test(input, document):
    tq = '"""'
    output = _pretty(input, document)
    return """\
    totest['change_this_test_name'] = [
[%s\\
%s
%s,
%s\\
%s
%s],
]
""" % ( tq, escape(input.rstrip()), tq, tq, escape(output.rstrip()), tq )

def escape(text):
    """
    Return `text` in a form compatible with triple-double-quoted Python strings.
    """
    return text.replace('\\', '\\\\').replace('"""', '""\\"')

_outputFormatters = {
    'rawxml': _rawxml,
    'xml': _prettyxml,
    'pretty' : _pretty,
    'test': _test
    }

def format(outputFormat, input, document):
    formatter = _outputFormatters[outputFormat]
    return formatter(input, document)

def main():
    outputFormat = 'pretty'
    isQuiet = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], "rxptq",
            [ "rawxml", "xml", "pretty", "test", "quiet" ])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ['-h', '--help']: # undocumented!
            usage()
            sys.exit()
        elif o in ['-r', '--rawxml']:
            outputFormat = 'rawxml'
        elif o in ['-x', '--xml']:
            outputFormat = 'xml'
        elif o in ['-p', '--pretty']:
            outputFormat = 'pretty'
        elif o in ['-t', '--test']:
            outputFormat = 'test'
        elif o in ['-q', '--quiet']:
            isQuiet = 1
        else:
            raise AssertionError, "getopt should have saved us!"

    if len(args)>1:
        print "Only one file at a time, thanks."
        usage()
        sys.exit(1)

    if len(args) == 1:
        inputFile = open(args[0])
    else:
        inputFile = sys.stdin

    # All of that hard work getting the options, when doing the work
    # couldn't possibly be simpler:

    parser = Parser()                   # create a parser
    input = inputFile.read()            # gather input
    if not isQuiet:                     # print a delimiter
        print '=>'
    document = parser.parse(input)      # parse the input
    print format(outputFormat, input, document), # format & print

if __name__ == '__main__':
    main()
