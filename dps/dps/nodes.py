#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.21 $
:Date: $Date: 2002/01/16 02:47:59 $
:Copyright: This module has been placed in the public domain.

"""

import sys
import xml.dom.minidom
from types import IntType, SliceType, StringType, TupleType
from UserString import MutableString

# ==============================
#  Functional Node Base Classes
# ==============================

class Node:

    def __nonzero__(self):
        """Node instances are always true."""
        return 1

    def asdom(self, dom=xml.dom.minidom):
        return self._dom_node(dom)

    def _dom_node(self, dom):
        pass
    
    def _rooted_dom_node(self, domroot):
        pass

    def astext(self):
        pass

    def validate(self):
        pass


class Text(Node, MutableString):

    tagname = '#text'

    def __repr__(self):
        data = repr(self.data)
        if len(data) > 70:
            data = repr(self.data[:64] + ' ...')
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

    childtextsep = '\n\n'
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
            data += '<%s...>' % c.tagname
            if len(data) > 60:
                data = data[:56] + ' ...'
                break
        return '<%s: %s>' % (self.__class__.__name__, data)

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
        return self.childtextsep.join([child.astext()
                                       for child in self.children])

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
        Return the index of the first child whose class matches `childclass`.

        `childclass` may also be a tuple of node classes, in which case any
        of the classes may match.
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
        Return the index of the first child not matching `childclass`.

        `childclass` may also be a tuple of node classes, in which case none
        of the classes may match.
        """
        if not isinstance(childclass, TupleType):
            childclass = (childclass,)
        for index in range(start, min(len(self), end)):
            match = 0
            for c in childclass:
                if isinstance(self[index], c):
                    match = 1
            if not match:
                return index
        return None

    def pformat(self, indent='    ', level=0):
        return ''.join(['%s%s\n' % (indent * level, self.starttag())] +
                           [child.pformat(indent, level+1)
                            for child in self.children])


class TextElement(Element):

    """
    An element which directly contains text.

    Its children are all Text or TextElement nodes.
    """

    childtextsep = ''
    """Separator for child nodes, used by `astext()` method."""

    def __init__(self, rawsource='', text='', *children, **attributes):
        if text != '':
            textnode = Text(text)
            Element.__init__(self, rawsource, textnode, *children,
                              **attributes)
        else:
            Element.__init__(self, rawsource, *children, **attributes)


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


# ==============
#  Root Element
# ==============

class document(Root, Element):

    def __init__(self, reporter, languagecode, *args, **kwargs):
        Element.__init__(self, *args, **kwargs)
        self.reporter = reporter
        self.languagecode = languagecode
        self.explicittargets = {}
        self.implicittargets = {}
        self.externaltargets = {}
        self.indirecttargets = {}
        self.substitutiondefs = {}
        self.refnames = {}
        self.substitutionrefs = {}
        self.anonymoustargets = []
        self.anonymousrefs = []
        self.autofootnotes = []
        self.autofootnoterefs = []

    def asdom(self, dom=xml.dom.minidom):
        domroot = dom.Document()
        domroot.appendChild(Element._rooted_dom_node(self, domroot))
        return domroot

    def addimplicittarget(self, name, targetnode, innode=None):
        if innode == None:
            innode = targetnode
        if self.explicittargets.has_key(name) \
              or self.externaltargets.has_key(name) \
              or self.implicittargets.has_key(name):
            sw = self.reporter.information(
                  'Duplicate implicit target name: "%s"' % name)
            innode += sw
            self.cleartargetnames(name, self.implicittargets)
            targetnode['dupname'] = name
            self.implicittargets.setdefault(name, []).append(targetnode)
        else:
            self.implicittargets[name] = [targetnode]
            targetnode['name'] = name

    def addexplicittarget(self, name, targetnode, innode=None):
        if innode == None:
            innode = targetnode
        if self.explicittargets.has_key(name):
            sw = self.reporter.warning(
                  'Duplicate explicit target name: "%s"' % name)
            innode += sw
            self.cleartargetnames(name, self.explicittargets,
                                  self.implicittargets, self.externaltargets)
            targetnode['dupname'] = name
            self.explicittargets.setdefault(name, []).append(targetnode)
            return
        elif self.implicittargets.has_key(name):
            sw = self.reporter.information(
                  'Duplicate implicit target name: "%s"' % name)
            innode += sw
            self.cleartargetnames(name, self.implicittargets)
        self.explicittargets[name] = [targetnode]
        targetnode['name'] = name

    def cleartargetnames(self, name, *targetdicts):
        for targetdict in targetdicts:
            for node in targetdict.get(name, []):
                if node.has_key('name'):
                    node['dupname'] = node['name']
                    del node['name']

    def addrefname(self, name, node):
        self.refnames.setdefault(name, []).append(node)

    def addexternaltarget(self, name, reference, targetnode, innode):
        if self.explicittargets.has_key(name):
            level = 0
            for t in self.explicittargets.get(name, []):
                if not t.has_key('refuri') or t['refuri'] != reference:
                    level = 1
                    break
            sw = self.reporter.system_warning(
                  level, 'Duplicate external target name: "%s"' % name)
            innode += sw
            self.cleartargetnames(name, self.explicittargets,
                                  self.externaltargets, self.implicittargets)
        elif self.implicittargets.has_key(name):
            sw = self.reporter.information(
                  'Duplicate implicit target name: "%s"' % name)
            innode += sw
            self.cleartargetnames(name, self.implicittargets)
        self.externaltargets.setdefault(name, []).append(targetnode)
        self.explicittargets.setdefault(name, []).append(targetnode)
        targetnode['name'] = name
        targetnode['refuri'] = reference

    def addindirecttarget(self, refname, targetnode):
        targetnode['refname'] = refname
        self.indirecttargets[refname] = targetnode

    def addanonymoustarget(self, targetnode):
        targetnode['anonymous'] = 1
        self.anonymoustargets.append(targetnode)

    def addanonymousref(self, refnode):
        refnode['anonymous'] = 1
        self.anonymousrefs.append(refnode)

    def addautofootnote(self, name, footnotenode):
        footnotenode['auto'] = 1
        self.autofootnotes.append((name, footnotenode))

    def addautofootnoteref(self, refname, refnode):
        refnode['auto'] = 1
        self.autofootnoterefs.append((refname, refnode))

    def addsubstitutiondef(self, name, substitutiondefnode, innode):
        if self.substitutiondefs.has_key(name):
            sw = self.reporter.error(
                  'Duplicate substitution definition name: "%s"' % name)
            innode += sw
            oldnode = self.substitutiondefs[name]
            oldnode['dupname'] = oldnode['name']
            del oldnode['name']
        self.substitutiondefs[name] = substitutiondefnode

    def addsubstitutionref(self, refname, subrefnode):
        subrefnode['refname'] = refname
        self.substitutionrefs.setdefault(refname, []).append(subrefnode)


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

class package_section(Structural, Element): pass
class module_section(Structural, Element): pass
class class_section(Structural, Element): pass
class method_section(Structural, Element): pass
class function_section(Structural, Element): pass
class module_attribute_section(Structural, Element): pass
class class_attribute_section(Structural, Element): pass
class instance_attribute_section(Structural, Element): pass

# Structural Support Elements
# ---------------------------

class inheritance_list(Component, Element): pass
class parameter_list(Component, Element): pass
class parameter_item(Component, Element): pass
class optional_parameters(Component, Element): pass
class parameter_tuple(Component, Element): pass
class parameter_default(Component, TextElement): pass
class initial_value(Component, TextElement): pass


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
class target(Special, Inline, TextElement): pass
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
class interpreted(Inline, TextElement): pass
class literal(Inline, TextElement): pass
class reference(Inline, TextElement): pass
class footnote_reference(Inline, TextElement): pass
class substitution_reference(Inline, TextElement): pass
class image(General, Inline, TextElement): pass

class package(Component, Inline, TextElement): pass
class module(Component, Inline, TextElement): pass


class inline_class(Component, Inline, TextElement):

    tagname = 'class'


class method(Component, Inline, TextElement): pass
class function(Component, Inline, TextElement): pass
class variable(Inline, TextElement): pass
class parameter(Component, Inline, TextElement): pass
class type(Inline, TextElement): pass
class class_attribute(Component, Inline, TextElement): pass
class module_attribute(Component, Inline, TextElement): pass
class instance_attribute(Component, Inline, TextElement): pass
class exception_class(Inline, TextElement): pass
class warning_class(Inline, TextElement): pass
