#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.7 $
:Date: $Date: 2002/02/06 02:41:54 $
:Copyright: This module has been placed in the public domain.

English-language mappings for language-dependent features of the Python
Docstring Processing System.
"""

__docformat__ = 'reStructuredText'

__all__ = ['bibliographic_labels', 'bibliographic_fields', 'author_separators']


from dps import nodes


bibliographic_labels = {
      'author': 'Author',
      'authors': 'Authors',
      'organization': 'Organization',
      'contact': 'Contact',
      'version': 'Version',
      'revision': 'Revision',
      'status': 'Status',
      'date': 'Date',
      'copyright': 'Copyright',
      'abstract': 'Abstract'}
"""Mapping of bibliographic node class name to label text."""

bibliographic_fields = {
      'author': nodes.author,
      'authors': nodes.authors,
      'organization': nodes.organization,
      'contact': nodes.contact,
      'version': nodes.version,
      'revision': nodes.revision,
      'status': nodes.status,
      'date': nodes.date,
      'copyright': nodes.copyright,
      'abstract': nodes.abstract}
"""Field name (lowcased) to node class name mapping for bibliographic fields
(field_list)."""

author_separators = [';', ',']
"""List of separator strings for the 'Authors' bibliographic field. Tried in
order."""
