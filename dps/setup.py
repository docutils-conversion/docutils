#!/usr/bin/env python
# $Id: setup.py,v 1.5 2002/01/30 04:56:15 goodger Exp $

from distutils.core import setup

def do_setup():
    dist = setup(name = 'dps',
          description = 'Python Docstring Processing System',
          #long_description = '',
          url = 'http://docstring.sourceforge.net/',
          version = '0.3+',
          author = 'David Goodger',
          author_email = 'goodger@users.sourceforge.net',
          license = 'public domain',
          packages = ['dps', 'dps.parsers', 'dps.transforms',
                      'dps.languages'])
    return dist

if __name__ == '__main__' :
    do_setup()
