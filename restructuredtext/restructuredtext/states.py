"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.20 $
:Date: $Date: 2001/09/17 04:24:20 $
:Copyright: This module has been placed in the public domain.

This is the ``dps.parsers.restructuredtext.states`` module, the core of the
reStructuredText parser. It defines the following:

:Classes:
    - `RSTStateMachine`: reStructuredText parser's entry point.
    - `NestedStateMachine`: recursive StateMachine.
    - `RSTState`: reStructuredText State superclass.
    - `Body`: Generic classifier of the first line of a block.
    - `BulletList`: Second and subsequent bullet_list list_items
    - `DefinitionList`: Second and subsequent definition_list_items.
    - `EnumeratedList`: Second and subsequent enumerated_list list_items.
    - `FieldList`: Second and subsequent fields.
    - `OptionList`: Second and subsequent option_list_items.
    - `Explicit`: Second and subsequent explicit markup constructs.
    - `Text`: Classifier of second line of a text block.
    - `Definition`: Second line of potential definition_list_item.
    - `Stuff`: An auxilliary collection class.

:Exception classes:
    - `MarkupError`
    - `ParserError`
    - `TransformationError`

:Functions:
    - `escape2null()`: Return a string, escape-backslashes converted to nulls.
    - `unescape()`: Return a string, nulls removed or restored to backslashes.
    - `normname()`: Return a case- and whitespace-normalized name.

:Attributes:
    - `stateclasses`: set of State classes used with `RSTStateMachine`.

Parser Overview
===============

The reStructuredText parser is implemented as a state machine, examining its
input one line at a time. To understand how the parser works, please first
become familiar with the `dps.statemachine` module. In the description below,
references are made to classes defined in this module; please see the
individual classes for details.

Parsing proceeds as follows:

1. The state machine examines each line of input, checking each of the
   transition patterns of the state `Body`, in order, looking for a match. The
   implicit transitions (blank lines and indentation) are checked before any
   others. The 'text' transition is a catch-all (matches anything).

2. The method associated with the matched transition pattern is called.

   A. Some transition methods are self-contained, appending elements to the
      document tree ('doctest' parses a doctest block). The parser's current
      line index is advanced to the end of the element, and parsing continues
      with step 1.

   B. Others trigger the creation of a nested state machine, whose job is to
      parse a compound construct ('indent' does a block quote, 'bullet' does a
      bullet list, 'overline' does a section [first checking for a valid
      section header]).

      - In the case of lists and explicit markup, a new state machine is
        created and run to parse the first item.

      - A new state machine is created and its initial state is set to the
        appropriate specialized state (`BulletList` in the case of the
        'bullet' transition). This state machine is run to parse the compound
        element (or series of explicit markup elements), and returns as soon
        as a non-member element is encountered. For example, the `BulletList`
        state machine aborts as soon as it encounters an element which is not
        a list item of that bullet list. The optional omission of
        inter-element blank lines is handled by the nested state machine.

      - The current line index is advanced to the end of the elements parsed,
        and parsing continues with step 1.

   C. The result of the 'text' transition depends on the next line of text.
      The current state is changed to `Text`, under which the second line is
      examined. If the second line is:

      - Indented: The element is a definition list item, and parsing proceeds
        similarly to step 2.B, using the `DefinitionList` state.

      - A line of uniform punctuation characters: The element is a section
        header; again, parsing proceeds as in step 2.B, and `Body` is still
        used.

      - Anything else: The element is a paragraph, which is examined for
        inline markup and appended to the parent element. Processing continues
        with step 1.
"""

__docformat__ = 'reStructuredText'


import sys, re, string
from dps import nodes, statemachine, utils, roman
from dps.statemachine import StateMachineWS, StateWS
import directives
from tableparser import TableParser, TableMarkupError


__all__ = ['RSTStateMachine', 'MarkupError', 'ParserError',
           'TransformationError']


class MarkupError(Exception): pass
class ParserError(Exception): pass
class TransformationError(Exception): pass


class Stuff:

    """Stores a bunch of stuff for dotted-attribute access."""

    def __init__(self, **keywordargs):
        self.__dict__.update(keywordargs)


class RSTStateMachine(StateMachineWS):

    """
    reStructuredText's master StateMachine.

    The entry point to reStructuredText parsing is the `run()` method.
    """

    def __init__(self, stateclasses, initialstate, language, debug=0):
        StateMachineWS.__init__(self, stateclasses, initialstate, debug=0)
        self.language = language

    def run(self, inputlines, inputoffset=0, warninglevel=1, errorlevel=3,
			matchtitles=1):
        """
        Parse `inputlines` and return a `dps.nodes.document` instance.

        Extend `StateMachineWS.run()`: set up parse-global data, run the
        StateMachine, do some final transformations, and return the resulting
        document.
        """
        self.matchtitles = matchtitles
        reporter = utils.Reporter(warninglevel, errorlevel)
        docroot = nodes.document(reporter)
        self.memo = Stuff(document=docroot,
                          reporter=reporter,
                          language=self.language,
                          titlestyles=[],
                          sectionlevel=0)
        self.node = docroot
        results = StateMachineWS.run(self, inputlines, inputoffset)
        assert results == [], 'RSTStateMachine.run() results should be empty.'
        self.promotelonesection()
        self.transformfirstfields()
        self.node = self.memo = None
        return docroot

    def promotelonesection(self):
        """
        Promote an only-child section to the document level.

        If the only non-comment child of an untitled document element is a
        section, the section is promoted to the document level. The section's
        title becomes the document title, and the section's contents become
        the document's contents.
        """
        index = self.node.findnonclass((nodes.comment, nodes.system_warning))
        if index is None or len(self.node) > (index + 1):
            return
        candidate = self.node[index]
        if not isinstance(candidate, nodes.section): 
            return
        self.node.attributes.update(candidate.attributes)
        self.node[:] = candidate[:1] + self.node[:index] + candidate[1:]

    def transformfirstfields(self):
        """
        Transform bibliographic field_list fields to elements if found.

        The bibliographic field_list must be the first non-comment child
        (possibly after a title) of the document element itself.
        """
        index = self.node.findnonclass(nodes.comment)
        if index is None:
            return
        candidate = self.node[index]
        if isinstance(candidate, nodes.title):
            titleindex = index
            biblioindex = titleindex + 1
            index = self.node.findnonclass(nodes.comment, titleindex + 1)
            if index is None:
                return
            candidate = self.node[index]
        else:
            biblioindex = 0
            titleindex = None
        if isinstance(candidate, nodes.field_list):
            bibliographic, remainder = self.extractbibliographic(candidate,
                                                                 titleindex)
            if remainder:
                self.node[index] = remainder
            else:
                del self.node[index]
            self.node[biblioindex:biblioindex] = bibliographic

    def extractbibliographic(self, field_list, title):
        nodelist = []
        remainder = []
        bibliofields = self.language.bibliographic_fields
        abstract = None
        for field in field_list:
            try:
                name = field[0][0].astext()
                normedname = normname(name)
                if len(field) != 2 or not bibliofields.has_key(normedname) \
                      or self.checkemptybibliofield(field, name):
                    raise TransformationError
                biblioclass = bibliofields[normedname]
                if issubclass(biblioclass, nodes._TextElement):
                    if self.checkcompoundbibliofield(field, name):
                        raise TransformationError
                    if biblioclass is nodes.title:
                        self.extracttitle(field, name, title, nodelist)
                        title = 1
                    else:
                        nodelist.append(biblioclass('', '',
                                                    *field[1][0].children))
                else:
                    if biblioclass is nodes.authors:
                        self.extractauthors(field, name, nodelist)
                    elif biblioclass is nodes.abstract:
                        if abstract:
                            field[-1] += self.memo.reporter.error(
                                  'There can only be one abstract.')
                            raise TransformationError
                        abstract = nodes.abstract('', *field[1].children)
                    else:
                        nodelist.append(biblioclass('', *field[1].children))
            except TransformationError:
                remainder.append(field)
                continue
        if remainder:
            field_list[:] = remainder
        else:
            field_list = None
        if abstract:
            nodelist.append(abstract)
        return nodelist, field_list

    def checkemptybibliofield(self, field, name):
        if len(field[1]) < 1:
            field[-1] += self.memo.reporter.error(
                  'Cannot extract empty bibliographic field "%s".' % name)
            return 1
        return None

    def checkcompoundbibliofield(self, field, name):
        if len(field[1]) > 1:
            field[-1] += self.memo.reporter.error(
                  'Cannot extract compound title bibliographic '
                  'field "%s".' % name)
            return 1
        if not isinstance(field[1][0], nodes.paragraph):
            field[-1] += self.memo.reporter.error(
                  'Cannot extract bibliographic field "%s" '
                  'containing anything other than a simple paragraph.'
                  % name)
            return 1
        return None

    def extracttitle(self, field, name, title, nodelist):
        if title is not None:
            field[-1] += self.memo.reporter.error(
                  'Multiple document titles (bibliographic field "%s").'
                  % name)
            raise TransformationError
        nodelist.insert(0, nodes.title('', '', *field[1][0].children))

    def extractauthors(self, field, name, nodelist):
        try:
            if len(field[1]) == 1:
                if isinstance(field[1][0], nodes.paragraph):
                    authors = self.authorsfrom1paragraph(field)
                elif isinstance(field[1][0], nodes.bullet_list):
                    authors = self.authorsfrombulletlist(field)
                else:
                    raise TransformationError
            else:
                authors = self.authorsfromparagraphs(field)
            authornodes = [nodes.author('', '', *author)
                           for author in authors if author]
            nodelist.append(nodes.authors('', *authornodes))
        except TransformationError:
            field[-1] += self.memo.reporter.error(
                  'Bibliographic field "%s" incompatible with extraction: '
                  'it must contain either a single paragraph (with authors '
                  'separated by one of "%s"), multiple paragraphs (one per '
                  'author), or a bullet list with one paragraph (one author) '
                  'per item.'
                  % (name, ''.join(self.language.author_separators)))
            raise

    def authorsfrom1paragraph(self, field):
        text = field[1][0].astext().strip()
        if not text:
            raise TransformationError
        for authorsep in self.language.author_separators:
            authornames = text.split(authorsep)
            if len(authornames) > 1:
                break
        authornames = [author.strip() for author in authornames]
        authors = [[nodes.Text(author)] for author in authornames]
        return authors

    def authorsfrombulletlist(self, field):
        authors = []
        for item in field[1][0]:
            if len(item) != 1 or not isinstance(item[0], nodes.paragraph):
                raise TransformationError
            authors.append(item[0].children)
        if not authors:
            raise TransformationError
        return authors

    def authorsfromparagraphs(self, field):
        for item in field[1]:
            if not isinstance(item, nodes.paragraph):
                raise TransformationError
        authors = [item.children for item in field[1]]
        return authors


class NestedStateMachine(StateMachineWS):

    """
    StateMachine run from within other StateMachine runs, to parse nested
    document structures.
    """

    def run(self, inputlines, inputoffset, memo, node, matchtitles=1):
        """
        Parse `inputlines` and return a `dps.nodes.document` instance.

        Extend `StateMachineWS.run()`: set up document-wide data.
        """
        self.matchtitles = matchtitles
        self.memo = memo
        self.node = node
        results = StateMachineWS.run(self, inputlines, inputoffset)
        assert results == [], 'NestedStateMachine.run() results should be empty'
        return results


class RSTState(StateWS):

    """
    reStructuredText State superclass.

    Contains methods used by all State subclasses.
    """

    nestedSM = NestedStateMachine

    def __init__(self, statemachine, debug=0):
        self.nestedSMkwargs = {'stateclasses': stateclasses,
                               'initialstate': 'Body'}
        StateWS.__init__(self, statemachine, debug)

    def gotoline(self, abslineoffset):
        """Jump to input line `abslineoffset`, ignoring jumps past the end."""
        try:
            self.statemachine.gotoline(abslineoffset)
        except IndexError:
            pass

    def bof(self, context):
        """Called at beginning of file."""
        return [], []

    def nestedparse(self, block, inputoffset, node, matchtitles=0,
                      statemachineclass=None, statemachinekwargs=None):
        """
        Create a new StateMachine rooted at `node` and run it over the input
        `block`.
        """
        if statemachineclass is None:
            statemachineclass = self.nestedSM
        if statemachinekwargs is None:
            statemachinekwargs = self.nestedSMkwargs
        statemachine = statemachineclass(debug=self.debug, **statemachinekwargs)
        statemachine.run(block, inputoffset, memo=self.statemachine.memo,
                         node=node, matchtitles=matchtitles)
        statemachine.unlink()
        return statemachine.abslineoffset()

    def nestedlistparse(self, block, inputoffset, node, initialstate,
                        blankfinish, blankfinishstate=None, extrasettings={},
                        matchtitles=0, statemachineclass=None,
                        statemachinekwargs=None):
        """
        Create a new StateMachine rooted at `node` and run it over the input
        `block`. Also keep track of optional intermdediate blank lines and the
        required final one.
        """
        if statemachineclass is None:
            statemachineclass = self.nestedSM
        if statemachinekwargs is None:
            statemachinekwargs = self.nestedSMkwargs.copy()
        statemachinekwargs['initialstate'] = initialstate
        statemachine = statemachineclass(debug=self.debug, **statemachinekwargs)
        if not blankfinishstate:
            blankfinishstate = initialstate
        statemachine.states[blankfinishstate].blankfinish = blankfinish
        for key, value in extrasettings.items():
            setattr(statemachine.states[initialstate], key, value)
        statemachine.run(block, inputoffset, memo=self.statemachine.memo,
                         node=node, matchtitles=matchtitles)
        blankfinish = statemachine.states[blankfinishstate].blankfinish
        statemachine.unlink()
        return statemachine.abslineoffset(), blankfinish

    def section(self, title, source, style, lineno):
        """
        When a new section is reached that isn't a subsection of the current
        section, back up the line count (use previousline(-x)), then raise
        EOFError. The current StateMachine will finish, then the calling
        StateMachine can re-examine the title. This will work its way back up
        the calling chain until the correct section level isreached.

        Alternative: Evaluate the title, store the title info & level, and
        back up the chain until that level is reached. Store in memo? Or
        return in results?
        """
        if self.checksubsection(source, style, lineno):
            self.newsubsection(title, lineno)

    def checksubsection(self, source, style, lineno):
        """
        Check for a valid subsection header. Return 1 (true) or None (false).

        :Exception: `EOFError` when a sibling or supersection encountered.
        """
        memo = self.statemachine.memo
        titlestyles = memo.titlestyles
        mylevel = memo.sectionlevel
        try:                            # check for existing title style
            level = titlestyles.index(style) + 1
        except ValueError:              # new title style
            if len(titlestyles) == memo.sectionlevel: # new subsection
                titlestyles.append(style)
                return 1
            else:                       # not at lowest level
                sw = memo.reporter.severe(
                      'Title level inconsistent at line %s:' % lineno, source)
                self.statemachine.node += sw
                return None
        if level <= mylevel:            # sibling or supersection
            memo.sectionlevel = level   # bubble up to parent section
            # back up 2 lines for underline title, 3 for overline title
            self.statemachine.previousline(len(style) + 1)
            raise EOFError              # let parent section re-evaluate
        if level == mylevel + 1:        # immediate subsection
            return 1
        else:                           # invalid subsection
            sw = memo.reporter.severe(
                  'Title level inconsistent at line %s:' % lineno, source)
            self.statemachine.node += sw
            return None

    def newsubsection(self, title, lineno):
        """Append new subsection to document tree. On return, check level."""
        memo = self.statemachine.memo
        mylevel = memo.sectionlevel
        memo.sectionlevel += 1
        sectionnode = nodes.section()
        self.statemachine.node += sectionnode
        textnodes, warnings = self.inline_text(title, lineno)
        titlenode = nodes.title(title, '', *textnodes)
        sectionnode += titlenode
        sectionnode += warnings
        memo.document.addimplicitlink(normname(titlenode.astext()), sectionnode)
        offset = self.statemachine.lineoffset + 1
        absoffset = self.statemachine.abslineoffset() + 1
        newabsoffset = self.nestedparse(
              self.statemachine.inputlines[offset:], inputoffset=absoffset,
              node=sectionnode, matchtitles=1)
        self.gotoline(newabsoffset)
        if memo.sectionlevel <= mylevel: # can't handle next section?
            raise EOFError              # bubble up to supersection
        # reset sectionlevel; next pass will detect it properly
        memo.sectionlevel = mylevel

    def paragraph(self, lines, lineno):
        """
        Return a list (paragraph & warnings) and a boolean: literal_block next?
        """
        data = '\n'.join(lines).rstrip()
        if data[-2:] == '::':
            if len(data) == 2:
                return [], 1
            elif data[-3] == ' ':
                text = data[:-3].rstrip()
            else:
                text = data[:-1]
            literalnext = 1
        else:
            text = data
            literalnext = 0
        textnodes, warnings = self.inline_text(text, lineno)
        p = nodes.paragraph(data, '', *textnodes)
        return [p] + warnings, literalnext

    inline = Stuff()
    """Patterns and constants used for inline markup recognition."""

    inline.openers = '\'"([{<'
    inline.closers = '\'")]}>'
    inline.start_string_prefix = (r'(?:(?<=^)|(?<=[ \n%s]))'
                                  % re.escape(inline.openers))
    inline.end_string_suffix = (r'(?:(?=$)|(?=[- \n.,:;!?%s]))'
                                % re.escape(inline.closers))
    inline.non_whitespace_before = r'(?<![ \n])'
    inline.non_whitespace_escape_before = r'(?<![ \n\x00])'
    inline.non_whitespace_after = r'(?![ \n])'
    inline.simplename = r'[a-zA-Z0-9](?:[-_.a-zA-Z0-9]*[a-zA-Z0-9])?'
    inline.uric = r"""[-_.!~*'();/:@&=+$,%a-zA-Z0-9]"""
    inline.urilast = r"""[_~/a-zA-Z0-9]"""
    inline.emailc = r"""[-_!~*'{|}/#?^`&=+$%a-zA-Z0-9]"""
    inline.identity = string.maketrans('', '')
    inline.null2backslash = string.maketrans('\x00', '\\')
    inline.patterns = Stuff(
          initial=re.compile(r"""
                             %s             # start-string prefix
                             (
                               (              # start-strings only (group 2):
                                   \*\*         # strong
                                 |
                                   \*           # emphasis
                                   (?!\*)         # but not strong
                                 |
                                   ``           # literal
                               )
                               %s             # no whitespace after
                             |              # *OR*
                               ((?::%s:)?)    # optional role (group 3)
                               (              # start-string (group 4)
                                 `              # interpreted or phrase link
                                 (?!`)          # but not literal
                               )
                               %s             # no whitespace after
                             |              # *OR*
                               (              # whole constructs (group 5):
                                   (%s)(_)      # link name, end-string (6,7)
                                 |
                                   \[           # footnote_reference start,
                                   (            # footnote label (group 8):
                                       \#         # anonymous auto-numbered
                                     |          # *OR*
                                       \#?%s      # (auto-numbered?) label
                                   )
                                   (\]_)        # end-string (group 9)
                               )
                               %s             # end-string suffix
                             )
                             """ % (inline.start_string_prefix,
                                    inline.non_whitespace_after,
                                    inline.simplename,
                                    inline.non_whitespace_after,
                                    inline.simplename,
                                    inline.simplename,
                                    inline.end_string_suffix),
                             re.VERBOSE),
          emphasis=re.compile(inline.non_whitespace_escape_before
                              + r'(\*)' + inline.end_string_suffix),
          strong=re.compile(inline.non_whitespace_escape_before
                            + r'(\*\*)' + inline.end_string_suffix),
          interpreted_or_phrase_link=re.compile(
                '%s(`(:%s:|_)?)%s' % (inline.non_whitespace_escape_before,
                                      inline.simplename,
                                      inline.end_string_suffix)),
          literal=re.compile(inline.non_whitespace_before + '(``)'
                             + inline.end_string_suffix),
          uri=re.compile(
                r"""
                %s                          # start-string prefix
                (
                  (                           # absolute URI (group 2)
                    [a-zA-Z][a-zA-Z0-9.+-]*     # scheme (http, ftp, mailto)
                    :
                    (?:
                      (?:                         # either:
                        (?://?)?                    # hierarchical URI
                        %s*                         # URI characters
                        %s                          # final URI char
                      )
                      (?:                         # optional query
                        \?%s*                       # URI characters
                        %s                          # final URI char
                      )?
                      (?:                         # optional fragment
                        \#%s*                       # URI characters
                        %s                          # final URI char
                      )?
                    )
                  )
                |                           # *OR*
                  (                           # email address (group 3)
                    %s+(?:\.%s+)*               # name
                    @                           # at
                    %s+(?:\.%s*)*               # host
                    %s                          # final URI char
                  )
                )
                %s                          # end-string suffix
                """ % (inline.start_string_prefix,
                       inline.uric, inline.urilast,
                       inline.uric, inline.urilast,
                       inline.uric, inline.urilast,
                       inline.emailc, inline.emailc,
                       inline.emailc, inline.emailc,
                       inline.urilast,
                       inline.end_string_suffix,),
                re.VERBOSE))
    inline.groups = Stuff(initial=Stuff(start=2, role=3, backquote=4, whole=5,
                                        linkname=6, linkend=7, footnotelabel=8,
                                        fnend=9),
                          interpreted_or_phrase_link=Stuff(suffix=2),
                          uri=Stuff(whole=1, absolute=2, email=3))

    def quotedstart(self, match):
        """Return 1 if inline markup start-string is 'quoted', 0 if not."""
        string = match.string
        start = match.start()           # self.inline.groups.initial.start
        end = match.end()               # self.inline.groups.initial.start)
        if start == 0:                  # start-string at beginning of text
            return 0
        prestart = string[start - 1]
        try:
            poststart = string[end]
            if self.inline.openers.index(prestart) \
                  == self.inline.closers.index(poststart):   # quoted
                return 1
        except IndexError:              # start-string at end of text
            return 1
        except ValueError:              # not quoted
            pass
        return 0

    def inlineobj(self, match, lineno, pattern, nodeclass,
                  restorebackslashes=0):
        string = match.string
        matchstart = match.start(self.inline.groups.initial.start)
        matchend = match.end(self.inline.groups.initial.start)
        if self.quotedstart(match):
            return (string[:matchend], [], string[matchend:], [])
        endmatch = pattern.search(string[matchend:])
        if endmatch and endmatch.start(1):  # 1 or more chars
            text = unescape(endmatch.string[:endmatch.start(1)],
                            restorebackslashes)
            rawsource = unescape(string[matchstart:matchend+endmatch.end(1)], 1)
            inlineobj = nodeclass(rawsource, text)
            return (string[:matchstart], [inlineobj],
                    string[matchend:][endmatch.end(1):], [])
        sw = self.statemachine.memo.reporter.warning(
              'Inline %s start-string without end-string '
              'at line %s.' % (nodeclass.__name__, lineno))
        return (string[:matchend], [], string[matchend:], [sw])

    def emphasis(self, match, lineno, pattern=inline.patterns.emphasis):
        return self.inlineobj(match, lineno, pattern, nodes.emphasis)

    def strong(self, match, lineno, pattern=inline.patterns.strong):
        return self.inlineobj(match, lineno, pattern, nodes.strong)

    def interpreted_or_phrase_link(
          self, match, lineno,
          pattern=inline.patterns.interpreted_or_phrase_link,
          rolegroup=inline.groups.initial.role,
          backquote=inline.groups.initial.backquote):
        string = match.string
        matchstart = match.start(backquote)
        matchend = match.end(backquote)
        rolestart = match.start(rolegroup)
        role = match.group(rolegroup)
        position = ''
        if role:
            role = role[1:-1]
            position = 'prefix'
        elif self.quotedstart(match):
            return (string[:matchend], [], string[matchend:], [])
        endmatch = pattern.search(string[matchend:])
        if endmatch and endmatch.start(1):  # 1 or more chars
            escaped = endmatch.string[:endmatch.start(1)]
            text = unescape(escaped, 0)
            rawsource = unescape(
                  string[match.start():matchend+endmatch.end()], 1)
            if rawsource[-1] == '_':
                if role:
                    sw = self.statemachine.memo.reporter.warning(
                          'Mismatch: inline interpreted text start-string '
                          'and role with phrase-link end-string at line %s.'
                          % lineno)
                    return (string[:matchend], [], string[matchend:], [sw])
                return self.phrase_link(
                      string[:matchstart], string[matchend:][endmatch.end():],
                      text, rawsource)
            else:
                return self.interpreted(
                      string[:rolestart], string[matchend:][endmatch.end():],
                      endmatch, role, position, lineno,
                      escaped, rawsource, text)
        sw = self.statemachine.memo.reporter.warning(
              'Inline interpreted text or phrase link start-string '
              'without end-string at line %s.' % lineno)
        return (string[:matchend], [], string[matchend:], [sw])

    def phrase_link(self, before, after, text, rawsource):
        refname = normname(text)
        inlineobj = nodes.link(rawsource, text, refname=normname(text))
        self.statemachine.memo.document.addrefname(refname, inlineobj)
        return (before, [inlineobj], after, [])

    def interpreted(self, before, after, endmatch, role, position, lineno,
                    escaped, rawsource, text,
                    suffix=inline.groups.interpreted_or_phrase_link.suffix):
        if endmatch.group(suffix):
            if role:
                sw = self.statemachine.memo.reporter.warning(
                      'Multiple roles in interpreted text at line %s.'
                      % lineno)
                return (before + rawsource, [], after, [sw])
            role = endmatch.group(suffix)[1:-1]
            position = 'suffix'
        if role:
            atts = {'role': role, 'position': position}
        else:
            atts = {}
        return before, [nodes.interpreted(rawsource, text, **atts)], after, []

    def literal(self, match, lineno, pattern=inline.patterns.literal):
        return self.inlineobj(match, lineno, pattern, nodes.literal,
                              restorebackslashes=1)

    def footnote_reference(self, match, lineno, pattern=None):
        fnname = match.group(self.inline.groups.initial.footnotelabel)
        refname = normname(fnname)
        fnrefnode = nodes.footnote_reference('[%s]_' % fnname)
        if refname[0] == '#':
            refname = refname[1:]
            fnname = fnname[1:]
            self.statemachine.memo.document.addautofootnoteref(refname,
                                                               fnrefnode)
        else:
            fnrefnode += nodes.Text(fnname)
        if refname:
            fnrefnode['refname'] = refname
            self.statemachine.memo.document.addrefname(refname, fnrefnode)
        string = match.string
        matchstart = match.start(self.inline.groups.initial.whole)
        matchend = match.end(self.inline.groups.initial.whole)
        return (string[:matchstart], [fnrefnode], string[matchend:], [])

    def link(self, match, lineno, pattern=None):
        linkname = match.group(self.inline.groups.initial.linkname)
        refname = normname(linkname)
        linknode = nodes.link(linkname + '_', linkname, refname=refname)
        self.statemachine.memo.document.addrefname(refname, linknode)
        string = match.string
        matchstart = match.start(self.inline.groups.initial.whole)
        matchend = match.end(self.inline.groups.initial.whole)
        return (string[:matchstart], [linknode], string[matchend:], [])

    def standalone_uri(self, text, lineno, pattern=inline.patterns.uri,
                       whole=inline.groups.uri.whole,
                       email=inline.groups.uri.email):
        remainder = text
        textnodes = []
        while 1:
            match = pattern.search(remainder)
            if match:
                if match.start(whole) > 0:
                    textnodes.append(nodes.Text(unescape(
                          remainder[:match.start(whole)])))
                if match.group(email):
                    scheme = 'mailto:'
                else:
                    scheme = ''
                text = match.group(whole)
                unescaped = unescape(text, 0)
                textnodes.append(nodes.link(unescape(text, 1),
                                            unescaped,
                                            refuri=scheme + unescaped))
                remainder = remainder[match.end(whole):]
            else:
                if remainder:
                    textnodes.append(nodes.Text(unescape(remainder)))
                break
        return textnodes

    inline.dispatch = {'*': emphasis,
                       '**': strong,
                       '`': interpreted_or_phrase_link,
                       '``': literal,
                       ']_': footnote_reference,
                       '_': link}

    def inline_text(self, text, lineno):
        """
        Return 2 lists: nodes (text and inline elements), and system_warnings.

        A pattern matching start-strings (for emphasis, strong, interpreted,
        phrase link, and literal) or complete constructs (simple link,
        footnote reference) is stored in `self.inline.patterns.initial`. First
        we search for a candidate. When one is found, we check for validity
        (e.g., not a quoted '*' character). If valid, search for the
        corresponding end string if applicable, and check for validity. If not
        found or invalid, raise a warning and ignore the start-string.
        Standalone hyperlinks are found last. Other than that, there is no
        "precedence order" to inline markup, just left-to-right.
        """
        pattern = self.inline.patterns.initial
        dispatch = self.inline.dispatch
        start = self.inline.groups.initial.start - 1
        backquote = self.inline.groups.initial.backquote - 1
        linkend = self.inline.groups.initial.linkend - 1
        fnend = self.inline.groups.initial.fnend - 1
        remaining = escape2null(text)
        processed = []
        unprocessed = []
        warnings = []
        while remaining:
            match = pattern.search(remaining)
            if match:
                groups = match.groups()
                before, inlines, remaining, syswarnings = \
                      dispatch[groups[start] or groups[backquote]
                               or groups[linkend]
                               or groups[fnend]](self, match, lineno)
                unprocessed.append(before)
                warnings += syswarnings
                if inlines:
                    processed += self.standalone_uri(''.join(unprocessed),
                                                     lineno)
                    processed += inlines
                    unprocessed = []
            else:
                break
        remaining = ''.join(unprocessed) + remaining
        if remaining:
            processed += self.standalone_uri(remaining, lineno)
        return processed, warnings

    def unindentwarning(self):
        return self.statemachine.memo.reporter.warning(
              ('Unindent without blank line at line %s.'
                  % (self.statemachine.abslineno() + 1)))


class Body(RSTState):

    """
    Generic classifier of the first line of a block.
    """

    enum = Stuff()
    """Enumerated list parsing information."""

    enum.formatinfo = {
          'parens': Stuff(prefix='(', suffix=')', start=1, end=-1),
          'rparen': Stuff(prefix='', suffix=')', start=0, end=-1),
          'period': Stuff(prefix='', suffix='.', start=0, end=-1)}
    enum.formats = enum.formatinfo.keys()
    enum.sequences = ['arabic', 'loweralpha', 'upperalpha',
                      'lowerroman', 'upperroman'] # ORDERED!
    enum.sequencepats = {'arabic': '[0-9]+',
                         'loweralpha': '[a-z]',
                         'upperalpha': '[A-Z]',
                         'lowerroman': '[ivxlcdm]+',
                         'upperroman': '[IVXLCDM]+',}
    enum.converters = {'arabic': int,
                       'loweralpha':
                       lambda s, zero=(ord('a')-1): ord(s) - zero,
                       'upperalpha':
                       lambda s, zero=(ord('A')-1): ord(s) - zero,
                       'lowerroman':
                       lambda s: roman.fromRoman(s.upper()),
                       'upperroman': roman.fromRoman}

    enum.sequenceregexps = {}
    for sequence in enum.sequences:
        enum.sequenceregexps[sequence] = re.compile(enum.sequencepats[sequence]
                                                + '$')

    tabletoppat = re.compile(r'\+-[-+]+-\+ *$')
    """Matches the top (& bottom) of a table)."""

    tableparser = TableParser()

    pats = {}
    """Fragments of patterns used by transitions."""

    pats['nonalphanum7bit'] = '[!-/:-@[-`{-~]'
    pats['alphanum'] = '[a-zA-Z0-9]'
    pats['alphanumplus'] = '[a-zA-Z0-9_-]'
    pats['enum'] = ('(%(arabic)s|%(loweralpha)s|%(upperalpha)s|%(lowerroman)s'
                    '|%(upperroman)s)' % enum.sequencepats)
    pats['optarg'] = '%(alphanum)s%(alphanumplus)s*' % pats
    pats['shortopt'] = '-%(alphanum)s( %(optarg)s|%(alphanumplus)s+)?' % pats
    pats['longopt'] = '--%(alphanum)s%(alphanumplus)s*([ =]%(optarg)s)?' % pats
    pats['vmsopt'] = '/%(alphanum)s( %(optarg)s|%(alphanumplus)s+)?' % pats
    pats['option'] = '(%(shortopt)s|%(longopt)s|%(vmsopt)s)' % pats

    for format in enum.formats:
        pats[format] = '(?P<%s>%s%s%s)' % (
              format, re.escape(enum.formatinfo[format].prefix),
              pats['enum'], re.escape(enum.formatinfo[format].suffix))

    patterns = {'bullet': r'[-+*]( +|$)',
                'enumerator': r'(%(parens)s|%(rparen)s|%(period)s)( +|$)'
                % pats,
                'fieldmarker': r':[^: ]([^:]*[^: ])?:( +|$)',
                'optionmarker': r'%(option)s(, %(option)s)*(  +| ?$)' % pats,
                'doctest': r'>>>( +|$)',
                'tabletop': tabletoppat,
                'explicit_markup': r'\.\.( +|$)',
                'overline': r'(%(nonalphanum7bit)s)\1\1\1+ *$' % pats,
                'rfc822': r'[!-9;-~]+:( +|$)',
                'text': r''}
    initialtransitions = ['bullet',
                          'enumerator',
                          'fieldmarker',
                          'optionmarker',
                          'doctest',
                          'tabletop',
                          'explicit_markup',
                          'overline',
                          'text']

    def indent(self, match, context, nextstate):
        """Block quote."""
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getindented()
        blockquote = self.block_quote(indented, lineoffset)
        self.statemachine.node += blockquote
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        return context, nextstate, []

    def block_quote(self, indented, lineoffset):
        blockquote = nodes.block_quote()
        self.nestedparse(indented, lineoffset, blockquote)
        return blockquote

    def bullet(self, match, context, nextstate):
        """Bullet list item."""
        bulletlist = nodes.bullet_list()
        self.statemachine.node += bulletlist
        bulletlist['bullet'] = match.string[0]
        i, blankfinish = self.list_item(match.end())
        bulletlist += i
        offset = self.statemachine.lineoffset + 1   # next line
        newlineoffset, blankfinish = self.nestedlistparse(
              self.statemachine.inputlines[offset:],
              inputoffset=self.statemachine.abslineoffset() + 1,
              node=bulletlist, initialstate='BulletList',
              blankfinish=blankfinish)
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        self.gotoline(newlineoffset)
        return [], nextstate, []

    def list_item(self, indent):
        indented, lineoffset, blankfinish = \
              self.statemachine.getknownindented(indent)
        listitem = nodes.list_item('\n'.join(indented))
        if indented:
            self.nestedparse(indented, inputoffset=lineoffset, node=listitem)
        return listitem, blankfinish

    def enumerator(self, match, context, nextstate):
        """Enumerated List Item"""
        format, sequence, text, ordinal = self.parseenumerator(match)
        if ordinal is None:
            sw = self.statemachine.memo.reporter.error(
                  ('Enumerated list start value invalid at line %s: '
                   '%r (sequence %r)' % (self.statemachine.abslineno(),
                                         text, sequence)))
            self.statemachine.node += sw
            indented, lineoffset, blankfinish = \
                  self.statemachine.getknownindented(match.end())
            bq = self.block_quote(indented, lineoffset)
            self.statemachine.node += bq
            if not blankfinish:
                self.statemachine.node += self.unindentwarning()
            return [], nextstate, []
        if ordinal != 1:
            sw = self.statemachine.memo.reporter.information(
                  ('Enumerated list start value not ordinal-1 at line %s: '
                      '%r (ordinal %s)' % (self.statemachine.abslineno(),
                                           text, ordinal)))
            self.statemachine.node += sw
        enumlist = nodes.enumerated_list()
        self.statemachine.node += enumlist
        enumlist['enumtype'] = sequence
        enumlist['start'] = text
        enumlist['prefix'] = self.enum.formatinfo[format].prefix
        enumlist['suffix'] = self.enum.formatinfo[format].suffix
        listitem, blankfinish = self.list_item(match.end())
        enumlist += listitem
        offset = self.statemachine.lineoffset + 1   # next line
        newlineoffset, blankfinish = self.nestedlistparse(
              self.statemachine.inputlines[offset:],
              inputoffset=self.statemachine.abslineoffset() + 1,
              node=enumlist, initialstate='EnumeratedList',
              blankfinish=blankfinish,
              extrasettings={'lastordinal': ordinal, 'format': format})
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        self.gotoline(newlineoffset)
        return [], nextstate, []

    def parseenumerator(self, match, expectedsequence=None):
        """
        Analyze an enumerator and return the results.

        :Return:
            - the enumerator format ('period', 'parens', or 'rparen'),
            - the sequence used ('arabic', 'loweralpha', 'upperroman', etc.),
            - the text of the enumerator, stripped of formatting, and
            - the ordinal value of the enumerator ('a' -> 1, 'ii' -> 2, etc.;
              ``None`` is returned for invalid enumerator text).

        The enumerator format has already been determined by the regular
        expression match. If `expectedsequence` is given, that sequence is
        tried first. If not, we check for Roman numeral 1. This way,
        single-character Roman numerals (which are also alphabetical) can be
        matched. If no sequence has been matched, all sequences are checked in
        order.
        """
        groupdict = match.groupdict()
        sequence = ''
        for format in self.enum.formats:
            if groupdict[format]:       # was this the format matched?
                break                   # yes; keep `format`
        else:                           # shouldn't happen
            raise ParserError, 'enumerator format not matched'
        text = groupdict[format][self.enum.formatinfo[format].start
                                 :self.enum.formatinfo[format].end]
        if expectedsequence:
            try:
                if self.enum.sequenceregexps[expectedsequence].match(text):
                    sequence = expectedsequence
            except KeyError:            # shouldn't happen
                raise ParserError, 'unknown sequence: %s' % sequence
        else:
            if text == 'i':
                sequence = 'lowerroman'
            elif text == 'I':
                sequence = 'upperroman'
        if not sequence:
            for sequence in self.enum.sequences:
                if self.enum.sequenceregexps[sequence].match(text):
                    break
            else:                       # shouldn't happen
                raise ParserError, 'enumerator sequence not matched'
        try:
            ordinal = self.enum.converters[sequence](text)
        except roman.InvalidRomanNumeralError:
            ordinal = None
        return format, sequence, text, ordinal

    def fieldmarker(self, match, context, nextstate):
        """Field list item."""
        fieldlist = nodes.field_list()
        self.statemachine.node += fieldlist
        field, blankfinish = self.field(match)
        fieldlist += field
        offset = self.statemachine.lineoffset + 1   # next line
        newlineoffset, blankfinish = self.nestedlistparse(
              self.statemachine.inputlines[offset:],
              inputoffset=self.statemachine.abslineoffset() + 1,
              node=fieldlist, initialstate='FieldList',
              blankfinish=blankfinish)
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        self.gotoline(newlineoffset)
        return [], nextstate, []

    def field(self, match):
        name, args = self.parsefieldmarker(match)
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        fieldnode = nodes.field()
        fieldnode += nodes.field_name(name, name)
        for arg in args:
            fieldnode += nodes.field_argument(arg, arg)
        fieldbody = nodes.field_body('\n'.join(indented))
        fieldnode += fieldbody
        if indented:
            self.nestedparse(indented, inputoffset=lineoffset, node=fieldbody)
        return fieldnode, blankfinish

    def parsefieldmarker(self, match):
        """Extract & return name & argument list from a field marker match."""
        field = match.string[1:]        # strip off leading ':'
        field = field[:field.find(':')] # strip off trailing ':' etc.
        tokens = field.split()
        return tokens[0], tokens[1:]    # first == name, others == args

    def optionmarker(self, match, context, nextstate):
        """Option list item."""
        optionlist = nodes.option_list()
        self.statemachine.node += optionlist
        try:
            listitem, blankfinish = self.option_list_item(match)
        except MarkupError, detail:     # shouldn't happen; won't match pattern
            sw = self.statemachine.memo.reporter.error(
                  ('Invalid option list marker at line %s: %s'
                      % (self.statemachine.abslineno(), detail)))
            self.statemachine.node += sw
            indented, indent, lineoffset, blankfinish = \
                  self.statemachine.getfirstknownindented(match.end())
            blockquote = self.block_quote(indented, lineoffset)
            self.statemachine.node += blockquote
            if not blankfinish:
                self.statemachine.node += self.unindentwarning()
            return [], nextstate, []
        optionlist += listitem
        offset = self.statemachine.lineoffset + 1   # next line
        newlineoffset, blankfinish = self.nestedlistparse(
              self.statemachine.inputlines[offset:],
              inputoffset=self.statemachine.abslineoffset() + 1,
              node=optionlist, initialstate='OptionList',
              blankfinish=blankfinish)
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        self.gotoline(newlineoffset)
        return [], nextstate, []

    def option_list_item(self, match):
        options = self.parseoptionmarker(match)
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        optionlistitem = nodes.option_list_item('', *options)
        description = nodes.description('\n'.join(indented))
        optionlistitem += description
        if indented:
            self.nestedparse(indented, inputoffset=lineoffset, node=description)
        return optionlistitem, blankfinish

    def parseoptionmarker(self, match):
        """
        Return a list of `node.option` objects from an option marker match.

        :Exception: `MarkupError` for invalid option markers.
        """
        optlist = []
        options = match.group().rstrip().split(', ')
        for optionstring in options:
            option = nodes.option(optionstring)
            tokens = optionstring.split()
            if tokens[0][:2] == '--':
                tokens[:1] = tokens[0].split('=')
            elif tokens[0][:1] in '-/':
                if len(tokens[0]) > 2:
                    tokens[:1] = [tokens[0][:2], tokens[0][2:]]
            else:
                raise MarkupError('not an option marker: %r' % optionstring)
            if 0 < len(tokens) <= 2:
                if tokens[0][:2] == '--':
                    option += nodes.long_option(tokens[0], tokens[0])
                elif tokens[0][:1] == '-':
                    option += nodes.short_option(tokens[0], tokens[0])
                elif tokens[0][:1] == '/':
                    option += nodes.vms_option(tokens[0], tokens[0])
                if len(tokens) > 1:
                    option += nodes.option_argument(tokens[1], tokens[1])
                optlist.append(option)
            else:
                raise MarkupError('wrong numer of option tokens (=%s), '
                                  'should be 1 or 2: %r' % (len(tokens),
                                                            optionstring))
        return optlist

    def doctest(self, match, context, nextstate):
        data = '\n'.join(self.statemachine.gettextblock())
        self.statemachine.node += nodes.doctest_block(data, data)
        return [], nextstate, []

    def tabletop(self, match, context, nextstate):
        """Top border of a table."""
        nodelist, blankfinish = self.table()
        self.statemachine.node += nodelist
        if not blankfinish:
            sw = self.statemachine.memo.reporter.warning(
                  'Blank line required after table at line %s.'
                  % (self.statemachine.abslineno() + 1))
            self.statemachine.node += sw
        return [], nextstate, []

    def table(self):
        """Temporarily parse a table as a literal_block."""
        block, warnings, blankfinish = self.isolatetable()
        if block:
            try:
                tabledata = self.tableparser.parse(block)
                tableline = self.statemachine.abslineno() - len(block) + 1
                table = self.buildtable(tabledata, tableline)
                nodelist = [table] + warnings
            except TableMarkupError, detail:
                nodelist = self.malformedtable(block, str(detail)) + warnings
        else:
            nodelist = warnings
        return nodelist, blankfinish

    def isolatetable(self):
        warnings = []
        blankfinish = 1
        try:
            block = self.statemachine.getunindented()
        except statemachine.UnexpectedIndentationError, instance:
            block, lineno = instance.args
            warnings.append(self.statemachine.memo.reporter.error(
                  'Unexpected indentation at line %s.' % lineno))
            blankfinish = 0
        width = len(block[0].strip())
        for i in range(len(block)):
            block[i] = block[i].strip()
            if block[i][0] not in '+|': # check left edge
                blankfinish = 0
                self.statemachine.previousline(len(block) - i)
                del block[i:]
                break
        if not self.tabletoppat.match(block[-1]): # find bottom
            blankfinish = 0
            # from second-last to third line of table:
            for i in range(len(block) - 2, 1, -1):
                if self.tabletoppat.match(block[i]):
                    self.statemachine.previousline(len(block) - i + 1)
                    del block[i+1:]
                    break
            else:
                warnings.extend(self.malformedtable(block))
                return [], warnings, blankfinish
        for i in range(len(block)):     # check right edge
            if len(block[i]) != width or block[i][-1] not in '+|':
                warnings.extend(self.malformedtable(block))
                return [], warnings, blankfinish
        return block, warnings, blankfinish

    def malformedtable(self, block, detail=''):
        data = '\n'.join(block)
        message = 'Malformed table at line %s; formatting as a ' \
                  'literal block.' % (self.statemachine.abslineno()
                                      - len(block) + 1)
        if detail:
            message += '\n' + detail
        nodelist = [self.statemachine.memo.reporter.error(message),
                    nodes.literal_block(data, data)]
        return nodelist

    def buildtable(self, tabledata, tableline):
        colspecs, headrows, bodyrows = tabledata
        table = nodes.table()
        tgroup = nodes.tgroup(cols=len(colspecs))
        table += tgroup
        for colspec in colspecs:
            tgroup += nodes.colspec(colwidth=colspec)
        if headrows:
            thead = nodes.thead()
            tgroup += thead
            for row in headrows:
                thead += self.buildtablerow(row, tableline)
        tbody = nodes.tbody()
        tgroup += tbody
        for row in bodyrows:
            tbody += self.buildtablerow(row, tableline)
        return table

    def buildtablerow(self, rowdata, tableline):
        row = nodes.row()
        for cell in rowdata:
            if cell is None:
                continue
            morerows, morecols, offset, cellblock = cell
            attributes = {}
            if morerows:
                attributes['morerows'] = morerows
            if morecols:
                attributes['morecols'] = morecols
            entry = nodes.entry(**attributes)
            row += entry
            if ''.join(cellblock):
                self.nestedparse(cellblock, inputoffset=tableline+offset,
                                 node=entry)
        return row


    explicit = Stuff()
    """Patterns and constants used for explicit markup recognition."""

    explicit.patterns = Stuff(
          target=re.compile(r"""
                            (`?)        # optional open quote
                            (?!=[ ])    # first char. not space
                            (           # hyperlink name
                              .+?
                            )
                            %s          # not whitespace or escape
                            \1          # close quote if open quote used
                            :           # end of hyperlink name
                            (?:[ ]+|$)    # followed by whitespace
                            """ % RSTState.inline.non_whitespace_escape_before,
                            re.VERBOSE),)
    explicit.groups = Stuff(
          target=Stuff(quote=1, name=2))

    def footnote(self, match):
        indented, indent, offset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        label = match.group(1)
        name = normname(label)
        footnotenode = nodes.footnote('\n'.join(indented))
        if name[0] == '#':
            name = name[1:]
            self.statemachine.memo.document.addautofootnote(name, footnotenode)
        else:
            footnotenode += nodes.label('', label)
        if name:
            self.statemachine.memo.document.addimplicitlink(name, footnotenode)
        if indented:
            self.nestedparse(indented, inputoffset=offset, node=footnotenode)
        return [footnotenode], blankfinish

    def hyperlink_target(self, match,
                         pattern=explicit.patterns.target,
                         namegroup=explicit.groups.target.name):
        escaped = escape2null(match.string)
        targetmatch = pattern.match(escaped[match.end():])
        if not targetmatch:
            raise MarkupError('malformed hyperlink target at line %s.'
                              % self.statemachine.abslineno())
        referencestart = match.end() + targetmatch.end()
        name = normname(unescape(targetmatch.group(namegroup)))
        block, indent, offset, blankfinish \
              = self.statemachine.getfirstknownindented(referencestart,
                                                        uptoblank=1)
        reference = ''.join([line.strip() for line in block])
        blocktext = match.string[:referencestart] + '\n'.join(block)
        nodelist = []
        if reference.find(' ') != -1:
            warning = self.statemachine.memo.reporter.warning(
                  'Hyperlink target at line %s contains whitespace. '
                  'Perhaps a footnote was intended?'
                  % (self.statemachine.abslineno() - len(block) + 1))
            warning += nodes.literal_block(blocktext, blocktext)
            nodelist.append(warning)
        else:
            target = nodes.target(blocktext, reference)
            if reference:
                self.statemachine.memo.document.addindirectlink(
                      name, reference, target, self.statemachine.node)
            else:
                self.statemachine.memo.document.addexplicitlink(
                      name, target, self.statemachine.node)
            nodelist.append(target)
        return nodelist, blankfinish

    def directive(self, match):
        typename = match.group(1)
        directivefunction = directives.directive(
              typename, self.statemachine.memo.language)
        data = match.string[match.end():].strip() or None
        if directivefunction:
            return directivefunction(match, typename, data, self,
                                     self.statemachine)
        else:
            return self.unknowndirective(typename, data)

    def unknowndirective(self, typename, data):
        lineno = self.statemachine.abslineno()
        indented, indent, offset, blankfinish = \
              self.statemachine.getfirstknownindented(0)
        margin = ' ' * indent
        for i in range(1, len(indented)):
            indented[i] = margin + indented[i]
        text = '\n'.join(indented)
        error = self.statemachine.memo.reporter.error(
              'Unknown directive type "%s" at line %s.\n'
              'Rendering the directive as a literal block.' % (typename,
                                                               lineno))
        literalblock = nodes.literal_block(text, text)
        nodelist = [error, literalblock]
        return nodelist, blankfinish

    def comment(self, match):
        if not match.string[match.end():].strip() \
              and self.statemachine.nextlineblank(): # an empty comment?
            return [nodes.comment()], 1 # "A tiny but practical wart."
        indented, indent, offset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        text = '\n'.join(indented)
        return [nodes.comment(text, text)], blankfinish

    explicit.constructs = [
          (footnote,
           re.compile(r"""
                      \.\.[ ]+          # explicit markup start
                      \[
                      (                 # footnote reference identifier:
                          \#              # anonymous auto-numbered reference
                        |               # *OR*
                          \#?%s           # (auto-numbered?) footnote label
                      )
                      \]
                      (?:[ ]+|$)        # whitespace or end of line
                      """ % RSTState.inline.simplename, re.VERBOSE)),
          (hyperlink_target,
           re.compile(r"""
                      \.\.[ ]+          # explicit markup start
                      _                 # target indicator
                      """, re.VERBOSE)),
          (directive,
           re.compile(r"""
                      \.\.[ ]+          # explicit markup start
                      (%s)              # directive name
                      ::                # directive delimiter
                      (?:[ ]+|$)        # whitespace or end of line
                      """ % RSTState.inline.simplename, re.VERBOSE))]

    def explicit_markup(self, match, context, nextstate):
        """Footnotes, hyperlink targets, directives, comments."""
        nodelist, blankfinish = self.explicit_construct(match)
        self.statemachine.node += nodelist
        offset = self.statemachine.lineoffset + 1   # next line
        newlineoffset, blankfinish = self.nestedlistparse(
              self.statemachine.inputlines[offset:],
              inputoffset=self.statemachine.abslineoffset() + 1,
              node=self.statemachine.node, initialstate='Explicit',
              blankfinish=blankfinish)
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        self.gotoline(newlineoffset)
        return [], nextstate, []

    def explicit_construct(self, match,
                           constructs=explicit.constructs):
        """Determine which explicit construct this is, parse & return it."""
        errors = []
        for method, pattern in constructs:
            expmatch = pattern.match(match.string)
            if expmatch:
                try:
                    return method(self, expmatch)
                except MarkupError, detail:
                    errors.append(
                          self.statemachine.memo.reporter.warning(
                          detail.__class__.__name__ + ': ' + str(detail)))
                    break
        nodelist, blankfinish = self.comment(match)
        return nodelist + errors, blankfinish

    def overline(self, match, context, nextstate):
        """Section title."""
        makesection = 1
        lineno = self.statemachine.abslineno()
        if not self.statemachine.matchtitles:
            sw = self.statemachine.memo.reporter.severe(
                  'Unexpected section title at line %s.' % lineno)
            self.statemachine.node += sw
            return [], nextstate, []
        title = underline = ''
        try:
            title = self.statemachine.nextline()
            underline = self.statemachine.nextline()
        except IndexError:
            sw = self.statemachine.memo.reporter.severe(
                  'Incomplete section title at line %s.' % lineno)
            self.statemachine.node += sw
            makesection = 0
        source = '%s\n%s\n%s' % (match.string, title, underline)
        overline = match.string.rstrip()
        underline = underline.rstrip()
        if not self.transitions['overline'][0].match(underline):
            sw = self.statemachine.memo.reporter.severe(
                  'Missing underline for overline at line %s.' % lineno)
            self.statemachine.node += sw
            makesection = 0
        elif overline != underline:
            sw = self.statemachine.memo.reporter.severe(
                  'Title overline & underline mismatch at ' 'line %s.'
                  % lineno)
            self.statemachine.node += sw
            makesection = 0
        title = title.rstrip()
        if len(title) > len(overline):
            self.statemachine.node += \
                  self.statemachine.memo.reporter.information(
                  'Title overline too short at line %s.'% lineno)
        if makesection:
            style = (overline[0], underline[0])
            self.section(title.lstrip(), source, style, lineno + 1)
        return [], nextstate, []

    def text(self, match, context, nextstate):
        """Titles, definition lists, paragraphs."""
        return [match.string], 'Text', []


class SpecializedBody(Body):

    """
    Superclass for second and subsequent compound element members.

    All transition methods are disabled. Override individual methods in
    subclasses to re-enable.
    """

    def invalid_input(self, match=None, context=None, nextstate=None):
        """Not a compound element member. Abort this state machine."""
        self.statemachine.previousline()  # back up so parent SM can reassess
        raise EOFError

    indent = invalid_input
    bullet = invalid_input
    enumerator = invalid_input
    fieldmarker = invalid_input
    optionmarker = invalid_input
    doctest = invalid_input
    tabletop = invalid_input
    explicit_markup = invalid_input
    overline = invalid_input
    text = invalid_input


class BulletList(SpecializedBody):

    """Second and subsequent bullet_list list_items."""

    def bullet(self, match, context, nextstate):
        """Bullet list item."""
        if match.string[0] != self.statemachine.node['bullet']:
            # different bullet: new list
            self.invalid_input()
        listitem, blankfinish = self.list_item(match.end())
        self.statemachine.node += listitem
        self.blankfinish = blankfinish
        return [], 'BulletList', []


class DefinitionList(SpecializedBody):

    """Second and subsequent definition_list_items."""

    def text(self, match, context, nextstate):
        """Definition lists."""
        return [match.string], 'Definition', []


class EnumeratedList(SpecializedBody):

    """Second and subsequent enumerated_list list_items."""

    def enumerator(self, match, context, nextstate):
        """Enumerated list item."""
        format, sequence, text, ordinal = self.parseenumerator(
              match, self.statemachine.node['enumtype'])
        if (sequence != self.statemachine.node['enumtype'] or
            format != self.format or
            ordinal != self.lastordinal + 1):
            # different enumeration: new list
            self.invalid_input()
        listitem, blankfinish = self.list_item(match.end())
        self.statemachine.node += listitem
        self.blankfinish = blankfinish
        self.lastordinal = ordinal
        return [], 'EnumeratedList', []


class FieldList(SpecializedBody):

    """Second and subsequent field_list fields."""

    def fieldmarker(self, match, context, nextstate):
        """Field list field."""
        field, blankfinish = self.field(match)
        self.statemachine.node += field
        self.blankfinish = blankfinish
        return [], 'FieldList', []


class OptionList(SpecializedBody):

    """Second and subsequent option_list option_list_items."""

    def optionmarker(self, match, context, nextstate):
        """Option list item."""
        try:
            optionlistitem, blankfinish = self.option_list_item(match)
        except MarkupError, detail:
            self.invalid_input()
        self.statemachine.node += optionlistitem
        self.blankfinish = blankfinish
        return [], 'OptionList', []


class RFC822List(SpecializedBody):

    """Second and subsequent RFC822 field_list fields."""

    pass


class Explicit(SpecializedBody):

    """Second and subsequent explicit markup construct."""

    def explicit_markup(self, match, context, nextstate):
        """Footnotes, hyperlink targets, directives, comments."""
        nodelist, blankfinish = self.explicit_construct(match)
        self.statemachine.node += nodelist
        self.blankfinish = blankfinish
        return [], nextstate, []


class Text(RSTState):

    """
    Classifier of second line of a text block.

    Could be a paragraph, a definition list item, or a title.
    """

    patterns = {'underline': r'([!-/:-@[-`{-~])\1\1\1+ *$',
                'text': r''}
    initialtransitions = [('underline', 'Body'), ('text', 'Body')]

    def blank(self, match, context, nextstate):
        """End of paragraph."""
        paragraph, literalnext = self.paragraph(
              context, self.statemachine.abslineno() - 1)
        self.statemachine.node += paragraph
        if literalnext:
            self.statemachine.node += self.literal_block()
        return [], 'Body', []

    def eof(self, context):
        if context:
            paragraph, literalnext = self.paragraph(
                  context, self.statemachine.abslineno() - 1)
            self.statemachine.node += paragraph
            if literalnext:
                self.statemachine.node += self.literal_block()
        return []

    def indent(self, match, context, nextstate):
        """Definition list item."""
        definitionlist = nodes.definition_list()
        definitionlistitem, blankfinish = self.definition_list_item(context)
        definitionlist += definitionlistitem
        self.statemachine.node += definitionlist
        offset = self.statemachine.lineoffset + 1   # next line
        newlineoffset, blankfinish = self.nestedlistparse(
              self.statemachine.inputlines[offset:],
              inputoffset=self.statemachine.abslineoffset() + 1,
              node=definitionlist, initialstate='DefinitionList',
              blankfinish=blankfinish, blankfinishstate='Definition')
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        self.gotoline(newlineoffset)
        return [], 'Body', []

    def underline(self, match, context, nextstate):
        """Section title."""
        lineno = self.statemachine.abslineno()
        if not self.statemachine.matchtitles:
            sw = self.statemachine.memo.reporter.severe(
                  'Unexpected section title at line %s.' % lineno)
            self.statemachine.node += sw
            return [], nextstate, []
        title = context[0].rstrip()
        underline = match.string.rstrip()
        source = title + '\n' + underline
        if len(title) > len(underline):
            self.statemachine.node += \
                  self.statemachine.memo.reporter.information(
                  'Title underline too short at line %s.' % lineno)
        style = underline[0]
        context[:] = []
        self.section(title, source, style, lineno - 1)
        return [], nextstate, []

    def text(self, match, context, nextstate):
        """Paragraph."""
        startline = self.statemachine.abslineno() - 1
        sw = None
        try:
            block = self.statemachine.getunindented()
        except statemachine.UnexpectedIndentationError, instance:
            block, lineno = instance.args
            sw = self.statemachine.memo.reporter.error(
                  'Unexpected indentation at line %s.' % lineno)
        lines = context + block
        paragraph, literalnext = self.paragraph(lines, startline)
        self.statemachine.node += paragraph
        self.statemachine.node += sw
        if literalnext:
            try:
                self.statemachine.nextline()
            except IndexError:
                pass
            self.statemachine.node += self.literal_block()
        return [], nextstate, []

    def literal_block(self):
        """Return a list of nodes."""
        indented, indent, offset, blankfinish = \
              self.statemachine.getindented()
        nodelist = []
        if indented:
            data = '\n'.join(indented)
            nodelist.append(nodes.literal_block(data, data))
            if not blankfinish:
                nodelist.append(self.unindentwarning())
        else:
            nodelist.append(self.statemachine.memo.reporter.warning(
                  'Literal block expected at line %s; none found.'
                  % self.statemachine.abslineno()))
        return nodelist

    def definition_list_item(self, termline):
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getindented()
        definitionlistitem = nodes.definition_list_item('\n'.join(termline
                                                                  + indented))
        termlist, warnings = self.term(termline,
                                       self.statemachine.abslineno() - 1)
        definitionlistitem += termlist
        definition = nodes.definition('', *warnings)
        definitionlistitem += definition
        if termline[0][-2:] == '::':
            definition += self.statemachine.memo.reporter.information(
                  'Blank line missing before literal block? Interpreted as a '
                  'definition list item. At line %s.' % (lineoffset + 1))
        self.nestedparse(indented, inputoffset=lineoffset, node=definition)
        return definitionlistitem, blankfinish

    def term(self, lines, lineno):
        """Return a definition_list's term and optional classifier."""
        assert len(lines) == 1
        nodelist = []
        parts = lines[0].split(' : ', 1)  # split into 1 or 2 parts
        termpart = parts[0].rstrip()
        textnodes, warnings = self.inline_text(termpart, lineno)
        nodelist = [nodes.term(termpart, '', *textnodes)]
        if len(parts) == 2:
            classifierpart = parts[1].lstrip()
            textnodes, cpwarnings = self.inline_text(classifierpart, lineno)
            nodelist.append(nodes.classifier(classifierpart, '', *textnodes))
            warnings += cpwarnings
        return nodelist, warnings


class SpecializedText(Text):

    """
    Superclass for second and subsequent lines of Text-variants.

    All transition methods are disabled. Override individual methods in
    subclasses to re-enable.
    """

    def eof(self, context):
        """Not a definition."""
        self.statemachine.previousline(2) # back up so parent SM can reassess
        return []

    def invalid_input(self, match=None, context=None, nextstate=None):
        """Not a compound element member. Abort this state machine."""
        raise EOFError

    blank = invalid_input
    indent = invalid_input
    underline = invalid_input
    text = invalid_input


class Definition(SpecializedText):

    """Second line of potential definition_list_item."""

    def indent(self, match, context, nextstate):
        """Definition list item."""
        definitionlistitem, blankfinish = self.definition_list_item(context)
        self.statemachine.node += definitionlistitem
        self.blankfinish = blankfinish
        return [], 'DefinitionList', []


stateclasses = [Body, BulletList, DefinitionList, EnumeratedList, FieldList,
                OptionList, RFC822List, Explicit, Text, Definition]
"""Standard set of State classes used to start `RSTStateMachine`."""


def escape2null(text):
    """Return a string with escape-backslashes converted to nulls."""
    parts = []
    start = 0
    while 1:
        found = text.find('\\', start)
        if found == -1:
            parts.append(text[start:])
            return ''.join(parts)
        parts.append(text[start:found])
        parts.append('\x00' + text[found+1:found+2])
        start = found + 2               # skip character after escape

def unescape(text, restorebackslashes=0):
    """Return a string with nulls removed or restored to backslashes."""
    if restorebackslashes:
        return text.translate(RSTState.inline.null2backslash)
    else:
        return text.translate(RSTState.inline.identity, '\x00')

def normname(name):
    """Return a case- and whitespace-normalized name."""
    return ' '.join(name.lower().split())
