#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.9 $
:Date: $Date: 2001/09/12 03:47:12 $
:Copyright: This module has been placed in the public domain.

"""

import sys
import xml.dom.minidom
from types import IntType, SliceType, StringType, TupleType
from UserString import MutableString

class _Node:

    def __nonzero__(self):
        """_Node instances are always true."""
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


class Text(_Node, MutableString):

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


class _Element(_Node):

    """
    `_Element` is the superclass to all specific elements.

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
        if isinstance(other, _Node):
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
        assert isinstance(item, _Node)
        self.children.append(item)

    def extend(self, item):
        self.children.extend(item)

    def insert(self, i, item):
        assert isinstance(item, _Node)
        self.children.insert(i, item)

    def pop(self, i=-1):
        return self.children.pop(i)

    def remove(self, item):
        assert isinstance(item, _Node)
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
        if self.children:
            return ''.join(['%s%s\n' % (indent * level, self.starttag())] +
                           [child.pformat(indent, level+1)
                            for child in self.children]
                           + ['%s%s\n' % (indent * level, self.endtag())])
        else:
            return '%s%s\n' % (indent * level, self.emptytag())


class _TextElement(_Element):

    """
    An element which directly contains text.

    Its children are all Text or _TextElement nodes.
    """

    childtextsep = ''
    """Separator for child nodes, used by `astext()` method."""

    def __init__(self, rawsource='', text='', *children, **attributes):
        if text != '':
            textnode = Text(text)
            _Element.__init__(self, rawsource, textnode, *children,
                              **attributes)
        else:
            _Element.__init__(self, rawsource, *children, **attributes)


# ==============
#  Root Element
# ==============

class document(_Element):

    def __init__(self, errorhandler, *args, **kwargs):
        _Element.__init__(self, *args, **kwargs)
        self.explicitlinks = {}
        self.implicitlinks = {}
        self.indirectlinks = {}
        self.refnames = {}
        self.autofootnotes = []
        self.autofootnoterefs = []
        self.errorhandler = errorhandler

    def asdom(self, dom=xml.dom.minidom):
        domroot = dom.Document()
        domroot.appendChild(_Element._rooted_dom_node(self, domroot))
        return domroot

    def addimplicitlink(self, name, linknode, innode=None):
        if innode == None:
            innode = linknode
        if self.explicitlinks.has_key(name) \
              or self.indirectlinks.has_key(name) \
              or self.implicitlinks.has_key(name):
            sw = self.errorhandler.system_warning(
                  0, 'Duplicate implicit link name: "%s"' % name)
            innode += sw
            self.clearlinknames(name, self.implicitlinks)
            linknode['dupname'] = name
            self.implicitlinks.setdefault(name, []).append(linknode)
        else:
            self.implicitlinks[name] = [linknode]
            linknode['name'] = name

    def addexplicitlink(self, name, linknode, innode=None):
        if innode == None:
            innode = linknode
        if self.explicitlinks.has_key(name):
            sw = self.errorhandler.system_warning(
                  1, 'Duplicate explicit link name: "%s"' % name)
            innode += sw
            self.clearlinknames(name, self.explicitlinks, self.implicitlinks,
                                self.indirectlinks)
            linknode['dupname'] = name
            self.explicitlinks.setdefault(name, []).append(linknode)
            return
        elif self.implicitlinks.has_key(name):
            sw = self.errorhandler.system_warning(
                  0, 'Duplicate implicit link name: "%s"' % name)
            innode += sw
            self.clearlinknames(name, self.implicitlinks)
        self.explicitlinks[name] = [linknode]
        linknode['name'] = name

    def clearlinknames(self, name, *linkdicts):
        for linkdict in linkdicts:
            for node in linkdict.get(name, []):
                if node.has_key('name'):
                    node['dupname'] = node['name']
                    del node['name']

    def addrefname(self, name, node):
        self.refnames.setdefault(name, []).append(node)

    def addindirectlink(self, name, reference, linknode, innode):
        if self.explicitlinks.has_key(name):
            level = 0
            for t in self.explicitlinks.get(name, []):
                if len(t) != 1 or str(t[0]) != reference:
                    level = 1
                    break
            sw = self.errorhandler.system_warning(
                  level, 'Duplicate indirect link name: "%s"' % name)
            innode += sw
            self.clearlinknames(name, self.explicitlinks, self.indirectlinks,
                                self.implicitlinks)
        elif self.implicitlinks.has_key(name):
            print >>sys.stderr, "already has explicit link"
            sw = self.errorhandler.system_warning(
                  0, 'Duplicate implicit link name: "%s"' % name)
            innode += sw
            self.clearlinknames(name, self.implicitlinks)
        self.indirectlinks.setdefault(name, []).append(linknode)
        self.explicitlinks.setdefault(name, []).append(linknode)
        linknode['name'] = name

    def addautofootnote(self, name, footnotenode):
        footnotenode['auto'] = 1
        self.autofootnotes.append((name, footnotenode))

    def addautofootnoteref(self, refname, refnode):
        refnode['auto'] = 1
        self.autofootnoterefs.append((refname, refnode))


# ========================
#  Bibliographic Elements
# ========================

class title(_TextElement): pass
class subtitle(_TextElement): pass
class author(_TextElement): pass
class authors(_Element): pass
class organization(_TextElement): pass
class contact(_TextElement): pass
class version(_TextElement): pass
class revision(_TextElement): pass
class status(_TextElement): pass
class date(_TextElement): pass
class copyright(_TextElement): pass
class abstract(_Element): pass


# =====================
#  Structural Elements
# =====================

class section(_Element): pass

class package_section(_Element): pass
class module_section(_Element): pass
class class_section(_Element): pass
class method_section(_Element): pass
class function_section(_Element): pass
class module_attribute_section(_Element): pass
class class_attribute_section(_Element): pass
class instance_attribute_section(_Element): pass

# Structural Support Elements
# ---------------------------

class inheritance_list(_Element): pass
class parameter_list(_Element): pass
class parameter_item(_Element): pass
class optional_parameters(_Element): pass
class parameter_tuple(_Element): pass
class parameter_default(_TextElement): pass
class initial_value(_TextElement): pass


# ===============
#  Body Elements
# ===============

class paragraph(_TextElement): pass
class bullet_list(_Element): pass
class enumerated_list(_Element): pass
class list_item(_Element): pass
class definition_list(_Element): pass
class definition_list_item(_Element): pass
class term(_TextElement): pass
class classifier(_TextElement): pass
class definition(_Element): pass
class field_list(_Element): pass
class field(_Element): pass
class field_name(_TextElement): pass
class field_argument(_TextElement): pass
class field_body(_Element): pass
class literal_block(_TextElement): pass
class block_quote(_Element): pass
class note(_Element): pass
class tip(_Element): pass
class warning(_Element): pass
class error(_Element): pass
class caution(_Element): pass
class danger(_Element): pass
class important(_Element): pass
class comment(_TextElement): pass
class directive(_Element): pass
class target(_TextElement): pass
class footnote(_Element): pass
class label(_TextElement): pass
class figure(_Element): pass
class caption(_TextElement): pass
class legend(_Element): pass
class table(_Element): pass
class tgroup(_Element): pass
class colspec(_Element): pass
class thead(_Element): pass
class tbody(_Element): pass
class row(_Element): pass
class entry(_Element): pass


class system_warning(_Element):

    def __init__(self, comment=None, *children, **attributes):
        #print ('nodes.system_warning.__init__: comment=%r, children=%r, '
        #       'attributes=%r' % (comment, children, attributes))
        if comment:
            p = paragraph('', comment)
            children = (p,) + children
        _Element.__init__(self, '', *children, **attributes)

    def astext(self):
        return '[level %s] ' % self['level'] + _Element.astext(self)


class option_list(_Element): pass
class option_list_item(_Element): pass
class option(_Element): pass
class short_option(_TextElement): pass
class long_option(_TextElement): pass
class vms_option(_TextElement): pass
class option_argument(_TextElement): pass
class description(_Element): pass
class doctest_block(_TextElement): pass


# =================
#  Inline Elements
# =================

class emphasis(_TextElement): pass
class strong(_TextElement): pass
class interpreted(_TextElement): pass
class literal(_TextElement): pass
class link(_TextElement): pass
class footnote_reference(_TextElement): pass
class image(_TextElement): pass

class package(_TextElement): pass
class module(_TextElement): pass


class inline_class(_TextElement):

    tagname = 'class'


class method(_TextElement): pass
class function(_TextElement): pass
class variable(_TextElement): pass
class parameter(_TextElement): pass
class type(_TextElement): pass
class class_attribute(_TextElement): pass
class module_attribute(_TextElement): pass
class instance_attribute(_TextElement): pass
class exception_class(_TextElement): pass
class warning_class(_TextElement): pass
