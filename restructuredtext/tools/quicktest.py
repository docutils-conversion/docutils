#!/usr/bin/env python

"""
:Author: Garth Kidd
:Contact: garth@deadlybloodyserious.com
:Revision: $Revision: 1.8 $
:Date: $Date: 2001/09/21 03:53:44 $
:Copyright: This module has been placed in the public domain.
"""

import sys, os, getopt
from StringIO import StringIO

try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser


usage_header = """\
quicktest.py: quickly test the restructuredtext parser.

Usage::

    quicktest.py [options] [filename]

``filename`` is the name of the file to use as input (default is stdin).

Options:
"""

options = [#(long option, short option, description)
           ('pretty', 'p',
            'output pretty pseudo-xml: no "&abc;" entities (default)'),
           ('test', 't', 'output parser test data (input & expected output)'),
           ('rawxml', 'r', 'output raw XML'),
           ('styledxml', 's', 'output XML with XSL style sheet reference'),
           ('xml', 'x', 'output pretty XML (indented)'),
           ('help', 'h', 'show help text')]

def usage():
    print usage_header
    for longopt, shortopt, description in options:
        print '-%s, --%-9s' % (shortopt, longopt),
        if len(longopt) > 8:
            print '%-16s' % '\n',
        print description

def _pretty(input, document):
    return document.pformat()

def _rawxml(input, document):
    return document.asdom().toprettyxml('', '\n')

def _styledxml(input, document):
    docnode = document.asdom().childNodes[0]
    return '%s\n%s\n%s' % (
          '<?xml version="1.0" encoding="ISO-8859-1"?>',
          '<?xml-stylesheet type="text/xsl" href="rtxt2html.xsl"?>',
          docnode.toprettyxml('', '\n'))

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
    'styledxml': _styledxml,
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
        return posixGetArgs(sys.argv[1:])

def posixGetArgs(argv):
    outputFormat = 'pretty'
    shortopts = ''.join([option[1] for option in options])
    longopts = [option[0] for option in options]
    try:
        opts, args = getopt.getopt(argv, shortopts, longopts)
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for o, a in opts:
        if o in ['-h', '--help']:
            usage()
            sys.exit()
        elif o in ['-r', '--rawxml']:
            outputFormat = 'rawxml'
        elif o in ['-s', '--styledxml']:
            outputFormat = 'styledxml'
        elif o in ['-x', '--xml']:
            outputFormat = 'xml'
        elif o in ['-p', '--pretty']:
            outputFormat = 'pretty'
        elif o in ['-t', '--test']:
            outputFormat = 'test'
        else:
            raise getopt.GetoptError, "getopt should have saved us!"
    if len(args) > 1:
        print "Only one file at a time, thanks."
        usage()
        sys.exit(1)
    if len(args) == 1:
        inputFile = open(args[0])
    else:
        inputFile = sys.stdin
    return inputFile, outputFormat

def macGetArgs():
    import EasyDialogs
    EasyDialogs.Message("""\
In the following window, please:

1. Choose an output format from the "Option" list.
2. Click "Add" (if you don't, the default format will
   be "pretty").
3. Click "Add existing file..." and choose an input file.
4. Click "OK".""")
    optionlist = [(longopt, description)
                  for (longopt, shortopt, description) in options]
    argv = EasyDialogs.GetArgv(optionlist=optionlist, addnewfile=0, addfolder=0)
    return posixGetArgs(argv)

def main():
    inputFile, outputFormat = getArgs() # process cmdline arguments
    parser = Parser()                   # create a parser
    input = inputFile.read()            # gather input
    document = parser.parse(input)      # parse the input
    output = format(outputFormat, input, document)
    print output,


if __name__ == '__main__':
    main()
