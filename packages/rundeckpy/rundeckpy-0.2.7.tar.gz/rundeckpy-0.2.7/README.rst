=========
rundeckpy
=========
Python based Rundeck plugins.

The package contains:

* a command line tool
* a series of helper functions
* a series of plugins
* squeleton for new plugins

command line tool
#################


plugins
#######


squeleton
#########


base class
##########


Development
###########

Install
*******
Clone
=====
Create venv 
===========
Activate
========
Install poetry 
==============
Install package
===============
.. code-block:: bash

    poetry install

Tests
*****

Code Quality
============

.. code-block:: bash

    black src/rundeckpy  
    poetry run pylint src/rundeckpy/  

Tests and coverage
==================

.. code-block:: bash

    poetry run pytest tests 
    poetry run coverage run -m pytest -v && poetry run coverage report -m  
    poetry run pytest --cov=src/rundeckpy/ tests  
  
poetry build

poetry publish

poetry publish -r gitlab