#! /usr/bin/env python
# $Id: model.py,v 1.3 2001/09/07 02:10:30 goodger Exp $
# by David Goodger (dgoodger@bigfoot.com)


from dps import utils


class Parser:

    def __init__(self, warninglevel=1, errorlevel=3, languagecode='en',
                 debug=0):
        """Initialize the Parser instance."""
        self.warninglevel = warninglevel
        self.errorlevel = errorlevel
        self.languagecode = languagecode
        self.language = utils.language(languagecode)
        self.debug = debug

    def parse(self, inputstring):
        """Override to parse `inputstring` and return a document tree."""
        raise NotImplementedError('subclass must override this method')

    def setup_parse(self, inputstring):
        """Initial setup, used by `parse()`."""
        self.inputstring = inputstring
