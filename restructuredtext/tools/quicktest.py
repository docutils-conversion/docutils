#!/usr/bin/env python
# $Id: quicktest.py,v 1.3 2001/08/03 01:19:37 gtk Exp $
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
Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.3 $
Date: $Date: 2001/08/03 01:19:37 $
Copyright: This module has been placed in the public domain.

"""

import sys
import dps.parsers.restructuredtext
import getopt

def usage(): 
    print __doc__

def _parse_pretty(parser, text):
    return parser.parse(text).pprint()

def _parse_xml(parser, text):
    return parser.parse(text).asdom().toxml()

def _parse_test(parser, text):
    tq = '"""'
    output = _parse_pretty(parser, text)
    return """\
    proven['change_this_test_name'] = [
[%s\\
%s
%s,
%s\\
%s
%s],
]""" % ( tq, text, tq, tq, output, tq )

_outputHandlers = {
    'xml': _parse_xml,
    'pretty' : _parse_pretty,
    'test': _parse_test
    }

def formattedOutput(format, parser, text): 
    handler = _outputHandlers[format]
    return apply(handler, (parser, text))
    
def main(): 
    outputFormat = 'pretty'
    inputFile = sys.stdin
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

    # All of that hard work getting the options, when doing the work
    # couldn't possibly be simpler:
    
    # create a parser
    parser = dps.parsers.restructuredtext.Parser()

    # gather input
    input = inputFile.read()

    # print a delimiter
    if not isQuiet:
        print '=>'
        
    # print the parser output
    print formattedOutput(outputFormat, parser, input)

if __name__ == '__main__':
    main()
