#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/02/07 02:02:24 $
:Copyright: This module has been placed in the public domain.


"""

__docformat__ = 'reStructuredText'

__all__ = ['Publisher', 'publish']


import readers, parsers, writers, utils


class Publisher:

    reporter = None
    """A `utils.Reporter` instance used for all document processing."""

    def __init__(self, reader=None, parser=None, writer=None, reporter=None,
                 languagecode='en', warninglevel=2, errorlevel=4,
                 warningstream=None, debug=0):
        self.reader = reader
        self.parser = parser
        self.writer = writer
        if not reporter:
            reporter = utils.Reporter(warninglevel, errorlevel, warningstream,
                                      debug)
        self.reporter = reporter
        self.languagecode = languagecode

    def setreader(self, readername, languagecode=None):
        """Set `self.reader` by name."""
        readerclass = readers.get_reader_class(readername)
        self.reader = readerclass(self.reporter,
                                  languagecode or self.languagecode)

    def setparser(self, parsername):
        """Set `self.parser` by name."""
        parserclass = parsers.get_parser_class(parsername)
        self.parser = parserclass()

    def setwriter(self, writername):
        """Set `self.writer` by name."""
        writerclass = writers.get_writer_class(writername)
        self.writer = writerclass()

    def publish(self, source, destination):
        document = self.reader.read(source, self.parser)
        self.writer.write(document, destination)


def publish(source=None, destination=None,
            reader=None, readername='standalone',
            parser=None, parsername='restructuredtext',
            writer=None, writername='pprint',
            reporter=None, languagecode='en',
            warninglevel=2, errorlevel=4, warningstream=None, debug=0):
    pub = Publisher(reader, parser, writer, reporter, languagecode,
                    warninglevel, errorlevel, warningstream, debug)
    if reader is None:
        pub.setreader(readername)
    if parser is None:
        pub.setparser(parsername)
    if writer is None:
        pub.setwriter(writername)
    pub.publish(source, destination)
