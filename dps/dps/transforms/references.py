#! /usr/bin/env python
"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/01/26 00:10:09 $
:Copyright: This module has been placed in the public domain.

Transforms for resolving references:

- `Hyperlinks`: Used to resolve hyperlink targets and references.
- `Footnotes`: Resolve footnote numbering and references.
- `Substitutions`: Resolve substitutions.
"""

__docformat__ = 'reStructuredText'

import re
from dps import nodes, utils
from dps.transforms import TransformError, Transform


class Hyperlinks(Transform):

    """
    Resolve the various types of hyperlink targets and references.

    Shown in isolation, the following individual transforms are performed:

    1. Anonymous references and targets::

           <paragraph>
               <reference anonymous="1">
                   text
           <target anonymous="1">

       Corresponding references and targets are assigned names, and the
       "anonymous" attributes are dropped::

           <paragraph>
               <reference refname="_:1:_">
                   text
           <target name="_:1:_">

    2. Chained targets::

           <target name="chained">
           <target name="external hyperlink" refuri="http://uri">

       Attributes "refuri" and "refname" are migrated from the final concrete
       target up the chain of contiguous adjacent internal targets::

           <target name="chained" refuri="http://uri">
           <target name="external hyperlink" refuri="http://uri">

    3. a) Indirect targets::

              <paragraph>
                  <reference refname="indirect external">
                      indirect external
              <target name="direct external" refuri="http://indirect">
              <target name="indirect external" refname="direct external">

          Attributes "refuri" and "refname" are migrated back to all indirect
          targets from the final concrete target (i.e. not referring to
          another indirect target)::

              <paragraph>
                  <reference refname="indirect external">
                      indirect external
              <target name="direct external" refuri="http://indirect">
              <target name="indirect external" refuri="http://indirect">

          If the "refuri" attribute is migrated, the preexisting "refname"
          attribute is dropped. This turns indirect external references into
          direct external references.

       b) Indirect internal references::

              <target name="final target">
              <paragraph>
                  <reference refname="indirect internal">
                      indirect internal
              <target name="indirect internal 2" refname="final target">
              <target name="indirect internal" refname="indirect internal 2">

          Targets which indirectly refer to an internal target become one-hop
          indirect (their "refname" attributes are directly set to the
          internal target's "name"). References which indirectly refer to an
          internal target become direct internal references::

              <target name="final target">
              <paragraph>
                  <reference refname="final target">
                      indirect internal
              <target name="indirect internal 2" refname="final target">
              <target name="indirect internal" refname="final target">

    4. External references::

           <paragraph>
               <reference refname="direct external">
                   direct external
           <target name="direct external" refuri="http://direct">

       The "refname" attribute is replaced by the direct "refuri" attribute::

           <paragraph>
               <reference refuri="http://direct">
                   direct external
           <target name="direct external" refuri="http://direct">
    """

    def transform(self, doctree):
        self.setup_transform(doctree)
        self.resolve_anonymous()
        self.resolve_chained_targets()
        self.resolve_indirect()
        self.resolve_external_references()

    def resolve_anonymous(self):
        if len(self.doctree.anonymous_refs) \
              != len(self.doctree.anonymous_targets):
            sw = self.doctree.reporter.error(
                  'Anonymous hyperlink mismatch: %s references but %s targets.'
                  % (len(self.doctree.anonymous_refs),
                     len(self.doctree.anonymous_targets)))
            self.doctree += sw
            return
        for i in range(len(self.doctree.anonymous_refs)):
            name = '_:%s:_' % self.doctree.anonymous_start
            self.doctree.anonymous_start += 1
            ref = self.doctree.anonymous_refs[i]
            ref['refname'] = name
            del ref['anonymous']
            self.doctree.note_refname(ref)
            target = self.doctree.anonymous_targets[i]
            target['name'] = name
            del target['anonymous']
            self.doctree.note_implicit_target(target, self.doctree)
            if target.hasattr('refname'):
                self.doctree.note_indirect_target(target)
            if target.hasattr('refuri'):
                self.doctree.note_external_target(target)

    def resolve_chained_targets(self):
        ChainedTargetResolver(self.doctree).walk()

    def resolve_indirect(self):
        for name, targets in self.doctree.indirect_targets.items():
            if len(targets) == 1:
                target = targets[-1]
                if not target.resolved:
                    self.one_indirect_target(target)
                if target.hasattr('refname'):
                    self.one_indirect_reference(target['name'],
                                                target['refname'])

    def one_indirect_target(self, target):
        name = target['name']
        refname = target['refname']
        try:
            reftargetlist = self.doctree.explicit_targets[refname]
        except KeyError:
            sw = self.doctree.reporter.warning(
                  'Indirect hyperlink target "%s" refers to target "%s", '
                  'which does not exist.' % (name, refname))
            self.doctree += sw
        reftarget = reftargetlist[-1]
        if reftarget.hasattr('name'):
            if not reftarget.resolved and reftarget.hasattr('refname'):
                self.one_indirect_target(reftarget)
            if reftarget.hasattr('refuri'):
                target['refuri'] = reftarget['refuri']
                del target['refname']
                self.doctree.note_external_target(target)
            elif reftarget.hasattr('refname'):
                target['refname'] = reftarget['refname']
        target.resolved = 1

    def one_indirect_reference(self, name, refname):
        try:
            reflist = self.doctree.refnames[name]
        except KeyError, instance:
            sw = self.doctree.reporter.information(
                  'Indirect hyperlink target "%s" is not referenced.'
                  % name)
            self.doctree += sw
            return
        for ref in self.doctree.refnames[name]:
            if ref.resolved:
                continue
            try:
                ref['refname'] = refname
            except KeyError, instance:
                sw = self.doctree.reporter.error(
                      'Indirect hyperlink target "%s" has no "refname" '
                      'attribute.' % name)
                self.doctree += sw
                continue
            ref.resolved = 1
            if isinstance(ref, nodes.target):
                self.one_indirect_reference(ref['name'], refname)

    def resolve_external_references(self):
        for name, targets in self.doctree.external_targets.items():
            target = targets[-1]
            if target.hasattr('refuri') and target.hasattr('name'):
                self.one_external_reference(name, targets[-1]['refuri'])

    def one_external_reference(self, name, refuri):
        try:
            reflist = self.doctree.refnames[name]
        except KeyError, instance:
            sw = self.doctree.reporter.information(
                  'External hyperlink target "%s" is not referenced.'
                  % name)
            self.doctree += sw
            return
        for ref in self.doctree.refnames[name]:
            if ref.resolved:
                continue
            try:
                ref['refuri'] = refuri
            except KeyError, instance:
                sw = self.doctree.reporter.error(
                      'External hyperlink target "%s" has no "refuri" '
                      'attribute.' % name)
                self.doctree += sw
                continue
            del ref['refname']
            ref.resolved = 1
            if isinstance(ref, nodes.target):
                self.one_external_reference(ref['name'], refuri)


class ChainedTargetResolver(nodes.Visitor):

    """
    Copy reference attributes up a length of hyperlink target chain.

    "Chained targets" are multiple adjacent internal hyperlink targets which
    "point to" an external or indirect target. After the transform, all
    chained targets will effectively point to the same place.

    Given the following ``doctree`` as input::

        <document>
            <target name="a">
            <target name="b">
            <target name="c" refuri="http://chained.external.targets">
            <target name="d">
            <paragraph>
                I'm known as "d".
            <target name="e">
            <target name="f">
            <target name="g" refname="d">

    ``ChainedTargetResolver(doctree).walk()`` will transform the above into::

        <document>
            <target name="a" refuri="http://chained.external.targets">
            <target name="b" refuri="http://chained.external.targets">
            <target name="c" refuri="http://chained.external.targets">
            <target name="d">
            <paragraph>
                I'm known as "d".
            <target name="e" refname="d">
            <target name="f" refname="d">
            <target name="g" refname="d">
    """

    def visit_target(self, node, ancestry):
        if node.hasattr('refuri'):
            refuri = node['refuri']
            parent, index = ancestry[-1]
            for i in range(index - 1, -1, -1):
                sibling = parent[i]
                if not isinstance(sibling, nodes.target) \
                      or sibling.hasattr('refuri') \
                      or sibling.hasattr('refname'):
                    break
                sibling['refuri'] = refuri
                self.doctree.note_external_target(sibling)
        elif node.hasattr('refname'):
            refname = node['refname']
            parent, index = ancestry[-1]
            for i in range(index - 1, -1, -1):
                sibling = parent[i]
                if not isinstance(sibling, nodes.target) \
                      or sibling.hasattr('refuri') \
                      or sibling.hasattr('refname'):
                    break
                sibling['refname'] = refname
                self.doctree.note_indirect_target(sibling)


class Footnotes(Transform):

    """
    """

    def transform(self, doctree):
        pass


class Substitutions(Transform):

    """
    """

    def transform(self, doctree):
        pass
