#!/usr/bin/env python
# $Id: quicktest.py,v 1.4 2001/08/22 03:56:44 goodger Exp $
#
# I used to have a much prettier version of this script, but
# inadvertently deleted it. Oops. Here's a quick, ugly, grotty hack
# as a temporary replacement. --gtk

"""\
quicktest.py: quickly test the restructuredtext parser.

Usage: quicktest.py [-x|-p|-t] [-q] [filename]

    filename     : filename to use as input (default is stdin)
    -x --xml     : output raw xml
    -p --pretty  : output pretty print (default)
    -t --test    : output in test format as per test_states.py
    -q --quiet   : don't print delimeters (except test wrappers)
"""

"""
:Author: Garth Kidd
:Contact: garth@deadlybloodyserious.com
:Revision: $Revision: 1.4 $
:Date: $Date: 2001/08/22 03:56:44 $
:Copyright: This module has been placed in the public domain.

"""

import sys
import getopt
try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser

def usage():
    print __doc__

def _pretty(input, document):
    return document.pprint()

def _xml(input, document):
    return document.asdom().toxml()

def _test(input, document):
    tq = '"""'
    output = _pretty(document)
    return """\
    proven['change_this_test_name'] = [
[%s\\
%s
%s,
%s\\
%s
%s],
]""" % ( tq, input, tq, tq, output, tq )

_outputFormatters = {
    'xml': _xml,
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
        opts, args = getopt.getopt(sys.argv[1:], "xptq",
            [ "xml", "pretty", "test", "quiet" ])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for o, a in opts:
        if o in ['-h', '--help']: # undocumented!
            usage()
            sys.exit()
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
    print format(outputFormat, input, document) # format & print

if __name__ == '__main__':
    main()
