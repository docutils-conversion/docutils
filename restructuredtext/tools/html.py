#!/usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/02/21 03:32:27 $
:Copyright: This module has been placed in the public domain.

A minimal front-end to the Docutils Publisher.

This module takes advantage of the default values defined in `publish()`.
"""

import sys
from dps.core import publish
from dps import utils

reporter = utils.Reporter(2, 4)
#reporter.setcategory('nodes.Node.walkabout', 2, 4, debug=1)

if len(sys.argv) == 2:
    publish(writername='html', source=sys.argv[1], reporter=reporter)
elif len(sys.argv) == 3:
    publish(writername='html', source=sys.argv[1], destination=sys.argv[2],
            reporter=reporter)
elif len(sys.argv) > 3:
    print >>sys.stderr, 'Maximum 2 arguments allowed.'
    sys.exit(1)
else:
    publish()
