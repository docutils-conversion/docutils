#!/usr/bin/env python
# $Id: quicktest.py,v 1.1 2001/07/27 02:11:50 gtk Exp $
# 
# I used to have a much prettier version of this script, but inadvertently 
# deleted it. Oops. Here's a quick, ugly, grotty hack as a temporary 
# replacement. --gtk

"""\
quicktest.py: quickly test the restructuredtext parser. 

No command line arguments are supported in this version. 

Proposed usage::

  quicktest.py [-x|-p|-t] [filename] 

    filename     : filename to use as input (default is stdin)
    -x --xml     : output raw xml
    -p --pretty  : output pretty print (default)
    -t --test    : output in test format as per test_states.py
"""

"""
Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Revision: $Revision: 1.1 $
Date: $Date: 2001/07/27 02:11:50 $
Copyright: This module has been placed in the public domain.

"""

import dps.parsers.restructuredtext

# create a parser
p = dps.parsers.restructuredtext.Parser()

# gather input
input = []
try: 
  while 1:
    input.append(raw_input())
except EOFError:
  pass

# generate parsed output
o = p.parse('\n'.join(input))

# print a delimiter
print '=>'

# print the parser output
print o.pprint()
