"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.13 $
:Date: $Date: 2001/09/04 04:13:27 $
:Copyright: This module has been placed in the public domain.

This is the ``dps.parsers.restructuredtext.states`` module, the core of the
reStructuredText parser. It defines the following:

:Classes:
    - `RSTStateMachine`: reStructuredText's customized StateMachine.
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
    - `TableParser`: Parses tables.

:Exception classes:
    - `MarkupError`
    - `ParserError`

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

   B. Others trigger the creation of a subordinate state machine, whose job is
      to parse a compound construct ('indent' for a block quote, 'bullet' for
      a bullet list, 'overline' for a section [first checking for a valid
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
        inter-element blank lines is also handled.

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

import sys, re, string
from dps import nodes, statemachine, utils, roman
from dps.statemachine import StateMachineWS, StateWS

__all__ = ['RSTStateMachine', 'MarkupError', 'ParserError']


class MarkupError(Exception): pass
class ParserError(Exception): pass


class Stuff:

    """Stores a bunch of stuff for dotted-attribute access."""

    def __init__(self, **keywordargs):
        self.__dict__.update(keywordargs)


class RSTStateMachine(StateMachineWS):

    """
    reStructuredText's customized StateMachine.
    """

    def run(self, inputlines, inputoffset=0,
            warninglevel=1, errorlevel=3,
            memo=None, node=None, matchtitles=1):
        """
        Parse `inputlines` and return a `dps.nodes.document` instance.

        Extend `StateMachineWS.run()`: set up document-wide data.

        When called initially (from outside, to parse a document), `memo` and
        `node` must *not* be supplied. When subsequently called (internally,
        to parse a portion of the document), `memo` and `node` *must* be
        supplied.
        """
        self.warninglevel = warninglevel
        self.errorlevel = errorlevel
        self.matchtitles = matchtitles
        if memo is None:
            errorist = utils.Errorist(warninglevel, errorlevel)
            docroot = nodes.document(errorist)
            self.memo = Stuff(document=docroot,
                              errorist=errorist,
                              titlestyles=[],
                              sectionlevel=0,
                              matchfirstfields=1)
            self.node = docroot
        else:
            if self.debug:
                print >>sys.stderr, ('\nRSTStateMachine (recursive): node=%r'
                                     % node)
            self.memo = memo
            self.node = node
        if not self.memo.matchfirstfields:
            for state in self.states.values:
                if state.transitions.has_key('firstfield'):
                    state.removetransition('firstfield')
        results = StateMachineWS.run(self, inputlines, inputoffset)
        assert results == [], 'RSTStateMachine results should be empty.'
        if memo is None:                # initial (external) call
            self.node = self.memo = None
            return docroot


class RSTState(StateWS):

    """reStructuredText State superclass."""

    def __init__(self, statemachine, debug=0):
        self.indentSMkwargs = {'stateclasses': stateclasses,
                               'initialstate': 'Body'}
        StateWS.__init__(self, statemachine, debug)

    def bof(self, context):
        return [], []

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
        # XXX need to catch title as first element (after comments),
        # so firstfields will work
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
                if self.debug:
                    print >>sys.stderr, ('\nstates.RSTState.checksubsection: '
                                         'mylevel=%s, new level=%s (new)'
                                         % (mylevel, len(titlestyles)))
                return 1
            else:                       # not at lowest level
                sw = memo.errorist.strong_system_warning(
                      'ABORT', 'Title level inconsistent at line %s:' % lineno,
                      source)
                self.statemachine.node += sw
                return None
        if self.debug:
            print >>sys.stderr, ('\nstates.RSTState.checksubsection: '
                                 'mylevel=%s, new level=%s (exists)'
                                 % (mylevel, level))
        if level <= mylevel:            # sibling or supersection
            memo.sectionlevel = level   # bubble up to parent section
            # back up 2 lines for underline title, 3 for overline title
            self.statemachine.previousline(len(style) + 1)
            raise EOFError              # let parent section re-evaluate
        if level == mylevel + 1:        # immediate subsection
            return 1
        else:                           # invalid subsection
            sw = memo.errorist.strong_system_warning(
                  'ABORT', 'Title level inconsistent at line %s:' % lineno,
                  source)
            self.statemachine.node += sw
            return None

    def newsubsection(self, title, lineno):
        """Append new subsection to document tree. On return, check level."""
        memo = self.statemachine.memo
        mylevel = memo.sectionlevel
        memo.sectionlevel += 1
        if self.debug:
            print >>sys.stderr, ('\nstates.RSTState.newsubsection: starting a '
                                 'new subsection (level %s)' % (mylevel + 1))
        s = nodes.section()
        self.statemachine.node += s
        textnodes, warnings = self.inline_text(title, lineno)
        titlenode = nodes.title(title, '', *textnodes)
        s += titlenode
        s += warnings
        memo.document.addimplicitlink(normname(titlenode.astext()), s)
        sm = RSTStateMachine(stateclasses=stateclasses, initialstate='Body',
                             debug=self.debug)
        offset = self.statemachine.lineoffset + 1
        absoffset = self.statemachine.abslineoffset() + 1
        sm.run(self.statemachine.inputlines[offset:], inputoffset=absoffset,
               memo=memo, node=s, matchtitles=1)
        sm.unlink()
        if self.debug:
            print >>sys.stderr, ('\nstates.RSTState.newsubsection: back from '
                                 'subsection (mylevel=%s, new level=%s)'
                                 % (mylevel,
                                    memo.sectionlevel))
            print >>sys.stderr, ('                       sm.abslineoffset=%s'
                                 % sm.abslineoffset())
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
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
        #print >>sys.stderr, ('paragraph: data=%r, textnodes=%r, warnings=%r'
        #                         % (data, textnodes, warnings))
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
    #print >>sys.stderr, '`RSTState.inline.patterns.uri.pattern`=\n%r' % inline.patterns.uri.pattern
    #print >>sys.stderr, 'RSTState.inline.patterns.uri.pattern=\n%s' % inline.patterns.uri.pattern

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
        sw = self.statemachine.memo.errorist.system_warning(
              1, 'Inline %s start-string without end-string '
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
            #print >>sys.stderr, 'interpreted_or_phrase_link: role=%r, position=%r' % (role, position)
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
                    sw = self.statemachine.memo.errorist.system_warning(
                          1, 'Mismatch: inline interpreted text start-string '
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
        sw = self.statemachine.memo.errorist.system_warning(
              1, 'Inline interpreted text or phrase link start-string '
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
                sw = self.statemachine.memo.errorist.system_warning(
                      1, 'Multiple roles in interpreted text at line %s.'
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
            #self.statemachine.memo.document.addautofootnoteref(refname,
            #                                                   fnrefnode)
            fnrefnode['auto'] = 1
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
            #print >>sys.stderr, 'RSTState.standalone_uri: remainder=%r' % remainder
            match = pattern.search(remainder)
            if match:
                #print >>sys.stderr, 'RSTState.standalone_uri: match.groups=%r, match.span(1)=%r' % (match.groups(), match.span(1))
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
        return self.statemachine.memo.errorist.system_warning(
              1, ('Unindent without blank line at line %s.'
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

    enum.sequenceREs = {}
    for sequence in enum.sequences:
        enum.sequenceREs[sequence] = re.compile(enum.sequencepats[sequence]
                                                + '$')

    tbl = Stuff()
    """Table parsing information."""

    tbl.pats = {'tableside': re.compile('[+|].+[+|]$'),
                'tabletop': re.compile(r'\+-[-+]+-\+ *$')}

    pats = {}
    """Fragments of patterns used by transitions."""

    pats['nonAlphaNum7Bit'] = '[!-/:-@[-`{-~]'
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
                'tabletop': tbl.pats['tabletop'],
                'explicit_markup': r'\.\.( +|$)',
                'overline': r'(%(nonAlphaNum7Bit)s)\1\1\1+ *$' % pats,
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
        if self.debug:
            print >>sys.stderr, ('\nstates.Body.indent (block_quote): '
                                 'indented=%r' % indented)
        bq = self.block_quote(indented, lineoffset)
        self.statemachine.node += bq
        if not blankfinish:
            self.statemachine.node += self.unindentwarning()
        return context, nextstate, []

    def block_quote(self, indented, lineoffset):
        bq = nodes.block_quote()
        sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
        sm.run(indented, inputoffset=lineoffset,
               memo=self.statemachine.memo, node=bq, matchtitles=0)
        sm.unlink()
        return bq

    def bullet(self, match, context, nextstate):
        """Bullet list item."""
        l = nodes.bullet_list()
        self.statemachine.node += l
        l['bullet'] = match.string[0]
        i, blankfinish = self.list_item(match.end())
        l += i
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'BulletList'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.states['BulletList'].blankfinish = blankfinish
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=l, matchtitles=0)
        if not sm.states['BulletList'].blankfinish:
            self.statemachine.node += self.unindentwarning()
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
        return [], nextstate, []

    def list_item(self, indent):
        indented, lineoffset, blankfinish = \
              self.statemachine.getknownindented(indent)
        if self.debug:
            print >>sys.stderr, ('\nstates.Body.list_item: blankfinish=%r'
                                 % blankfinish)
            print >>sys.stderr, ('\nstates.Body.list_item: indented=%r'
                                 % indented)
        i = nodes.list_item('\n'.join(indented))
        if indented:
            sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
            sm.run(indented, inputoffset=lineoffset,
                   memo=self.statemachine.memo, node=i, matchtitles=0)
            sm.unlink()
        return i, blankfinish

    def enumerator(self, match, context, nextstate):
        """Enumerated List Item"""
        format, sequence, text, ordinal = self.parseenumerator(match)
        #print >>sys.stderr, 'Body.enumerated: format=%r, sequence=%r, text=%r, ordinal=%r' % (format, sequence, text, ordinal)
        if ordinal is None:
            sw = self.statemachine.memo.errorist.system_warning(
                  2, ('Enumerated list start value invalid at line %s: '
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
            sw = self.statemachine.memo.errorist.system_warning(
                  0, ('Enumerated list start value not ordinal-1 at line %s: '
                      '%r (ordinal %s)' % (self.statemachine.abslineno(),
                                           text, ordinal)))
            self.statemachine.node += sw
        l = nodes.enumerated_list()
        self.statemachine.node += l
        l['enumtype'] = sequence
        l['start'] = text
        l['prefix'] = self.enum.formatinfo[format].prefix
        l['suffix'] = self.enum.formatinfo[format].suffix
        i, blankfinish = self.list_item(match.end())
        l += i
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'EnumeratedList'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.states['EnumeratedList'].blankfinish = blankfinish
        sm.states['EnumeratedList'].lastordinal = ordinal
        sm.states['EnumeratedList'].format = format
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=l, matchtitles=0)
        if not sm.states['EnumeratedList'].blankfinish:
            self.statemachine.node += self.unindentwarning()
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
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
                if self.enum.sequenceREs[expectedsequence].match(text):
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
                if self.enum.sequenceREs[sequence].match(text):
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
        l = nodes.field_list()
        self.statemachine.node += l
        f, blankfinish = self.field(match)
        l += f
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'FieldList'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.states['FieldList'].blankfinish = blankfinish
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=l, matchtitles=0)
        if not sm.states['FieldList'].blankfinish:
            self.statemachine.node += self.unindentwarning()
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
        return [], nextstate, []

    def field(self, match):
        name, args = self.parsefieldmarker(match)
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        if self.debug:
            print >>sys.stderr, ('\nstates.Body.field_list_item: indented=%r'
                                 % indented)
        f = nodes.field()
        f += nodes.field_name(name, name)
        for arg in args:
            f += nodes.field_argument(arg, arg)
        b = nodes.field_body('\n'.join(indented))
        f += b
        if indented:
            sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
            sm.run(indented, inputoffset=lineoffset,
                   memo=self.statemachine.memo, node=b, matchtitles=0)
            sm.unlink()
        return f, blankfinish

    def parsefieldmarker(self, match):
        """Extract & return name & argument list from a field marker match."""
        field = match.string[1:]        # strip off leading ':'
        field = field[:field.find(':')] # strip off trailing ':' etc.
        tokens = field.split()
        return tokens[0], tokens[1:]    # first == name, others == args

    def optionmarker(self, match, context, nextstate):
        """Option list item."""
        l = nodes.option_list()
        self.statemachine.node += l
        try:
            i, blankfinish = self.option_list_item(match)
        except MarkupError, detail:     # shouldn't happen; won't match pattern
            sw = self.statemachine.memo.errorist.system_warning(
                  2, ('Invalid option list marker at line %s: %s'
                      % (self.statemachine.abslineno(), detail)))
            self.statemachine.node += sw
            indented, indent, lineoffset, blankfinish = \
                  self.statemachine.getfirstknownindented(match.end())
            bq = self.block_quote(indented, lineoffset)
            self.statemachine.node += bq
            if not blankfinish:
                self.statemachine.node += self.unindentwarning()
            return [], nextstate, []
        l += i
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'OptionList'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.states['OptionList'].blankfinish = blankfinish
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=l, matchtitles=0)
        if not sm.states['OptionList'].blankfinish:
            self.statemachine.node += self.unindentwarning()
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
        return [], nextstate, []

    def option_list_item(self, match):
        options = self.parseoptionmarker(match)
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getfirstknownindented(match.end())
        if self.debug:
            print >>sys.stderr, ('\nstates.Body.option_list_item: indented=%r'
                                 % indented)
        i = nodes.option_list_item('', *options)
        d = nodes.description('\n'.join(indented))
        i += d
        if indented:
            sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
            sm.run(indented, inputoffset=lineoffset,
                   memo=self.statemachine.memo, node=d, matchtitles=0)
            sm.unlink()
        return i, blankfinish

    def parseoptionmarker(self, match):
        """
        Return a list of `node.option` objects from an option marker match.

        :Exception: `MarkupError` for invalid option markers.
        """
        optlist = []
        options = match.group().rstrip().split(', ')
        for optionstring in options:
            o = nodes.option(optionstring)
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
                    o += nodes.long_option(tokens[0], tokens[0])
                elif tokens[0][:1] == '-':
                    o += nodes.short_option(tokens[0], tokens[0])
                elif tokens[0][:1] == '/':
                    o += nodes.vms_option(tokens[0], tokens[0])
                if len(tokens) > 1:
                    o += nodes.option_argument(tokens[1], tokens[1])
                optlist.append(o)
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
            sw = self.statemachine.memo.errorist.system_warning(
                  1, 'Blank line required after table at line %s.'
                  % (self.statemachine.abslineno() + 1))
            self.statemachine.node += sw
        return [], nextstate, []

    def table(self):
        """Temporarily parse a table as a literal_block."""
        block, warnings, blankfinish = self.isolatetable()
        if block:
            data = '\n'.join(block)
            t = nodes.literal_block(data, data)
            nodelist = [t] + warnings
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
            warnings.append(self.statemachine.memo.errorist.system_warning(
                  2, 'Unexpected indentation at line %s.' % lineno))
            blankfinish = 0
        width = len(block[0].strip())
        for i in range(len(block)):
            block[i] = block[i].strip()
            if block[i][0] not in '+|': # check left edge
                blankfinish = 0
                self.statemachine.previousline(len(block) - i)
                del block[i:]
                break
        if not self.tbl.pats['tabletop'].match(block[-1]): # find bottom
            blankfinish = 0
            # from second-last to third line of table:
            for i in range(len(block) - 2, 1, -1):
                if self.tbl.pats['tabletop'].match(block[i]):
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

    def malformedtable(self, block):
        data = '\n'.join(block)
        nodelist = [
              self.statemachine.memo.errorist.system_warning(
              2, 'Malformed table at line %s; formatting as a literal '
              'block.' % (self.statemachine.abslineno() - len(block) + 1)),
              nodes.literal_block(data, data)]
        return nodelist

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
        f = nodes.footnote('\n'.join(indented))
        if name[0] == '#':
            name = name[1:]
            #self.statemachine.memo.document.addautofootnote(name, f)
        else:
            f += nodes.label('', label)
        if name:
            self.statemachine.memo.document.addimplicitlink(name, f)
        if indented:
            sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
            sm.run(indented, inputoffset=offset,
                   memo=self.statemachine.memo, node=f, matchtitles=0)
            sm.unlink()
        return [f], blankfinish

    def hyperlink_target(self, match,
                         pattern=explicit.patterns.target,
                         namegroup=explicit.groups.target.name):
        escaped = escape2null(match.string)
        targetmatch = pattern.match(escaped[match.end():])
        if not targetmatch:
            raise MarkupError('malformed hyperlink target at line %s.'
                              % self.statemachine.abslineno())
        name = normname(unescape(targetmatch.group(namegroup)))
        block = self.statemachine.gettextblock()
        reference = unescape(targetmatch.string[targetmatch.end():], 1).strip()
        blankfinish = 1
        for i in range(1,len(block)):
            if block[i][:1] != ' ':
                blankfinish = 0
                self.statemachine.previousline(len(block) - i)
                del block[i:]
                break
            reference += block[i].strip()
        blocktext = '\n'.join(block)
        if reference.find(' ') != -1:
            t = self.statemachine.memo.errorist.system_warning(
                  1, 'Hyperlink target at line %s contains whitespace. '
                  'Perhaps a footnote was intended?'
                  % (self.statemachine.abslineno() - len(block) + 1))
            t += nodes.literal_block(blocktext, blocktext)
        else:
            t = nodes.target(blocktext, reference)
            if reference:
                self.statemachine.memo.document.addindirectlink(
                      name, reference, t, self.statemachine.node)
            else:
                self.statemachine.memo.document.addexplicitlink(
                      name, t, self.statemachine.node)
        return [t], blankfinish

    def directive(self, match):
        # XXX need to actually *do* something with the directive
        type = match.group(1).lower()
        atts = {'type': type}
        data = match.string[match.end():].strip()
        if data:
            atts['data'] = data
        try:
            self.statemachine.nextline()
            indented, indent, offset, blankfinish = \
                  self.statemachine.getindented()
            text = '\n'.join(indented)
        except IndexError:
            text = ''
            blankfinish = 1
        children = []
        if text:
            children.append(nodes.literal_block(text, text))
        return [nodes.directive(text, *children, **atts)], blankfinish

    def comment(self, match):
        if not match.string[match.end():].strip(): # text on first line?
            try:                        # no
                if self.statemachine.nextline().strip(): # text on next line?
                    self.statemachine.previousline() # yes; it's not empty
                else:                   # yes; it's an empty comment
                    raise IndexError
            except IndexError:          # "A tiny but practical wart."
                return [nodes.comment()], 1
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
                      ([\w-]+)          # directive name
                      ::                # directive delimiter
                      (?:[ ]+|$)        # whitespace or end of line
                      """, re.VERBOSE))]

    def explicit_markup(self, match, context, nextstate):
        """Footnotes, hyperlink targets, directives, comments."""
        nodelist, blankfinish = self.explicit_construct(match)
        self.statemachine.node += nodelist
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'Explicit'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.states['Explicit'].blankfinish = blankfinish
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=self.statemachine.node,
               matchtitles=0)
        if not sm.states['Explicit'].blankfinish:
            self.statemachine.node += self.unindentwarning()
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
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
                          self.statemachine.memo.errorist.system_warning(
                          1, detail.__class__.__name__ + ': ' + str(detail)))
                    break
        nodelist, blankfinish = self.comment(match)
        return nodelist + errors, blankfinish

    def overline(self, match, context, nextstate):
        """Section title."""
        makesection = 1
        lineno = self.statemachine.abslineno()
        if not self.statemachine.matchtitles:
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Unexpected section title at line %s.' % lineno)
            self.statemachine.node += sw
            return [], nextstate, []
        title = underline = ''
        try:
            title = self.statemachine.nextline()
            underline = self.statemachine.nextline()
        except IndexError:
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Incomplete section title at line %s.' % lineno)
            self.statemachine.node += sw
            makesection = 0
        source = '%s\n%s\n%s' % (match.string, title, underline)
        overline = match.string.rstrip()
        underline = underline.rstrip()
        if not self.transitions['overline'][0].match(underline):
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Missing underline for overline at line %s.' % lineno)
            self.statemachine.node += sw
            makesection = 0
        elif overline != underline:
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Title overline & underline mismatch at ' 'line %s.'
                  % lineno)
            self.statemachine.node += sw
            makesection = 0
        title = title.rstrip()
        if len(title) > len(overline):
            self.statemachine.node += \
                  self.statemachine.memo.errorist.system_warning(
                  0, 'Title overline too short at line %s.'% lineno)
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
        i, blankfinish = self.list_item(match.end())
        self.statemachine.node += i
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
        i, blankfinish = self.list_item(match.end())
        self.statemachine.node += i
        self.blankfinish = blankfinish
        self.lastordinal = ordinal
        return [], 'EnumeratedList', []


class FieldList(SpecializedBody):

    """Second and subsequent field_list fields."""

    def fieldmarker(self, match, context, nextstate):
        """Field list field."""
        f, blankfinish = self.field(match)
        self.statemachine.node += f
        self.blankfinish = blankfinish
        return [], 'FieldList', []


class OptionList(SpecializedBody):

    """Second and subsequent option_list option_list_items."""

    def optionmarker(self, match, context, nextstate):
        """Option list item."""
        try:
            i, blankfinish = self.option_list_item(match)
        except MarkupError, detail:
            self.invalid_input()
        self.statemachine.node += i
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
        p, literalnext = self.paragraph(context,
                                        self.statemachine.abslineno() - 1)
        self.statemachine.node += p
        if literalnext:
            self.statemachine.node += self.literal_block()
        return [], 'Body', []

    def eof(self, context):
        if context:
            p, literalnext = self.paragraph(context,
                                            self.statemachine.abslineno() - 1)
            if self.debug:
                print >>sys.stderr, ('\nstates.Text.eof: context=%r, p=%r, '
                                     'node=%r' % (context, p,
                                                  self.statemachine.node))
            self.statemachine.node += p
            if literalnext:
                self.statemachine.node += self.literal_block()
        return []

    def indent(self, match, context, nextstate):
        """Definition list item."""
        l = nodes.definition_list()
        i, blankfinish = self.definition_list_item(context)
        l += i
        self.statemachine.node += l
        offset = self.statemachine.lineoffset + 1   # next line
        kwargs = self.indentSMkwargs.copy()
        kwargs['initialstate'] = 'DefinitionList'
        sm = self.indentSM(debug=self.debug, **kwargs)
        sm.states['Definition'].blankfinish = blankfinish
        sm.run(self.statemachine.inputlines[offset:],
               inputoffset=self.statemachine.abslineoffset() + 1,
               memo=self.statemachine.memo, node=l, matchtitles=0)
        if not sm.states['Definition'].blankfinish:
            self.statemachine.node += self.unindentwarning()
        sm.unlink()
        try:
            self.statemachine.gotoline(sm.abslineoffset())
        except IndexError:
            pass
        return [], 'Body', []

    def underline(self, match, context, nextstate):
        """Section title."""
        lineno = self.statemachine.abslineno()
        if not self.statemachine.matchtitles:
            sw = self.statemachine.memo.errorist.system_warning(
                  3, 'Unexpected section title at line %s.' % lineno)
            self.statemachine.node += sw
            return [], nextstate, []
        title = context[0].rstrip()
        underline = match.string.rstrip()
        source = title + '\n' + underline
        if self.debug:
            print >>sys.stderr, ('\nstates.Text.underline: context=%r, '
                                 'match.string=%r, title=%r, titlestyles=%r'
                                 % (context, match.string, title,
                                    self.statemachine.memo.titlestyles))
        if len(title) > len(underline):
            self.statemachine.node += \
                  self.statemachine.memo.errorist.system_warning(
                  0, 'Title underline too short at line %s.' % lineno)
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
            sw = self.statemachine.memo.errorist.system_warning(
                  2, 'Unexpected indentation at line %s.' % lineno)
        lines = context + block
        if self.debug:
            print >>sys.stderr, 'states.Text.text: lines=%r' % lines
        p, literalnext = self.paragraph(lines, startline)
        if self.debug:
            print >>sys.stderr, 'states.Text.text: p=%r' % p
        self.statemachine.node += p
        self.statemachine.node += sw
        if literalnext:
            try:
                line = self.statemachine.nextline()
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
            nodelist.append(self.statemachine.memo.errorist.system_warning(
                  1, 'Literal block expected at line %s; none found.'
                  % self.statemachine.abslineno()))
        return nodelist

    def definition_list_item(self, termline):
        indented, indent, lineoffset, blankfinish = \
              self.statemachine.getindented()
        if self.debug:
            print >>sys.stderr, ('\nstates.Text.indent (definition): indented=%r'
                                 % indented)
        i = nodes.definition_list_item('\n'.join(termline + indented))
        t, warnings = self.term(termline, self.statemachine.abslineno() - 1)
        i += t
        d = nodes.definition('', *warnings)
        if termline[0][-2:] == '::':
            d += self.statemachine.memo.errorist.system_warning(
                  0, 'Blank line missing before literal block? '
                  'Interpreted as a definition list item. '
                  'At line %s.' % (lineoffset + 1))
        sm = self.indentSM(debug=self.debug, **self.indentSMkwargs)
        sm.run(indented, inputoffset=lineoffset,
               memo=self.statemachine.memo, node=d, matchtitles=0)
        sm.unlink()
        i += d
        return i, blankfinish

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
        i, blankfinish = self.definition_list_item(context)
        self.statemachine.node += i
        self.blankfinish = blankfinish
        return [], 'DefinitionList', []


stateclasses = [Body, BulletList, DefinitionList, EnumeratedList, FieldList,
                OptionList, RFC822List, Explicit, Text, Definition]
"""Standard set of State classes used to start `RSTStateMachine`."""


class TableParser:

    headBodySeparatorPat = re.compile(r'\+=[=+]+=\+$')

    def init(self, block):
        self.block = block[:]           # make a copy; it may be modified
        self.bottom = len(block) - 1
        self.right = len(block[0]) - 1
        self.headbodysep = None
        self.done = [-1] * len(block[0])
        self.cells = []
        self.rowseps = {0: [0]}
        self.colseps = {0: [0]}

    def parse(self, block):
        self.init(block)
        self.findheadbodysep()
        self.parsegrid()

    def findheadbodysep(self):
        for i in range(len(self.block)):
            line = self.block[i]
            if self.headBodySeparatorPat.match(line):
                if self.headbodysep:
                    raise MarkupError, ('Multiple head/body row separators '
                          'in table (at line offset %s and %s); only one '
                          'allowed.' % (self.headbodysep, i))
                else:
                    self.headbodysep = i
                    self.block[i] = line.replace('=', '-')

    def parsegrid(self):
        corners = [(0, 0)]
        while corners:
            top, left = corners.pop(0)
            if top == self.bottom or left == self.right \
                  or top <= self.done[left]:
                continue
            result = self.scancell(top, left)
            if not result:
                continue
            bottom, right, rowseps, colseps = result
            updateDictOfLists(self.rowseps, rowseps)
            updateDictOfLists(self.colseps, colseps)
            self.markdone(top, left, bottom, right)
            cellblock = self.getcellblock(top, left, bottom, right)
            self.cells.append((top, left, bottom, right, cellblock))
            corners.extend([(top, right), (bottom, left)])
            corners.sort()
        if not self.checkparsecomplete():
            raise MarkupError, 'Malformed table; parse incomplete.'

    def markdone(self, top, left, bottom, right):
        before = top - 1
        after = bottom - 1
        for col in range(left, right):
            assert self.done[col] == before
            self.done[col] = after

    def checkparsecomplete(self):
        last = self.bottom - 1
        for col in range(self.right):
            if self.done[col] != last:
                return None
        return 1

    def getcellblock(self, top, left, bottom, right):
        cellblock = []
        margin = right
        for lineno in range(top + 1, bottom):
            line = self.block[lineno][left + 1 : right].rstrip()
            cellblock.append(line)
            if line:
                margin = margin and min(margin, len(line) - len(line.lstrip()))
        if 0 < margin < right:
            cellblock = [line[margin:] for line in cellblock]
        return cellblock

    def scancell(self, top, left):
        assert self.block[top][left] == '+'
        result = self.scanright(top, left)
        return result

    def scanright(self, top, left):
        colseps = {}
        line = self.block[top]
        for i in range(left + 1, self.right + 1):
            if line[i] == '+':
                colseps[i] = [top]
                result = self.scandown(top, left, i)
                if result:
                    bottom, rowseps, newcolseps = result
                    updateDictOfLists(colseps, newcolseps)
                    return bottom, i, rowseps, colseps
            elif line[i] != '-':
                return None
        return None

    def scandown(self, top, left, right):
        rowseps = {}
        for i in range(top + 1, self.bottom + 1):
            if self.block[i][right] == '+':
                rowseps[i] = [right]
                result = self.scanleft(top, left, i, right)
                if result:
                    newrowseps, colseps = result
                    updateDictOfLists(rowseps, newrowseps)
                    return i, rowseps, colseps
            elif self.block[i][right] != '|':
                return None
        return None

    def scanleft(self, top, left, bottom, right):
        colseps = {}
        line = self.block[bottom]
        for i in range(right - 1, left, -1):
            if line[i] == '+':
                colseps[i] = [bottom]
            elif line[i] != '-':
                return None
        if line[left] != '+':
            return None
        result = self.scanup(top, left, bottom, right)
        if result is not None:
            rowseps = result
            return rowseps, colseps
        return None

    def scanup(self, top, left, bottom, right):
        rowseps = {}
        for i in range(bottom - 1, top, -1):
            if self.block[i][left] == '+':
                rowseps[i] = [left]
            elif self.block[i][left] != '|':
                return None
        return rowseps


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

def updateDictOfLists(master, newdata):
    for key, values in newdata.items():
        master.setdefault(key, []).extend(values)
