==============
 README: test
==============

Author: Garth Kidd
Contact: garth@deadlybloodyserious.com
Version: Rrefactor-test (EXPERIMENTAL)
Date: $Date: 2001/07/29 09:05:39 $
Web-site: http://structuredtext.sf.net/

**THIS IS AN EXPERIMENTAL VERSION**

**IF YOU WANT THE OFFICIAL VERSION, CHECK OUT ``RELEASE``**

Files
-----

``README.txt``: 
    You're reading it. 

``TestFramework.py``: 
    Provides some handy classes, command line parsing, a ``main()`` method 
    for other tests to use, and some shared state. 

``test_all.py``: 
    Finds all test_* apart from itself, builds a TestSuite, and runs it. 

    **DISCLAIMER:** Currently doesn't do any of the searching. Oops. 

``test_*.py``: individual tests. 

Notes
-----

Notes on my restructuring of the test framework: 

* This experiment is a direct result of tracker item `443275`_, 
  "refactor tests". I raised that item, so no surprises there. 

  .. http://sf.net/tracker/?func=detail&aid=443275&group_id=7050&atid=107050

* I'm also addressing tracker item `443273`_, "need new test types."

  .. http://sf.net/tracker/?func=detail&aid=443273&group_id=7050&atid=107050

* I'm removing restructuredtext/test_states.py and replacing it with 
  test/*. The specific reason for moving it is that I can't see a 
  need for the test suite to be installed into someone's Python 
  distribution. If there turns out to be a good reason for moving 
  test/* to restructuredtext/test/*, let me know. 

 
