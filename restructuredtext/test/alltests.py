#!/usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2001/09/02 13:50:48 $
:Copyright: This module has been placed in the public domain.
"""

import time
start = time.time()

import sys, os


class Tee:

    """Write to a file and a stream (default: stdout) simultaneously."""
    
    def __init__(self, filename, stream=sys.__stdout__):
        self.file = open(filename, 'w')
        self.stream = stream
    
    def write(self, string):
        self.stream.write(string)
        self.file.write(string)

# must redirect stderr *before* first import of unittest
sys.stdout = sys.stderr = Tee('alltests.out')

import UnitTestFolder


if __name__ == '__main__':
    path, script = os.path.split(sys.argv[0])
    suite = UnitTestFolder.loadModulesFromFolder(path, 'test_', subfolders=1)
    UnitTestFolder.main(suite)
    finish = time.time()
    print 'Elapsed time: %s seconds' % (finish - start)
