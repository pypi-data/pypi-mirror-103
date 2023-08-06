hydroMT-wflow: wflow plugin for hydroMT
#######################################

.. image:: https://codecov.io/gh/Deltares/hydromt_wflow/branch/main/graph/badge.svg?token=ss3EgmwHhH
    :target: https://codecov.io/gh/Deltares/hydromt_wflow

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
    :target: http://deltares.github.io/hydromt_wflow/latest/?badge=latest

.. image:: https://mybinder.org/badge_logo.svg
    :target: https://mybinder.org/v2/gh/Deltares/hydromt_wflow/main?urlpath=lab/tree/examples

hydroMT_ is a python package, developed by Deltares, to build and analysis hydro models.
It provides a generic model api with attributes to access the model schematization,
(dynamic) forcing data, results and states. This plugin provides an implementation 
for the wflow_ model.


.. _hydromt: https://deltares.github.io/hydromt

.. _wflow: https://github.com/Deltares/Wflow.jl


Installation
------------

hydroMT is availble from pypi and conda-forge. We recommend installing a stable version with conda:

To install hydromt using conda do:

.. code-block:: console

  conda install hydromt_wflow -c conda-forge

To install the latest hydromt with some additional packages to run the examples, 
we recommend install a hydromt-wflow environment based on the environment.yml file.

.. code-block:: console

  conda env create -f environment.yml

Documentation
-------------

Learn more about hydroMT in its `online documentation <http://deltares.github.io/hydromt_wflow/latest/>`_

Contributing
------------

You can find information about contributing to hydroMT at our `Contributing page <http://deltares.github.io/hydromt_wflow/latest/contributing.html>`_.

License
-------

Copyright (c) 2021, Deltares

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
