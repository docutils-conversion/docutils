#! /usr/bin/env python
# $Id: model.py,v 1.2 2001/08/01 02:56:35 goodger Exp $
# by David Goodger (dgoodger@bigfoot.com)


class Parser:

    def __init__(self, warninglevel=1, errorlevel=3, language='en'):
        """Initialize the Parser instance."""
        self.warninglevel = warninglevel
        self.errorlevel = errorlevel
        self.language = language

    def parse(self, inputstring):
        """Override to parse `inputstring` and return a document tree."""
        raise NotImplementedError('subclass must override this method')

    def setup_parse(self, inputstring):
        """Initial setup, used by `parse()`."""
        self.inputstring = inputstring
