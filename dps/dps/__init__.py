#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2002/02/06 02:41:37 $
:Copyright: This module has been placed in the public domain.

This is the Docstring Processing System (DPS) Python package. 

Package Structure
=================

Modules:

- __init__.py: Contains the package docstring only (this text).

- core.py: Contains the ``Publisher`` class and ``convert()`` function.

- nodes.py: DPS document tree (doctree) node class library.

- roman.py: Conversion to and from Roman numerals. Courtesy of Mark
  Pilgrim (http://diveintopython.org/).

- statemachine.py: A finite state machine specialized for
  regular-expression-based text filters.

- urischemes.py: Contains a complete mapping of known URI addressing
  scheme names to descriptions.

- utils.py: Miscellaneous utilities.

Subpackages:

- languages: Language-specific mappings of terms.

- parsers: Syntax-specific input parser modules or packages.

- readers: Context-specific input handlers which understand the data
  source and manage a parser.

- transforms: Modules used by readers and writers to modify DPS
  doctrees.

- writers: Format-specific output translators.
"""

__docformat__ = 'reStructuredText'
