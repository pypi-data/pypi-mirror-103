|PyPI version| |numpy-fracadf| |Total alerts| |Language grade: Python|
|deepcode|

numpy-fracadf
=============

Determine fractal order by the ADF test

Installation
------------

The ``numpy-fracadf`` `git
repo <http://github.com/ulf1/numpy-fracadf>`__ is available as `PyPi
package <https://pypi.org/project/numpy-fracadf>`__

::

   pip install numpy-fracadf
   pip install git+ssh://git@github.com/ulf1/numpy-fracadf.git

Usage
-----

.. code:: py

   from numpy_fracadf import fracadf2
   d = fracadf2(X, tau=1e-4, mmax=527)

Check the `examples <http://github.com/ulf1/numpy-fracadf/examples>`__
folder for notebooks.

Appendix
--------

Install a virtual env
~~~~~~~~~~~~~~~~~~~~~

.. code:: sh

   python3.6 -m venv .venv
   source .venv/bin/activate
   pip3 install --upgrade pip
   pip3 install -r requirements.txt
   pip3 install -r requirements-dev.txt
   pip3 install -r requirements-demo.txt

Python commands
~~~~~~~~~~~~~~~

-  Jupyter for the examples: ``jupyter lab``
-  Check syntax:
   ``flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')``

Publish

.. code:: sh

   pandoc README.md --from markdown --to rst -s -o README.rst
   python setup.py sdist 
   twine upload -r pypi dist/*

Clean up
~~~~~~~~

.. code:: sh

   find . -type f -name "*.pyc" | xargs rm
   find . -type d -name "__pycache__" | xargs rm -r
   rm -r .pytest_cache
   rm -r .venv

.. |PyPI version| image:: https://badge.fury.io/py/numpy-fracadf.svg
   :target: https://badge.fury.io/py/numpy-fracadf
.. |numpy-fracadf| image:: https://snyk.io/advisor/python/numpy-fracadf/badge.svg
   :target: https://snyk.io/advisor/python/numpy-fracadf
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/ulf1/numpy-fracadf.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/numpy-fracadf/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/ulf1/numpy-fracadf.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/numpy-fracadf/context:python
.. |deepcode| image:: https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6InVsZjEiLCJyZXBvMSI6Im51bXB5LWZyYWNhZGYiLCJpbmNsdWRlTGludCI6ZmFsc2UsImF1dGhvcklkIjoyOTQ1MiwiaWF0IjoxNjE5NTM4OTQ2fQ.wP1E2eQ0qLTS97oCc6KIqkOL-DR6eMnM4JG6fHhUHxk
   :target: https://www.deepcode.ai/app/gh/ulf1/numpy-fracadf/_/dashboard?utm_content=gh%2Fulf1%2Fnumpy-fracadf
