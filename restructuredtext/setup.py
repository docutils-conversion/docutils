#!/usr/bin/env python
# $Id: setup.py,v 1.2 2001/07/28 04:55:29 goodger Exp $

from distutils.core import setup

def do_setup():
    dist = setup(
          name = 'restructuredtext',
          description = 'reStructuredText parser for Python DPS',
          #long_description = '',
          url = 'http://structuredtext.sourceforge.net/',
          version = '0.4',
          author = 'David Goodger',
          author_email = 'dgoodger@bigfoot.com',
          license = 'public domain',
          packages = ['dps.parsers.restructuredtext',
                      'dps.parsers.restructuredtext.directives'],
          package_dir = {'dps.parsers.restructuredtext': 'restructuredtext'})
    return dist

if __name__ == '__main__' :
    do_setup()
