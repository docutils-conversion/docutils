#!/usr/bin/env python
# $Id: setup.py,v 1.4 2002/01/16 02:43:49 goodger Exp $

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
          packages = ['dps', 'dps.readers', 'dps.parsers',
                      'dps.writers', 'dps.transforms',
                      'dps.languages'])
    return dist

if __name__ == '__main__' :
    do_setup()
