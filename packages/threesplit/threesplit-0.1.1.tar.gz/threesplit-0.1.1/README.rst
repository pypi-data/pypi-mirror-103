|PyPI version| |threesplit| |Total alerts| |Language grade: Python|
|deepcode|

threesplit
==========

Three-way data split into training set, validation set, and test set.

Installation
------------

The ``threesplit`` `git repo <http://github.com/kmedian/threesplit>`__
is available as `PyPi package <https://pypi.org/project/threesplit>`__

::

   pip install threesplit

Usage
-----

Check the `examples <examples>`__ folder for notebooks.

Commands
--------

-  Check syntax: ``flake8 --ignore=F401``
-  Remove ``.pyc`` files: ``find . -type f -name "*.pyc" | xargs rm``
-  Remove ``__pycache__`` folders:
   ``find . -type d -name "__pycache__" | xargs rm -rf``

Publish

.. code:: sh

   pandoc README.md --from markdown --to rst -s -o README.rst
   python setup.py sdist 
   twine upload -r pypi dist/*

Support
-------

Please `open an
issue <https://github.com/kmedian/threesplit/issues/new>`__ for support.

Contributing
------------

Please contribute using `Github
Flow <https://guides.github.com/introduction/flow/>`__. Create a branch,
add commits, and `open a pull
request <https://github.com/kmedian/threesplit/compare/>`__.

.. |PyPI version| image:: https://badge.fury.io/py/threesplit.svg
   :target: https://badge.fury.io/py/threesplit
.. |threesplit| image:: https://snyk.io/advisor/python/threesplit/badge.svg
   :target: https://snyk.io/advisor/python/threesplit
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/kmedian/threesplit.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/kmedian/threesplit/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/kmedian/threesplit.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/kmedian/threesplit/context:python
.. |deepcode| image:: https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6ImttZWRpYW4iLCJyZXBvMSI6InRocmVlc3BsaXQiLCJpbmNsdWRlTGludCI6ZmFsc2UsImF1dGhvcklkIjoyOTQ1MiwiaWF0IjoxNjE5NTQwNjI4fQ.YC9h-9S3cQqgPOlYq3WYA8SegkLEL4sFHN-DQAVQBY0
   :target: https://www.deepcode.ai/app/gh/kmedian/threesplit/_/dashboard?utm_content=gh%2Fkmedian%2Fthreesplit
