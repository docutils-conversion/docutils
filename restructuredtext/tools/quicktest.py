#!/usr/bin/env python

"""\
quicktest.py: quickly test the restructuredtext parser.

Usage::

    quicktest.py [-p|-r|-t|-x] [filename]

``filename`` is the name of the file to use as input (default is stdin).

Options:

-p, --pretty  output pretty pseudo-xml: no '&abc;' entities (default)
-r, --rawxml  output raw xml
-t, --test    output in test format as per test_states.py
-x, --xml     output pretty xml (indented)
"""

"""
:Author: Garth Kidd
:Contact: garth@deadlybloodyserious.com
:Revision: $Revision: 1.6 $
:Date: $Date: 2001/09/08 03:30:08 $
:Copyright: This module has been placed in the public domain.

"""

import sys, os, getopt
from StringIO import StringIO

try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser

def usage():
    print __doc__

def _pretty(input, document):
    return document.pformat()

def _rawxml(input, document):
    return document.asdom().toprettyxml('', '\n')

def _prettyxml(input, document):
    return document.asdom().toprettyxml('    ', '\n')

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

def getArgs():
	if os.name == 'mac' and len(sys.argv) <= 1:
		return macGetArgs()
	else:
		return posixGetArgs()

def posixGetArgs():
    outputFormat = 'pretty'
    try:
        opts, args = getopt.getopt(sys.argv[1:], "rxpth",
            [ "rawxml", "xml", "pretty", "test", "help" ])
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
    return inputFile, outputFormat

def main():
    inputFile, outputFormat = getArgs() # process cmdline arguments
    parser = Parser()                   # create a parser
    input = inputFile.read()            # gather input
    document = parser.parse(input)      # parse the input
    print format(outputFormat, input, document), # format & print

if __name__ == '__main__':
    main()
