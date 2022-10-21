#! /usr/bin/env python3

# $Id$
# Author: Garth Kidd <garth@deadlybloodyserious.com>
# Copyright: This module has been placed in the public domain.

"""
This module extends unittest.py with `loadTestModules()`, by loading multiple
test modules from a directory.  Optionally, test packages are also loaded,
recursively.
"""

import sys
import os
import types
import unittest
from importlib import import_module


# So that individual test modules can share a bit of state,
# `package_unittest` acts as an intermediary for the following
# variables:
debug = False
verbosity = 1


def loadTestModules(path, name='', packages=None):
    """
    Return a test suite composed of all the tests from modules in a directory.

    Search for modules in directory `path`, beginning with `name`. If
    `packages` is true, search subdirectories (also beginning with `name`)
    recursively.  Subdirectories must be Python packages; they must contain an
    '__init__.py' module.
    """
    testLoader = unittest.defaultTestLoader
    testSuite = unittest.TestSuite()
    testModules = []
    path = os.path.abspath(path)        # current working dir if `path` empty
    paths = [path]
    while paths:
        p = paths.pop(0)
        files = os.listdir(p)
        for filename in files:
            if not filename.startswith(name):
                continue
            fullpath = os.path.join(p, filename)
            if filename.endswith('.py'):
                fullpath = fullpath[len(path)+1:]
                testModules.append(path2mod(fullpath))
            elif (packages and os.path.isdir(fullpath)
                  and os.path.isfile(os.path.join(fullpath, '__init__.py'))):
                paths.append(fullpath)
# Import modules and add their tests to the suite.
    sys.path.insert(0, path)
    for mod in testModules:
        try:
            module = import_module(mod)
        except ImportError:
            print(f"ERROR: Can't import {mod}, skipping its tests:",
                  file=sys.stderr)
            sys.excepthook(*sys.exc_info())
        else:
            # if there's a suite defined, incorporate its contents
            try:
                suite = getattr(module, 'suite')
            except AttributeError:
                # Look for individual tests
                moduleTests = testLoader.loadTestsFromModule(module)
                # unittest.TestSuite.addTests() doesn't work as advertised,
                # as it can't load tests from another TestSuite, so we have
                # to cheat:
                testSuite.addTest(moduleTests)
                continue
            if isinstance(suite, types.FunctionType):
                testSuite.addTest(suite())
            elif isinstance(suite, unittest.TestSuite):
                testSuite.addTest(suite)
            else:
                raise AssertionError("don't understand suite (%s)" % mod)
    sys.path.pop(0)
    return testSuite


def path2mod(path):
    """Convert a file path to a dotted module name."""
    return path[:-3].replace(os.sep, '.')
