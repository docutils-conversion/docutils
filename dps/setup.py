#!/usr/bin/env python
# $Id: setup.py,v 1.6 2002/02/06 03:04:19 goodger Exp $

from distutils.core import setup

def do_setup():
    dist = setup(
          name = 'dps',
          description = 'Python Docstring Processing System',
          #long_description = '',
          url = 'http://docstring.sourceforge.net/',
          version = '0.3+',
          author = 'David Goodger',
          author_email = 'goodger@users.sourceforge.net',
          license = 'public domain',
          packages = ['dps', 'dps.readers', 'dps.parsers', 'dps.writers',
                      'dps.transforms', 'dps.languages'])
    return dist

if __name__ == '__main__' :
    do_setup()
