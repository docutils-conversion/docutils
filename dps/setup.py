#!/usr/bin/env python
# $Id: setup.py,v 1.2 2001/07/28 04:48:21 goodger Exp $

from distutils.core import setup

def do_setup():
    dist = setup(name = 'dps',
          description = 'Python Docstring Processing System',
          #long_description = '',
          url = 'http://docstring.sourceforge.net/',
          version = '0.4',
          author = 'David Goodger',
          author_email = 'dgoodger@bigfoot.com',
          license = 'public domain',
          packages = ['dps', 'dps.parsers', 'dps.formatters',
                      'dps.languages'])
    return dist

if __name__ == '__main__' :
    do_setup()
