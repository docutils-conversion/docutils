#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.23 $
:Date: $Date: 2002/01/28 02:18:45 $
:Copyright: This module has been placed in the public domain.

Classes in CamelCase are abstract base classes or auxiliary classes. The one
exception is `Text`, for a text node; uppercase is used to differentiate from
element classes.

Classes in lower_case_with_underscores are element classes, matching the XML
element generic identifiers in the DTD_.

.. _DTD: http://docstring.sourceforge.net/spec/gpdi.dtd
"""

import sys
import xml.dom.minidom
from types import IntType, SliceType, StringType, TupleType
from UserString import MutableString

# ==============================
#  Functional Node Base Classes
# ==============================

class Node:

    """Abstract base class of nodes in a document tree."""

    def __nonzero__(self):
        """Node instances are always true."""
        return 1

    def asdom(self, dom=xml.dom.minidom):
        return self._dom_node(dom)

    def walk(self, visitor, ancestry=()):
        """
        Traverse a tree of `Node` objects, calling ``visit_*`` methods of
        `visitor`.

        Parameters:

        - `visitor`: A `Visitor` object, containing a ``visit_...`` method for
          each `Node` subclass encountered.
        - `ancestry`: A list of (parent, index) pairs. `self`'s parent is the
          last entry.
        """
        method = getattr(visitor, 'visit_' + self.__class__.__name__)
        method(self, ancestry)
        children = self.getchildren()
        for i in range(len(children)):
            children[i].walk(visitor, ancestry + ((self, i),))


class Text(Node, MutableString):

    tagname = '#text'

    def __repr__(self):
        data = repr(self.data)
        if len(data) > 70:
            data = repr(self.data[:64] + ' ...')
        return '<%s: %s>' % (self.tagname, data)

    def shortrepr(self):
        data = repr(self.data)
        if len(data) > 20:
            data = repr(self.data[:16] + ' ...')
        return '<%s: %s>' % (self.tagname, data)

    def _dom_node(self, dom):
        return dom.Text(self.data)

    def _rooted_dom_node(self, domroot):
        return domroot.createTextNode(self.data)

    def astext(self):
        return self.data

    def pformat(self, indent='    ', level=0):
        result = []
        indent = indent * level
        for line in self.data.splitlines():
            result.append(indent + line + '\n')
        return ''.join(result)

    def getchildren(self):
        """Text nodes have no children. Return []."""
        return []


class Element(Node):

    """
    `Element` is the superclass to all specific elements.

    Elements contain attributes and child nodes. Elements emulate dictionaries
    for attributes, indexing by attribute name (a string). To set the
    attribute 'att' to 'value', do::

        element['att'] = 'value'

    Elements also emulate lists for child nodes (element nodes and/or text
    nodes), indexing by integer. To get the first child node, use::

        element[0]

    Elements may be constructed using the ``+=`` operator. To add one new
    child node to element, do::

        element += node

    To add a list of multiple child nodes at once, use the same ``+=``
    operator::

        element += [node1, node2]
    """

    tagname = None
    """The element generic identifier. If None, it is set as an instance
    attribute to the name of the class."""

    child_text_separator = '\n\n'
    """Separator for child nodes, used by `astext()` method."""

    def __init__(self, rawsource='', *children, **attributes):
        self.rawsource = rawsource
        """The raw text from which this element was constructed."""

        self.children = list(children)
        """List of child nodes (elements and/or text)."""

        self.attributes = attributes
        """Dictionary of attribute {name: value}."""

        if self.tagname is None:
            self.tagname = self.__class__.__name__

    def _dom_node(self, dom):
        element = dom.Element(self.tagname)
        for attribute, value in self.attributes.items():
            element.setAttribute(attribute, str(value))
        for child in self.children:
            element.appendChild(child._dom_node(dom))
        return element

    def _rooted_dom_node(self, domroot):
        element = domroot.createElement(self.tagname)
        for attribute, value in self.attributes.items():
            element.setAttribute(attribute, str(value))
        for child in self.children:
            element.appendChild(child._rooted_dom_node(domroot))
        return element

    def __repr__(self):
        data = ''
        for c in self.children:
            data += c.shortrepr()
            if len(data) > 60:
                data = data[:56] + ' ...'
                break
        if self.hasattr('name'):
            return '<%s "%s": %s>' % (self.__class__.__name__,
                                      self.attributes['name'], data)
        else:
            return '<%s: %s>' % (self.__class__.__name__, data)

    def shortrepr(self):
        if self.hasattr('name'):
            return '<%s "%s"...>' % (self.__class__.__name__,
                                      self.attributes['name'])
        else:
            return '<%s...>' % self.tagname

    def __str__(self):
        if self.children:
            return '%s%s%s' % (self.starttag(),
                                ''.join([str(c) for c in self.children]),
                                self.endtag())
        else:
            return self.emptytag()

    def starttag(self):
        return '<%s>' % ' '.join([self.tagname] +
                                 ['%s="%s"' % (n, v)
                                  for n, v in self.attlist()])

    def endtag(self):
        return '</%s>' % self.tagname

    def emptytag(self):
        return '<%s/>' % ' '.join([self.tagname] +
                                  ['%s="%s"' % (n, v)
                                   for n, v in self.attlist()])

    def __len__(self):
        return len(self.children)

    def __getitem__(self, key):
        if isinstance(key, StringType):
            return self.attributes[key]
        elif isinstance(key, IntType):
            return self.children[key]
        elif isinstance(key, SliceType):
            assert key.step is None, 'cannot handle slice with stride'
            return self.children[key.start:key.stop]
        else:
            raise TypeError, ('element index must be an integer, a slice, or '
                              'an attribute name string')

    def __setitem__(self, key, item):
        if isinstance(key, StringType):
            self.attributes[key] = item
        elif isinstance(key, IntType):
            self.children[key] = item
        elif isinstance(key, SliceType):
            assert key.step is None, 'cannot handle slice with stride'
            self.children[key.start:key.stop] = item
        else:
            raise TypeError, ('element index must be an integer, a slice, or '
                              'an attribute name string')

    def __delitem__(self, key):
        if isinstance(key, StringType):
            del self.attributes[key]
        elif isinstance(key, IntType):
            del self.children[key]
        elif isinstance(key, SliceType):
            assert key.step is None, 'cannot handle slice with stride'
            del self.children[key.start:key.stop]
        else:
            raise TypeError, ('element index must be an integer, a simple '
                              'slice, or an attribute name string')

    def __add__(self, other):
        return self.children + other

    def __radd__(self, other):
        return other + self.children

    def __iadd__(self, other):
        """Append a node or a list of nodes to `self.children`."""
        if isinstance(other, Node):
            self.children.append(other)
        elif other is not None:
            self.children.extend(other)
        return self

    def astext(self):
        return self.child_text_separator.join(
              [child.astext() for child in self.children])

    def attlist(self):
        attlist = self.attributes.items()
        attlist.sort()
        return attlist

    def get(self, key, failobj=None):
        return self.attributes.get(key, failobj)

    def hasattr(self, attr):
        return self.attributes.has_key(attr)

    has_key = hasattr

    def append(self, item):
        assert isinstance(item, Node)
        self.children.append(item)

    def extend(self, item):
        self.children.extend(item)

    def insert(self, i, item):
        assert isinstance(item, Node)
        self.children.insert(i, item)

    def pop(self, i=-1):
        return self.children.pop(i)

    def remove(self, item):
        assert isinstance(item, Node)
        self.children.remove(item)

    def findclass(self, childclass, start=0, end=sys.maxint):
        """
        Return the index of the first child whose class exactly matches.

        Parameters:

        - `childclass`: A `Node` subclass to search for, or a tuple of `Node`
          classes. If a tuple, any of the classes may match.
        - `start`: Initial index to check.
        - `end`: Initial index to *not* check.
        """
        if not isinstance(childclass, TupleType):
            childclass = (childclass,)
        for index in range(start, min(len(self), end)):
            for c in childclass:
                if isinstance(self[index], c):
                    return index
        return None

    def findnonclass(self, childclass, start=0, end=sys.maxint):
        """
        Return the index of the first child whose class does *not* match.

        Parameters:

        - `childclass`: A `Node` subclass to skip, or a tuple of `Node`
          classes. If a tuple, none of the classes may match.
        - `start`: Initial index to check.
        - `end`: Initial index to *not* check.
        """
        if not isinstance(childclass, TupleType):
            childclass = (childclass,)
        for index in range(start, min(len(self), end)):
            match = 0
            for c in childclass:
                if isinstance(self.children[index], c):
                    match = 1
            if not match:
                return index
        return None

    def pformat(self, indent='    ', level=0):
        return ''.join(['%s%s\n' % (indent * level, self.starttag())] +
                       [child.pformat(indent, level+1)
                        for child in self.children])

    def getchildren(self):
        """Return this element's children."""
        return self.children


class TextElement(Element):

    """
    An element which directly contains text.

    Its children are all Text or TextElement nodes.
    """

    child_text_separator = ''
    """Separator for child nodes, used by `astext()` method."""

    def __init__(self, rawsource='', text='', *children, **attributes):
        if text != '':
            textnode = Text(text)
            Element.__init__(self, rawsource, textnode, *children,
                              **attributes)
        else:
            Element.__init__(self, rawsource, *children, **attributes)


# ========
#  Mixins
# ========

class ToBeResolved:

    resolved = 0


# ====================
#  Element Categories
# ====================

class Root: pass

class Title: pass

class Bibliographic: pass

class Structural: pass

class Body: pass

class General(Body): pass

class List(Body): pass

class Admonition(Body): pass

class Special(Body): pass

class Component: pass

class Inline: pass


class Reference(ToBeResolved):

    refnode = None
    """Resolved reference to a node."""


# ==============
#  Root Element
# ==============

class document(Root, Element):

    def __init__(self, reporter, languagecode, *args, **kwargs):
        Element.__init__(self, *args, **kwargs)

        self.reporter = reporter
        """System warning generator."""

        self.languagecode = languagecode
        """ISO 639 2-letter language identifier."""

        self.explicit_targets = {}
        """Mapping of target names to lists of explicit target nodes."""

        self.implicit_targets = {}
        """Mapping of target names to lists of implicit (internal) target
        nodes."""

        self.external_targets = {}
        """Mapping of target names to lists of external target nodes."""

        self.indirect_targets = {}
        """Mapping of target names to indirect target nodes."""

        self.substitution_defs = {}
        """Mapping of substitution names to substitution_definition nodes."""

        self.refnames = {}
        """Mapping of reference names to reference nodes."""

        self.substitution_refs = {}
        """Mapping of substitution names to substitution_reference nodes."""

        self.footnote_refs = {}
        """Mapping of footnote labels to footnote_reference nodes."""

        self.anonymous_targets = []
        """List of anonymous target nodes."""

        self.anonymous_refs = []
        """List of anonymous reference nodes."""

        self.autofootnotes = []
        """List of auto-numbered footnote nodes."""

        self.autofootnote_refs = []
        """List of auto-numbered footnote_reference nodes."""

        self.anonymous_start = 1
        """Initial anonymous hyperlink number."""

        self.autofootnote_start = 1
        """Initial auto-numbered footnote number."""

    def asdom(self, dom=xml.dom.minidom):
        domroot = dom.Document()
        domroot.appendChild(Element._rooted_dom_node(self, domroot))
        return domroot

    def note_implicit_target(self, targetnode, innode=None):
        if innode == None:
            innode = self
        name = targetnode['name']
        if self.explicit_targets.has_key(name) \
              or self.external_targets.has_key(name) \
              or self.implicit_targets.has_key(name):
            sw = self.reporter.information(
                  'Duplicate implicit target name: "%s"' % name)
            innode += sw
            self.clear_target_names(name, self.implicit_targets)
            del targetnode['name']
            targetnode['dupname'] = name
        self.implicit_targets.setdefault(name, []).append(targetnode)

    def note_explicit_target(self, targetnode, innode=None):
        if innode == None:
            innode = self
        name = targetnode['name']
        if self.explicit_targets.has_key(name):
            level = 1
            if targetnode.has_key('refuri'): # external target, dups OK
                refuri = targetnode['refuri']
                for t in self.explicit_targets.get(name, []):
                    if not t.has_key('refuri') or t['refuri'] != refuri:
                        break
                else:
                    level = 0           # just inform if refuri's identical
            sw = self.reporter.system_warning(
                  level, 'Duplicate explicit target name: "%s"' % name)
            innode += sw
            self.clear_target_names(name, self.explicit_targets,
                                    self.implicit_targets)
            if level > 0:
                del targetnode['name']
                targetnode['dupname'] = name
        elif self.implicit_targets.has_key(name):
            sw = self.reporter.information(
                  'Duplicate implicit target name: "%s"' % name)
            innode += sw
            self.clear_target_names(name, self.implicit_targets)
        self.explicit_targets.setdefault(name, []).append(targetnode)

    def clear_target_names(self, name, *targetdicts):
        for targetdict in targetdicts:
            for node in targetdict.get(name, []):
                if node.has_key('name'):
                    node['dupname'] = node['name']
                    del node['name']

    def note_refname(self, node):
        self.refnames.setdefault(node['refname'], []).append(node)

    def note_external_target(self, targetnode):
        self.external_targets.setdefault(
              targetnode['name'], []).append(targetnode)

    def note_indirect_target(self, targetnode):
        self.indirect_targets.setdefault(
              targetnode['name'], []).append(targetnode)
        self.note_refname(targetnode)

    def note_anonymous_target(self, targetnode):
        self.anonymous_targets.append(targetnode)

    def note_anonymous_ref(self, refnode):
        self.anonymous_refs.append(refnode)

    def note_autofootnote(self, footnotenode):
        self.autofootnotes.append(footnotenode)

    def note_autofootnote_ref(self, refnode):
        self.autofootnote_refs.append(refnode)

    def note_footnote_ref(self, refnode):
        self.footnote_refs.setdefault(refnode['refname'], []).append(refnode)
        self.note_refname(refnode)

    def note_substitution_def(self, substitutiondefnode, innode=None):
        if innode == None:
            innode = self
        name = substitutiondefnode['name']
        if self.substitution_defs.has_key(name):
            sw = self.reporter.error(
                  'Duplicate substitution definition name: "%s"' % name)
            innode += sw
            oldnode = self.substitution_defs[name]
            oldnode['dupname'] = oldnode['name']
            del oldnode['name']
        # keep only the last definition
        self.substitution_defs[name] = substitutiondefnode

    def note_substitution_ref(self, subrefnode):
        self.substitution_refs.setdefault(
              subrefnode['refname'], []).append(subrefnode)


# ================
#  Title Elements
# ================

class title(Title, TextElement): pass
class subtitle(Title, TextElement): pass


# ========================
#  Bibliographic Elements
# ========================

class docinfo(Bibliographic, Element): pass
class author(Bibliographic, TextElement): pass
class authors(Bibliographic, Element): pass
class organization(Bibliographic, TextElement): pass
class contact(Bibliographic, TextElement): pass
class version(Bibliographic, TextElement): pass
class revision(Bibliographic, TextElement): pass
class status(Bibliographic, TextElement): pass
class date(Bibliographic, TextElement): pass
class copyright(Bibliographic, TextElement): pass
class abstract(Bibliographic, Element): pass


# =====================
#  Structural Elements
# =====================

class section(Structural, Element): pass
class transition(Structural, Element): pass


# ===============
#  Body Elements
# ===============

class paragraph(General, TextElement): pass
class bullet_list(List, Element): pass
class enumerated_list(List, Element): pass
class list_item(Component, Element): pass
class definition_list(List, Element): pass
class definition_list_item(Component, Element): pass
class term(Component, TextElement): pass
class classifier(Component, TextElement): pass
class definition(Component, Element): pass
class field_list(List, Element): pass
class field(Component, Element): pass
class field_name(Component, TextElement): pass
class field_argument(Component, TextElement): pass
class field_body(Component, Element): pass
class option_list(List, Element): pass
class option_list_item(Component, Element): pass
class option(Component, Element): pass
class short_option(Component, TextElement): pass
class long_option(Component, TextElement): pass
class vms_option(Component, TextElement): pass
class option_argument(Component, TextElement): pass
class description(Component, Element): pass
class literal_block(General, TextElement): pass
class block_quote(General, Element): pass
class doctest_block(General, TextElement): pass
class attention(Admonition, Element): pass
class caution(Admonition, Element): pass
class danger(Admonition, Element): pass
class error(Admonition, Element): pass
class important(Admonition, Element): pass
class note(Admonition, Element): pass
class tip(Admonition, Element): pass
class hint(Admonition, Element): pass
class warning(Admonition, Element): pass
class comment(Special, TextElement): pass
class substitution_definition(Special, TextElement): pass
class target(Special, Inline, TextElement, ToBeResolved): pass
class footnote(General, Element): pass
class label(Component, TextElement): pass
class figure(General, Element): pass
class caption(Component, TextElement): pass
class legend(Component, Element): pass
class table(General, Element): pass
class tgroup(Component, Element): pass
class colspec(Component, Element): pass
class thead(Component, Element): pass
class tbody(Component, Element): pass
class row(Component, Element): pass
class entry(Component, Element): pass


class system_warning(Special, Element):

    def __init__(self, comment=None, *children, **attributes):
        #print ('nodes.system_warning.__init__: comment=%r, children=%r, '
        #       'attributes=%r' % (comment, children, attributes))
        if comment:
            p = paragraph('', comment)
            children = (p,) + children
        Element.__init__(self, '', *children, **attributes)

    def astext(self):
        return '[level %s] ' % self['level'] + Element.astext(self)


# =================
#  Inline Elements
# =================

class emphasis(Inline, TextElement): pass
class strong(Inline, TextElement): pass
class interpreted(Inline, Reference, TextElement): pass
class literal(Inline, TextElement): pass
class reference(Inline, Reference, TextElement): pass
class footnote_reference(Inline, Reference, TextElement): pass
class substitution_reference(Inline, Reference, TextElement): pass
class image(General, Inline, TextElement): pass


# ========================================
#  Auxiliary Classes, Functions, and Data
# ========================================

node_class_names = """
    Text
    abstract attention author authors
    block_quote bullet_list
    caption caution classifier colspec comment contact copyright
    danger date definition definition_list definition_list_item
        description docinfo doctest_block document
    emphasis entry enumerated_list error
    field field_argument field_body field_list field_name figure
        footnote footnote_reference
    hint
    image important interpreted
    label legend list_item literal literal_block long_option
    note
    option option_argument option_list option_list_item organization
    paragraph
    reference revision row
    section short_option status strong substitution_definition
        substitution_reference subtitle system_warning
    table target tbody term tgroup thead tip title transition
    version vms_option
    warning""".split()
"""A list of names of all concrete Node subclasses."""


class Visitor:

    """
    "Visitor" pattern [GoF95]_ abstract superclass implementation for document
    tree traversals.

    Each node class has corresponding methods, doing nothing by default;
    override individual methods for specific and useful behaviour. The
    "``visit_`` + node class name" method is called by `Node.walk()` upon
    entering a node.
    
    .. [GoF95] Gamma, Helm, Johnson, Vlissides. *Design Patterns: Elements of
       Reusable Object-Oriented Software*. Addison-Wesley, Reading, MA, USA,
       1995.
    """

    def __init__(self, doctree):
        self.doctree = doctree

    def walk(self):
        self.doctree.walk(self)

    # Save typing with dynamic definitions.
    for name in node_class_names:
        exec """def visit_%s(self, node, ancestry): pass\n""" % name
    del name


class GenericVisitor(Visitor):

    """
    Generic "Visitor" abstract superclass, for simple traversals.

    Unless overridden, each ``visit_*`` method calls `default_visit()`.
    ``default_visit()`` must be overridden in subclasses.

    Define fully generic visitors by overriding ``default_visit()`` only.
    Define semi-generic visitors by overriding individual ``visit_*()``
    methods also.
    """

    def default_visit(self, node, ancestry):
        """Override for generic, uniform traversals."""
        raise NotImplementedError

    # Save typing with dynamic definitions.
    for name in node_class_names:
        exec """def visit_%s(self, node, ancestry):
                    self.default_visit(node, ancestry)\n""" % name
    del name
