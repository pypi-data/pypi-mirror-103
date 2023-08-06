|PyPI version| |numpy-linreg| |Total alerts| |Language grade: Python|
|deepcode|

numpy-linreg
============

Linear Regression with numpy only.

Installation
------------

The ``numpy-linreg`` `git repo <http://github.com/ulf1/numpy-linreg>`__
is available as `PyPi package <https://pypi.org/project/numpy-linreg>`__

.. code:: sh

   pip install numpy-linreg
   pip install git+ssh://git@github.com/ulf1/numpy-linreg.git

Usage
-----

Ridge Regression

.. code:: py

   import numpy_linreg.ridge as ridge
   import numpy_linreg.metrics as metrics
   beta = ridge.lu(y, X)
   rmse = metrics.rmse(y, X, beta)

OLS Regression

.. code:: py

   import numpy_linreg.ols as ols
   beta = ols.lu(y, X)
   beta = ols.pinv(y, X)
   beta = ols.qr(y, X)
   beta = ols.svd(y, X)

Check the
`examples <http://github.com/ulf1/numpy-linreg/tree/master/examples>`__
folder for notebooks.

Appendix
--------

Commands
~~~~~~~~

Install a virtual environment

.. code:: sh

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
issue <https://github.com/ulf1/numpy-linreg/issues/new>`__ for support.

Contributing
~~~~~~~~~~~~

Please contribute using `Github
Flow <https://guides.github.com/introduction/flow/>`__. Create a branch,
add commits, and `open a pull
request <https://github.com/ulf1/numpy-linreg/compare/>`__.

.. |PyPI version| image:: https://badge.fury.io/py/numpy-linreg.svg
   :target: https://badge.fury.io/py/numpy-linreg
.. |numpy-linreg| image:: https://snyk.io/advisor/python/numpy-linreg/badge.svg
   :target: https://snyk.io/advisor/python/numpy-linreg
.. |Total alerts| image:: https://img.shields.io/lgtm/alerts/g/ulf1/numpy-linreg.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/numpy-linreg/alerts/
.. |Language grade: Python| image:: https://img.shields.io/lgtm/grade/python/g/ulf1/numpy-linreg.svg?logo=lgtm&logoWidth=18
   :target: https://lgtm.com/projects/g/ulf1/numpy-linreg/context:python
.. |deepcode| image:: https://www.deepcode.ai/api/gh/badge?key=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybTEiOiJnaCIsIm93bmVyMSI6InVsZjEiLCJyZXBvMSI6Im51bXB5LWxpbnJlZyIsImluY2x1ZGVMaW50IjpmYWxzZSwiYXV0aG9ySWQiOjI5NDUyLCJpYXQiOjE2MTk1NDAzMDZ9.edO77WsHsnY9tPe9cajcO_xDc6JX9Nt9etM0GHshJbY
   :target: https://www.deepcode.ai/app/gh/ulf1/numpy-linreg/_/dashboard?utm_content=gh%2Fulf1%2Fnumpy-linreg
