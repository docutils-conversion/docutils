#! /usr/bin/env python
"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.12 $
:Date: $Date: 2002/03/16 05:59:38 $
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

       Corresponding references and targets are assigned ids::

           <paragraph>
               <reference anonymous="1" refid="id1">
                   text
           <target anonymous="1" id="id1">

    2. Chained targets::

           <target id="id1" name="chained">
           <target id="id2" name="external hyperlink" refuri="http://uri">

       Attributes "refuri" and "refname" are migrated from the final concrete
       target up the chain of contiguous adjacent internal targets::

           <target id="id1" name="chained" refuri="http://uri">
           <target id="id2" name="external hyperlink" refuri="http://uri">

    3. a) Indirect targets::

              <paragraph>
                  <reference refname="indirect external">
                      indirect external
              <target id="id1" name="direct external"
                  refuri="http://indirect">
              <target id="id2" name="indirect external"
                  refname="direct external">

          Attributes "refuri" and "refname" are migrated back to all indirect
          targets from the final concrete target (i.e. not referring to
          another indirect target)::

              <paragraph>
                  <reference refname="indirect external">
                      indirect external
              <target id="id1" name="direct external"
                  refuri="http://indirect">
              <target id="id2" name="indirect external"
                  refuri="http://indirect">

          If the "refuri" attribute is migrated, the preexisting "refname"
          attribute is dropped. This turns indirect external references into
          direct external references.

       b) Indirect internal references::

              <target id="id1" name="final target">
              <paragraph>
                  <reference refname="indirect internal">
                      indirect internal
              <target id="id2" name="indirect internal 2"
                  refname="final target">
              <target id="id3" name="indirect internal"
                  refname="indirect internal 2">

          Targets which indirectly refer to an internal target become one-hop
          indirect (their "refname" attributes are directly set to the
          internal target's "name"). References which indirectly refer to an
          internal target become direct internal references::

              <target id="id1" name="final target">
              <paragraph>
                  <reference refname="final target">
                      indirect internal
              <target id="id2" name="indirect internal 2"
                  refname="final target">
              <target id="id3" name="indirect internal"
                  refname="final target">

    4. External references::

           <paragraph>
               <reference refname="direct external">
                   direct external
           <target id="id1" name="direct external" refuri="http://direct">

       The "refname" attribute is replaced by the direct "refuri" attribute::

           <paragraph>
               <reference refuri="http://direct">
                   direct external
           <target id="id1" name="direct external" refuri="http://direct">
    """

    def transform(self):
        self.resolve_anonymous()
        self.resolve_chained_targets()
        self.resolve_indirect()
        self.resolve_external_references()

    def resolve_anonymous(self):
        if len(self.doctree.anonymous_refs) \
              != len(self.doctree.anonymous_targets):
            msg = self.doctree.reporter.error(
                  'Anonymous hyperlink mismatch: %s references but %s targets.'
                  % (len(self.doctree.anonymous_refs),
                     len(self.doctree.anonymous_targets)))
            self.doctree.messages += msg
            return
        for i in range(len(self.doctree.anonymous_refs)):
            name = '_:%s:_' % self.doctree.anonymous_start
            self.doctree.anonymous_start += 1
            ref = self.doctree.anonymous_refs[i]
            ref['refname'] = name
            self.doctree.note_refname(ref)
            target = self.doctree.anonymous_targets[i]
            target['name'] = name
            id = self.doctree.set_id(target)
            self.doctree.note_implicit_target(target, self.doctree)
            if target.hasattr('refname'):
                #ref['refname'] = target['refname']
                self.doctree.note_indirect_target(target)
            elif target.hasattr('refuri'):
                #ref['refuri'] = target['refuri']
                self.doctree.note_external_target(target)
            #else:
            #    ref['refid'] = id

    def resolve_chained_targets(self):
        visitor = ChainedTargetResolver(self.doctree)
        self.doctree.walk(visitor)

    def resolve_indirect(self):
        for name, target in self.doctree.indirect_targets.items():
            if not target.resolved:
                self.one_indirect_target(target)
            if target.hasattr('refname'):
                self.one_indirect_reference(target['name'],
                                            target['refname'])

    def one_indirect_target(self, target):
        name = target['name']
        refname = target['refname']
        if self.doctree.explicit_targets.has_key(refname):
            try:
                reftarget = self.doctree.explicit_targets[refname]
            except KeyError:
                self.nonexistent_indirect_target(name, refname, target)
                return
            if reftarget.hasattr('name'):
                if not reftarget.resolved and reftarget.hasattr('refname'):
                    self.one_indirect_target(reftarget) # multiply indirect
                if reftarget.hasattr('refuri'):
                    target['refuri'] = reftarget['refuri']
                    del target['refname']
                    self.doctree.note_external_target(target)
                elif reftarget.hasattr('refname'):
                    target['refname'] = reftarget['refname']
                #else: # @@@ ?
                #    target['refid'] = reftarget['refid']
        elif self.doctree.implicit_targets.has_key(refname):
            reftarget = self.doctree.implicit_targets[refname]
            try:
                target['refname'] = reftarget['name']
            except KeyError:
                self.nonexistent_indirect_target(name, refname, target)
                return
        else:
            self.nonexistent_indirect_target(name, refname, target)
            return
        target.resolved = 1

    def nonexistent_indirect_target(self, name, refname, target):
        if target.hasattr('anonymous'):
            naming = '(id="%s")' % target['id']
        else:
            naming = '"%s"' % name
        msg = self.doctree.reporter.warning(
              'Indirect hyperlink target %s refers to target "%s", '
              'which does not exist.' % (naming, refname))
        self.doctree.messages += msg

    def one_indirect_reference(self, name, refname):
        try:
            reflist = self.doctree.refnames[name]
        except KeyError, instance:
            msg = self.doctree.reporter.info(
                  'Indirect hyperlink target "%s" is not referenced.'
                  % name)
            self.doctree.messages += msg
            return
        for ref in self.doctree.refnames[name]:
            if ref.resolved:
                continue
            ref['refname'] = refname
            ref.resolved = 1
            if isinstance(ref, nodes.target):
                self.one_indirect_reference(ref['name'], refname)

    def resolve_external_references(self):
        for name, target in self.doctree.external_targets.items():
            if target.hasattr('refuri') and target.hasattr('name'):
                self.one_external_reference(name, target['refuri'])

    def one_external_reference(self, name, refuri):
        try:
            reflist = self.doctree.refnames[name]
        except KeyError, instance:
            msg = self.doctree.reporter.info(
                  'External hyperlink target "%s" is not referenced.' % name)
            self.doctree.messages += msg
            return
        for ref in self.doctree.refnames[name]:
            if ref.resolved:
                continue
            ref['refuri'] = refuri
            del ref['refname']
            ref.resolved = 1
            if isinstance(ref, nodes.target):
                self.one_external_reference(ref['name'], refuri)


class ChainedTargetResolver(nodes.NodeVisitor):

    """
    Copy reference attributes up the length of a hyperlink target chain.

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

    def unknown_visit(self, node):
        pass

    def visit_target(self, node):
        if node.hasattr('refuri'):
            refuri = node['refuri']
            index = node.parent.index(node)
            for i in range(index - 1, -1, -1):
                sibling = node.parent[i]
                if not isinstance(sibling, nodes.target) \
                      or sibling.hasattr('refuri') \
                      or sibling.hasattr('refname'):
                    break
                sibling['refuri'] = refuri
                self.doctree.note_external_target(sibling)
        elif node.hasattr('refname'):
            refname = node['refname']
            index = node.parent.index(node)
            for i in range(index - 1, -1, -1):
                sibling = node.parent[i]
                if not isinstance(sibling, nodes.target) \
                      or sibling.hasattr('refuri') \
                      or sibling.hasattr('refname'):
                    break
                sibling['refname'] = refname
                self.doctree.note_indirect_target(sibling)


class Footnotes(Transform):

    """
    Assign numbers and resolve links to autonumbered footnotes and references.

    Given the following ``doctree`` as input::

        <document>
            <paragraph>
                A labeled autonumbered footnote referece:
                <footnote_reference auto="1" refname="footnote">
            <paragraph>
                An unlabeled autonumbered footnote referece:
                <footnote_reference auto="1">
            <footnote auto="1">
                <paragraph>
                    Unlabeled autonumbered footnote.
            <footnote auto="1" name="footnote">
                <paragraph>
                    Labeled autonumbered footnote.

    Auto-numbered footnotes have attribute ``auto="1"`` and no label.
    Auto-numbered footnote_references have no reference text (they're
    empty elements). When resolving the numbering, a ``label`` element
    is added to the beginning of the ``footnote``, and reference text
    to the ``footnote_reference``.

    The transformed result will be::

        <document>
            <paragraph>
                A labeled autonumbered footnote referece:
                <footnote_reference auto="1" refname="footnote">
                    2
            <paragraph>
                An unlabeled autonumbered footnote referece:
                <footnote_reference auto="1" refname="1">
                    1
            <footnote auto="1" name="1">
                <label>
                    1
                <paragraph>
                    Unlabeled autonumbered footnote.
            <footnote auto="1" name="footnote">
                <label>
                    2
                <paragraph>
                    Labeled autonumbered footnote.

    Note that the footnotes are not in the same order as the references.

    The labels and reference text are added to the auto-numbered
    ``footnote`` and ``footnote_reference`` elements. The unlabeled
    auto-numbered footnote and reference are assigned name and refname
    attributes respectively, being the footnote number.

    After adding labels and reference text, the "auto" attributes can be
    ignored.
    """

    autofootnote_labels = None
    """Keep track of unlabeled autonumbered footnotes."""

    symbols = [
          # Entries 1-4 and 6 below are from section 12.51 of
          # The Chicago Manual of Style, 14th edition.
          '*',                          # asterisk/star
          u'\u2020',                    # dagger &dagger;
          u'\u2021',                    # double dagger &Dagger;
          u'\u00A7',                    # section mark &sect;
          u'\u00B6',                    # paragraph mark (pilcrow) &para;
                                        # (parallels ['||'] in CMoS)
          '#',                          # number sign
          # The entries below were chosen arbitrarily.
          u'\u2660',                    # spade suit &spades;
          u'\u2665',                    # heart suit &hearts;
          u'\u2666',                    # diamond suit &diams;
          u'\u2663',                    # club suit &clubs;
          ]

    def transform(self):
        self.autofootnote_labels = []
        startnum = self.doctree.autofootnote_start
        self.number_footnotes()
        self.number_footnote_references(startnum)
        self.symbolize_footnotes()

    def number_footnotes(self):
        """
        Assign numbers to autonumbered footnotes.

        For labeled footnotes, copy the number over to corresponding footnote
        references.
        """
        for footnote in self.doctree.autofootnotes:
            while 1:
                label = str(self.doctree.autofootnote_start)
                self.doctree.autofootnote_start += 1
                if not self.doctree.explicit_targets.has_key(label):
                    break
            footnote.insert(0, nodes.label('', label))
            if footnote.hasattr('dupname'):
                continue
            if footnote.hasattr('name'):
                name = footnote['name']
                for ref in self.doctree.footnote_refs.get(name, []):
                    ref += nodes.Text(label)
                    ref.resolved = 1
            else:
                footnote['name'] = label
                self.doctree.note_explicit_target(footnote, footnote)
                self.autofootnote_labels.append(label)

    def number_footnote_references(self, startnum):
        """Assign numbers to unlabeled autonumbered footnote references."""
        i = 0
        for ref in self.doctree.autofootnote_refs:
            if ref.resolved or ref.hasattr('refname'):
                continue
            try:
                ref += nodes.Text(self.autofootnote_labels[i])
                ref['refname'] = self.autofootnote_labels[i]
            except IndexError:
                msg = self.doctree.reporter.error(
                      'Too many autonumbered footnote references: only %s '
                      'corresponding footnotes available.'
                      % len(self.autofootnote_labels))
                msgid = self.doctree.set_id(msg)
                self.doctree.messages += msg
                for ref in self.doctree.autofootnote_refs[i:]:
                    if not (ref.resolved or ref.hasattr('refname')):
                        prb = nodes.problematic(ref.rawsource, ref.rawsource,
                                                refid=msgid)
                        ref.parent.replace(ref, prb)
                        # @@@ insert reference to each prb in msg?
                break
            ref.resolved = 1
            i += 1

    def symbolize_footnotes(self):
        """Add symbols indexes to "[*]"-style footnotes and references."""
        labels = []
        for footnote in self.doctree.symbol_footnotes:
            reps, index = divmod(self.doctree.symbol_footnote_start,
                                 len(self.symbols))
            labeltext = self.symbols[index] * (reps + 1)
            labels.append(labeltext)
            footnote.insert(0, nodes.label('', labeltext))
            self.doctree.symbol_footnote_start += 1
            self.doctree.set_id(footnote)
        i = 0
        for ref in self.doctree.symbol_footnote_refs:
            try:
                ref += nodes.Text(labels[i])
                ref['refid'] = self.doctree.symbol_footnotes[i]['id']
            except IndexError:
                msg = self.doctree.reporter.error(
                      'Too many symbol footnote references: only %s '
                      'corresponding footnotes available.' % len(labels))
                msgid = self.set_id(msg)
                self.doctree.messages += msg
                for ref in self.doctree.symbol_footnote_refs[i:]:
                    if not (ref.resolved or ref.hasattr('refid')):
                        prb = nodes.problematic(ref.rawsource, ref.rawsource,
                                                refid=msgid)
                        ref.parent.replace(ref, prb)
                        # @@@ insert reference to each prb in msg?
                break
            ref.resolved = 1
            i += 1

class Substitutions(Transform):

    """
    Given the following ``doctree`` as input::

        <document>
            <paragraph>
                The
                <substitution_reference refname="biohazard">
                    biohazard
                 symbol is deservedly scary-looking.
            <substitution_definition name="biohazard">
                <image alt="biohazard" uri="biohazard.png">

    The ``substitution_reference`` will simply be replaced by the
    contents of the corresponding ``substitution_definition``.

    The transformed result will be::

        <document>
            <paragraph>
                The
                <image alt="biohazard" uri="biohazard.png">
                 symbol is deservedly scary-looking.
            <substitution_definition name="biohazard">
                <image alt="biohazard" uri="biohazard.png">
    """

    def transform(self):
        defs = self.doctree.substitution_defs
        for refname, refs in self.doctree.substitution_refs.items():
            for ref in refs:
                if defs.has_key(refname):
                    ref.parent.replace(ref, defs[refname].getchildren())
                else:
                    msg = self.doctree.reporter.error(
                          'Undefined substitution referenced: "%s".' % refname)
                    msgid = self.doctree.set_id(msg)
                    self.doctree.messages += msg
                    prb = nodes.problematic(
                          ref.rawsource, '', refid=msgid, *ref.getchildren())
                    prbid = self.doctree.set_id(prb)
                    ref.parent.replace(ref, prb)
                    msg['refid'] = prbid
        self.doctree.substitution_refs = None  # release replaced references
