#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.5 $
:Date: $Date: 2002/01/16 02:50:12 $
:Copyright: This module has been placed in the public domain.

English-language mappings for language-dependent features of the Python
Docstring Processing System.
"""

__docformat__ = 'reStructuredText'

__all__ = ['interpreted', 'bibliographic_labels', 'bibliographic_fields',
           'author_separators']


from dps import nodes


interpreted = {
      'package': nodes.package,
      'module': nodes.module,
      'class': nodes.inline_class,
      'method': nodes.method,
      'function': nodes.function,
      'variable': nodes.variable,
      'parameter': nodes.parameter,
      'type': nodes.type,
      'class attribute': nodes.class_attribute,
      'classatt': nodes.class_attribute,
      'instance attribute': nodes.instance_attribute,
      'instanceatt': nodes.instance_attribute,
      'module attribute': nodes.module_attribute,
      'moduleatt': nodes.module_attribute,
      'exception class': nodes.exception_class,
      'exception': nodes.exception_class,
      'warning class': nodes.warning_class,
      'warning': nodes.warning_class,}
"""Mapping of interpreted text role name to nodes.py class."""

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
