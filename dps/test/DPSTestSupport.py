#! /usr/bin/env python
"""
:Author:  David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2001/09/17 04:04:07 $
:Copyright: This module has been placed in the public domain.

Exports the following:

:Modules:
    Try to import modules from the current working copy of dps
    first, or from the installed version. In test modules, import these modules
    from here:

    - `statemachine` is 'dps.statemachine'
    - `nodes` is 'dps.nodes'
    - `utils` is 'dps.utils'
"""
__docformat__ = 'reStructuredText'

import UnitTestFolder
import sys, os
#, unittest, re, difflib, types, inspect
#from pprint import pformat

# try to import the current working version if possible
sys.path.insert(0, os.pardir)           # running in test framework dir?
import dps                              # or restructuredtext on path?

from dps import statemachine, nodes, utils

try:
    import mypdb as pdb
except:
    import pdb
