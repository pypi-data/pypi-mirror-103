|PyPI version| |datefeatures| |Total alerts| |Language grade: Python|
|deepcode|

datefeatures
============

Table of Contents
-----------------

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Commands <#commands>`__
-  `Support <#support>`__
-  `Contributing <#contributing>`__

Installation
------------

The ``datefeatures`` `git
repo <http://github.com/kmedian/datefeatures>`__ is available as `PyPi
package <https://pypi.org/project/datefeatures>`__

::

   pip install datefeatures

Usage
-----

Check the `examples <examples>`__ folder for notebooks.

Commands
--------

Install a virtual environment

::

   python3 -m venv .venv  # see note below
   source .venv/bin/activate
   pip3 install --upgrade pip
   pip3 install -r requirements.txt
   pip3 install jupyterlab

(If your git repo is stored in a folder with whitespaces, then don’t use
the subfolder ``.venv``. Use an absolute path without whitespaces.)

Python commands

-  Jupyter for the examples: ``jupyter lab``
-  Check syntax:
   ``flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')``
-  Run Unit Tests: ``python -W ignore -m unittest discover``

Publish

.. code:: sh

   pandoc README.md --from markdown --to rst -s -o README.rst
   python setup.py sdist 
   twine upload -r pypi dist/*

Clean up

::

   find . -type f -name "*.pyc" | xargs rm
   find . -type d -name "__pycache__" | xargs rm -r
   rm -r .pytest_cache
   rm -r .venv

Support
-------

Please `open an
issue <https://github.com/kmedian/datefeatures/issues/new>`__ for
support.

Contributing
------------

Please contribute using `Github
Flow <https://guides.github.com/introduction/flow/>`__. Create a branch,
add commits, and `open a pull
request <https://github.com/kmedian/datefeatures/compare/>`__.

.. |PyPI version| image:: https://badge.fury.io/py/datefeatures.svg
   :target: https://badge.fury.io/py/datefeatures
.. |datefeatures| image:: https://snyk.io/advisor/python/datefeatures/badge.svg
   :target: https://snyk.io/advisor/python/datefeatures
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/kmedian/datefeatures.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/kmedian/datefeatures/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/kmedian/datefeatures.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/kmedian/datefeatures/context:python
.. |deepcode| image:: https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6ImttZWRpYW4iLCJyZXBvMSI6ImRhdGVmZWF0dXJlcyIsImluY2x1ZGVMaW50IjpmYWxzZSwiYXV0aG9ySWQiOjI5NDUyLCJpYXQiOjE2MTk1MzYxMzR9.N7NgWjiFb0RXjg2MK8jsmf_2KPL8cWtkUhz02uZ-k2w
   :target: https://www.deepcode.ai/app/gh/kmedian/datefeatures/_/dashboard?utm_content=gh%2Fkmedian%2Fdatefeatures
