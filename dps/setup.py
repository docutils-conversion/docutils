#!/usr/bin/env python
# $Id: setup.py,v 1.3 2001/08/23 03:53:54 goodger Exp $

from distutils.core import setup

def do_setup():
    dist = setup(name = 'dps',
          description = 'Python Docstring Processing System',
          #long_description = '',
          url = 'http://docstring.sourceforge.net/',
          version = '0.4',
          author = 'David Goodger',
          author_email = 'goodger@users.sourceforge.net',
          license = 'public domain',
          packages = ['dps', 'dps.parsers', 'dps.formatters',
                      'dps.languages'])
    return dist

if __name__ == '__main__' :
    do_setup()
