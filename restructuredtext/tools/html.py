#!/usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/02/20 04:28:17 $
:Copyright: This module has been placed in the public domain.

A minimal front-end to the Docutils Publisher.

This module takes advantage of the default values defined in `publish()`.
"""

import sys
from dps.core import publish


if len(sys.argv) == 2:
    publish(writername='html', source=sys.argv[1])
elif len(sys.argv) == 3:
    publish(writername='html', source=sys.argv[1], destination=sys.argv[2])
elif len(sys.argv) > 3:
    print >>sys.stderr, 'Maximum 2 arguments allowed.'
    sys.exit(1)
else:
    publish()
