#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/02/06 03:02:51 $
:Copyright: This module has been placed in the public domain.


"""

__docformat = 'reStructuredText'

__all__ = ['Publisher', 'setup']


from dps import readers, parsers, writers


class Publisher:

    def __init__(self, reader=None, parser=None, writer=None):
        self.reader = reader
        self.parser = parser
        self.writer = writer

    def setreader(self, readername, languagecode='en', warninglevel=2,
                  errorlevel=4, warningstream=None, debug=0):
        """Set `self.reader` by name."""
        readerclass = readers.get_reader_class(readername)
        self.reader = readerclass(languagecode, warninglevel, errorlevel,
                                  warningstream, debug)

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


def convert(source=None, destination=None,
            reader=None, readername='standalone',
            parser=None, parsername='restructuredtext',
            writer=None, writername='pprint'):
    pub = Publisher(reader, parser, writer)
    if reader is None:
        pub.setreader(readername)
    if parser is None:
        pub.setparser(parsername)
    if writer is None:
        pub.setwriter(writername)
    pub.publish(source, destination)
