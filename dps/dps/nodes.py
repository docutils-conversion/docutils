#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.34 $
:Date: $Date: 2002/03/04 04:47:06 $
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

    parent = None
    """Back-reference to the `Node` containing this `Node`."""

    def __nonzero__(self):
        """Node instances are always true."""
        return 1

    def asdom(self, dom=xml.dom.minidom):
        return self._dom_node(dom)

    def walk(self, visitor):
        """
        Traverse a tree of `Node` objects, calling ``visit_...`` methods of
        `visitor` when entering each node. If there is no
        ``visit_particular_node`` method for a node of type
        ``particular_node``, the ``unknown_visit`` method is called.

        Doesn't handle arbitrary modification in-place during the traversal.
        Replacing one element with one element is OK.

        Parameter `visitor`: A `NodeVisitor` object, containing a
        ``visit_...`` method for each `Node` subclass encountered.
        """
        name = 'visit_' + self.__class__.__name__
        method = getattr(visitor, name, visitor.unknown_visit)
        visitor.doctree.reporter.debug(name, category='nodes.Node.walk')
        try:
            method(self)
            children = self.getchildren()
            try:
                for i in range(len(children)):
                    children[i].walk(visitor)
            except SkipSiblings:
                pass
        except (SkipChildren, SkipNode):
            pass

    def walkabout(self, visitor):
        """
        Perform a tree traversal similarly to `Node.walk()`, except also call
        ``depart_...`` methods before exiting each node. If there is no
        ``depart_particular_node`` method for a node of type
        ``particular_node``, the ``unknown_departure`` method is called.

        Parameter `visitor`: A `NodeVisitor` object, containing ``visit_...``
        and ``depart_...`` methods for each `Node` subclass encountered.
        """
        name = 'visit_' + self.__class__.__name__
        method = getattr(visitor, name, visitor.unknown_visit)
        visitor.doctree.reporter.debug(name, category='nodes.Node.walkabout')
        try:
            method(self)
            children = self.getchildren()
            try:
                for i in range(len(children)):
                    children[i].walkabout(visitor)
            except SkipSiblings:
                pass
        except SkipChildren:
            pass
        except SkipNode:
            return
        name = 'depart_' + self.__class__.__name__
        method = getattr(visitor, name, visitor.unknown_departure)
        visitor.doctree.reporter.debug(name, category='nodes.Node.walkabout')
        method(self)


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

        self.children = []
        """List of child nodes (elements and/or `Text`)."""

        self.extend(children)           # extend self.children w/ attributes

        self.attributes = {}
        """Dictionary of attribute {name: value}."""

        for att, value in attributes.items():
            self.attributes[att.lower()] = value

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
            item.parent = self
            self.children[key] = item
        elif isinstance(key, SliceType):
            assert key.step is None, 'cannot handle slice with stride'
            for node in item:
                node.parent = self
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
            other.parent = self
            self.children.append(other)
        elif other is not None:
            for node in other:
                node.parent = self
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
        item.parent = self
        self.children.append(item)

    def extend(self, item):
        for node in item:
            node.parent = self
        self.children.extend(item)

    def insert(self, i, item):
        assert isinstance(item, Node)
        item.parent = self
        self.children.insert(i, item)

    def pop(self, i=-1):
        return self.children.pop(i)

    def remove(self, item):
        self.children.remove(item)

    def index(self, item):
        return self.children.index(item)

    def replace(self, old, new):
        """Replace one child `Node` with another child or children."""
        index = self.index(old)
        if isinstance(new, Node):
            self[index] = new
        elif new is not None:
            self[index:index+1] = new

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

class Titular: pass

class Bibliographic: pass


class PreBibliographic:
    """Category of Node which may occur before Bibliographic Nodes."""
    pass


class Structural: pass

class Body: pass

class General(Body): pass

class Sequential(Body): pass

class Admonition(Body): pass


class Special(Body):
    """Special internal body elements, not true document components."""
    pass


class Component: pass

class Inline: pass


class Referential(ToBeResolved):

    refnode = None
    """Resolved reference to a node."""


# ==============
#  Root Element
# ==============

class document(Root, Element):

    def __init__(self, reporter, languagecode, *args, **kwargs):
        Element.__init__(self, *args, **kwargs)

        self.reporter = reporter
        """System message generator."""

        self.languagecode = languagecode
        """ISO 639 2-letter language identifier."""

        self.explicit_targets = {}
        """Mapping of target names to explicit target nodes."""

        self.implicit_targets = {}
        """Mapping of target names to implicit (internal) target
        nodes."""

        self.external_targets = {}
        """Mapping of target names to external target nodes."""

        self.indirect_targets = {}
        """Mapping of target names to indirect target nodes."""

        self.substitution_defs = {}
        """Mapping of substitution names to substitution_definition nodes."""

        self.refnames = {}
        """Mapping of reference names to lists of reference nodes."""

        self.nameids = {}
        """Mapping of names to unique id's."""

        self.ids = {}
        """Mapping of ids to nodes."""

        self.substitution_refs = {}
        """Mapping of substitution names to lists of substitution_reference
        nodes."""

        self.footnote_refs = {}
        """Mapping of footnote labels to lists of footnote_reference nodes."""

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

        self.id_start = 1
        """Initial ID number."""

        self.messages = Element()
        """System messages generated after parsing."""

    def asdom(self, dom=xml.dom.minidom):
        domroot = dom.Document()
        domroot.appendChild(Element._rooted_dom_node(self, domroot))
        return domroot

    def set_id(self, node, msgnode=None):
        if msgnode == None:
            msgnode = self.messages
        if node.has_key('id'):
            id = node['id']
            if self.ids.has_key(id) and self.ids[id] is not node:
                msg = self.reporter.error('Duplicate ID: "%s"' % id)
                msgnode += msg
        else:
            while 1:
                id = 'id%s' % self.id_start
                self.id_start += 1
                if not self.ids.has_key(id):
                    break
            node['id'] = id
        self.ids[id] = node
        if node.has_key('name'):
            name = node['name']
            if self.nameids.has_key(name) \
                  and self.ids[self.nameids[name]].has_key('name'):
                msg = self.reporter.info(
                      'Multiple IDs for name "%s": "%s", "%s"'
                      % (name, self.nameids[name], id))
                msgnode += msg
            self.nameids[name] = id

    def note_implicit_target(self, targetnode, msgnode=None):
        if msgnode == None:
            msgnode = self.messages
        name = targetnode['name']
        if self.explicit_targets.has_key(name) \
              or self.external_targets.has_key(name) \
              or self.implicit_targets.has_key(name):
            msg = self.reporter.info(
                  'Duplicate implicit target name: "%s"' % name)
            msgnode += msg
            self.clear_target_names(name, self.implicit_targets)
            del targetnode['name']
            targetnode['dupname'] = name
        self.implicit_targets[name] = targetnode
        self.set_id(targetnode, msgnode)

    def note_explicit_target(self, targetnode, msgnode=None):
        if msgnode == None:
            msgnode = self.messages
        name = targetnode['name']
        if self.explicit_targets.has_key(name):
            level = 2
            if targetnode.has_key('refuri'): # external target, dups OK
                refuri = targetnode['refuri']
                t = self.explicit_targets[name]
                if t.has_key('name') and t.has_key('refuri') \
                      and t['refuri'] == refuri:
                    level = 1           # just inform if refuri's identical
            msg = self.reporter.system_message(
                  level, 'Duplicate explicit target name: "%s"' % name)
            msgnode += msg
            self.clear_target_names(name, self.explicit_targets,
                                    self.implicit_targets)
            if level > 1:
                del targetnode['name']
                targetnode['dupname'] = name
        elif self.implicit_targets.has_key(name):
            msg = self.reporter.info(
                  'Duplicate implicit target name: "%s"' % name)
            msgnode += msg
            self.clear_target_names(name, self.implicit_targets)
        self.explicit_targets[name] = targetnode
        self.set_id(targetnode, msgnode)

    def clear_target_names(self, name, *targetdicts):
        for targetdict in targetdicts:
            if not targetdict.has_key(name):
                continue
            node = targetdict[name]
            if node.has_key('name'):
                node['dupname'] = node['name']
                del node['name']

    def note_refname(self, node):
        self.refnames.setdefault(node['refname'], []).append(node)

    def note_external_target(self, targetnode):
        self.external_targets[targetnode['name']] = targetnode

    def note_indirect_target(self, targetnode):
        self.indirect_targets[targetnode['name']] = targetnode
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

    def note_substitution_def(self, substitutiondefnode, msgnode=None):
        name = substitutiondefnode['name']
        if self.substitution_defs.has_key(name):
            msg = self.reporter.error(
                  'Duplicate substitution definition name: "%s"' % name)
            if msgnode == None:
                msgnode = self.messages
            msgnode += msg
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

class title(Titular, PreBibliographic, TextElement): pass
class subtitle(Titular, PreBibliographic, TextElement): pass


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


# =====================
#  Structural Elements
# =====================

class section(Structural, Element): pass
class topic(Structural, Element): pass
class transition(Structural, Element): pass


# ===============
#  Body Elements
# ===============

class paragraph(General, TextElement): pass
class bullet_list(Sequential, Element): pass
class enumerated_list(Sequential, Element): pass
class list_item(Component, Element): pass
class definition_list(Sequential, Element): pass
class definition_list_item(Component, Element): pass
class term(Component, TextElement): pass
class classifier(Component, TextElement): pass
class definition(Component, Element): pass
class field_list(Sequential, Element): pass
class field(Component, Element): pass
class field_name(Component, TextElement): pass
class field_argument(Component, TextElement): pass
class field_body(Component, Element): pass


class option(Component, Element):

    child_text_separator = ''


class option_argument(Component, TextElement):

    def astext(self):
        return self.get('delimiter', ' ') + TextElement.astext(self)


class option_group(Component, Element):

    child_text_separator = ', '


class option_list(Sequential, Element): pass


class option_list_item(Component, Element):

    child_text_separator = '  '


class option_string(Component, TextElement): pass
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
class comment(Special, PreBibliographic, TextElement): pass
class substitution_definition(Special, TextElement): pass
class target(Special, Inline, TextElement, ToBeResolved): pass
class footnote(General, Element): pass
class citation(General, Element): pass
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


class system_message(Special, PreBibliographic, Element):

    def __init__(self, comment=None, *children, **attributes):
        if comment:
            p = paragraph('', comment)
            children = (p,) + children
        Element.__init__(self, '', *children, **attributes)

    def astext(self):
        return '%s (%s) %s' % (self['type'], self['level'],
                               Element.astext(self))


# =================
#  Inline Elements
# =================

class emphasis(Inline, TextElement): pass
class strong(Inline, TextElement): pass
class interpreted(Inline, Referential, TextElement): pass
class literal(Inline, TextElement): pass
class reference(Inline, Referential, TextElement): pass
class footnote_reference(Inline, Referential, TextElement): pass
class citation_reference(Inline, Referential, TextElement): pass
class substitution_reference(Inline, Referential, TextElement): pass
class image(General, Inline, TextElement): pass
class problematic(Inline, TextElement): pass


# ========================================
#  Auxiliary Classes, Functions, and Data
# ========================================

node_class_names = """
    Text
    attention author authors
    block_quote bullet_list
    caption caution citation citation_reference classifier colspec
        comment contact copyright
    danger date definition definition_list definition_list_item
        description docinfo doctest_block document
    emphasis entry enumerated_list error
    field field_argument field_body field_list field_name figure
        footnote footnote_reference
    hint
    image important interpreted
    label legend list_item literal literal_block
    note
    option option_argument option_group option_list option_list_item
        option_string organization
    paragraph problematic
    reference revision row
    section status strong substitution_definition
        substitution_reference subtitle system_message
    table target tbody term tgroup thead tip title topic transition
    version
    warning""".split()
"""A list of names of all concrete Node subclasses."""


class NodeVisitor:

    """
    "Visitor" pattern [GoF95]_ abstract superclass implementation for document
    tree traversals.

    Each node class has corresponding methods, doing nothing by default;
    override individual methods for specific and useful behaviour. The
    "``visit_`` + node class name" method is called by `Node.walk()` upon
    entering a node. `Node.walkabout()` also calls the "``depart_`` + node
    class name" method before exiting a node.

    .. [GoF95] Gamma, Helm, Johnson, Vlissides. *Design Patterns: Elements of
       Reusable Object-Oriented Software*. Addison-Wesley, Reading, MA, USA,
       1995.
    """

    def __init__(self, doctree):
        self.doctree = doctree

    def unknown_visit(self, node):
        """
        Called when entering unknown `Node` types.

        Raise an exception unless overridden.
        """
        raise NotImplementedError('visiting unknown node type: %s'
                                  % node.__class__.__name__)

    def unknown_departure(self, node):
        """
        Called before exiting unknown `Node` types.

        Raise exception unless overridden.
        """
        raise NotImplementedError('departing unknown node type: %s'
                                  % node.__class__.__name__)

    # Save typing with dynamic definitions.
    for name in node_class_names:
        exec """def visit_%s(self, node): pass\n""" % name
        exec """def depart_%s(self, node): pass\n""" % name
    del name


class GenericNodeVisitor(NodeVisitor):

    """
    Generic "Visitor" abstract superclass, for simple traversals.

    Unless overridden, each ``visit_...`` method calls `default_visit()`, and
    each ``depart_...`` method (when using `Node.walkabout()`) calls
    `default_departure()`. `default_visit()` (`default_departure()`) must be
    overridden in subclasses.

    Define fully generic visitors by overriding `default_visit()`
    (`default_departure()`) only. Define semi-generic visitors by overriding
    individual ``visit_...()`` (``depart_...()``) methods also.

    `NodeVisitor.unknown_visit()` (`NodeVisitor.unknown_departure()`) should
    be overridden for default behavior.
    """

    def default_visit(self, node):
        """Override for generic, uniform traversals."""
        raise NotImplementedError

    def default_departure(self, node):
        """Override for generic, uniform traversals."""
        raise NotImplementedError

    # Save typing with dynamic definitions.
    for name in node_class_names:
        exec """def visit_%s(self, node):
                    self.default_visit(node)\n""" % name
        exec """def depart_%s(self, node):
                    self.default_departure(node)\n""" % name
    del name


class VisitorException(Exception): pass
class SkipChildren(VisitorException): pass
class SkipSiblings(VisitorException): pass
class SkipNode(VisitorException): pass
