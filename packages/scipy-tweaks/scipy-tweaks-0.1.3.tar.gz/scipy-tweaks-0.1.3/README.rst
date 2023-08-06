|PyPI version| |scipy-tweaks| |Total alerts| |Language grade: Python|
|deepcode|

scipy-tweaks
============

Utility functions for scipy.

Usage
-----

Check the `examples <http://github.com/ulf1/scipy-tweaks/examples>`__
folder for notebooks.

Appendix
--------

Installation
~~~~~~~~~~~~

The ``scipy-tweaks`` `git repo <http://github.com/ulf1/scipy-tweaks>`__
is available as `PyPi package <https://pypi.org/project/scipy-tweaks>`__

::

   pip install scipy-tweaks
   pip install git+ssh://git@github.com/ulf1/scipy-tweaks.git

Install a virtual environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   python3.6 -m venv .venv
   source .venv/bin/activate
   pip3 install --upgrade pip
   pip3 install -r requirements.txt
   pip3 install -r requirements-dev.txt
   pip3 install -r requirements-demo.txt

(If your git repo is stored in a folder with whitespaces, then don’t use
the subfolder ``.venv``. Use an absolute path without whitespaces.)

Python commands
~~~~~~~~~~~~~~~

-  Jupyter for the examples: ``jupyter lab``
-  Check syntax:
   ``flake8 --ignore=F401 --exclude=$(grep -v '^#' .gitignore | xargs | sed -e 's/ /,/g')``
-  Run Unit Tests: ``pytest``

Publish

.. code:: sh

   pandoc README.md --from markdown --to rst -s -o README.rst
   python setup.py sdist 
   twine upload -r pypi dist/*

Clean up
~~~~~~~~

::

   find . -type f -name "*.pyc" | xargs rm
   find . -type d -name "__pycache__" | xargs rm -r
   rm -r .pytest_cache
   rm -r .venv

Support
~~~~~~~

Please `open an
issue <https://github.com/ulf1/scipy-tweaks/issues/new>`__ for support.

Contributing
~~~~~~~~~~~~

Please contribute using `Github
Flow <https://guides.github.com/introduction/flow/>`__. Create a branch,
add commits, and `open a pull
request <https://github.com/ulf1/scipy-tweaks/compare/>`__.

.. |PyPI version| image:: https://badge.fury.io/py/scipy-tweaks.svg
   :target: https://badge.fury.io/py/scipy-tweaks
.. |scipy-tweaks| image:: https://snyk.io/advisor/python/scipy-tweaks/badge.svg
   :target: https://snyk.io/advisor/python/scipy-tweaks
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/ulf1/scipy-tweaks.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/scipy-tweaks/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/ulf1/scipy-tweaks.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/scipy-tweaks/context:python
.. |deepcode| image:: https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6InVsZjEiLCJyZXBvMSI6InNjaXB5LXR3ZWFrcyIsImluY2x1ZGVMaW50IjpmYWxzZSwiYXV0aG9ySWQiOjI5NDUyLCJpYXQiOjE2MTk1NDA0MDR9.CRitUw9wkJfdXyNbjeOlHjm3IY3-QHUhpxnn1BRqskk
   :target: https://www.deepcode.ai/app/gh/ulf1/scipy-tweaks/_/dashboard?utm_content=gh%2Fulf1%2Fscipy-tweaks
