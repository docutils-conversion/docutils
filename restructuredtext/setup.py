#!/usr/bin/env python
# $Id: setup.py,v 1.3 2001/08/23 04:08:49 goodger Exp $

from distutils.core import setup

def do_setup():
    dist = setup(
          name = 'restructuredtext',
          description = 'reStructuredText parser for Python DPS',
          #long_description = '',
          url = 'http://structuredtext.sourceforge.net/',
          version = '0.4',
          author = 'David Goodger',
          author_email = 'goodger@users.sourceforge.net',
          license = 'public domain',
          packages = ['dps.parsers.restructuredtext',
                      'dps.parsers.restructuredtext.directives'],
          package_dir = {'dps.parsers.restructuredtext': 'restructuredtext'})
    return dist

if __name__ == '__main__' :
    do_setup()
