=======================
NLDI Elevation Services
=======================


.. image:: https://img.shields.io/pypi/v/nldi_el_serv.svg
        :target: https://pypi.python.org/pypi/nldi_el_serv

.. image:: https://travis-ci.com/ACWI-SSWD/nldi_el_serv.svg?branch=main
        :target: https://travis-ci.com/ACWI-SSWD/nldi_el_serv

.. image:: https://readthedocs.org/projects/nldi-el-serv/badge/?version=latest
        :target: https://nldi-el-serv.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status



NLDI Elevation Sevices

* Free software
* Documentation: https://nldi-el-serv.readthedocs.io.

Development
-----------
* conda env create -f .\requirements_dev.yml
* conda activate nldi_el_serv
* pip install -e .


Features
--------

* nldi_el_serv xsatpoint -f test1.json --lonlat -103.80119 40.2684  --width 1000 --numpoints 101
* nldi_el_serv xsatendpts -f test2.json -s -103.801134 40.267335 -e -103.800787 40.272798 -c epsg:4326 -n 101

Credits
-------

CLI developed from example: https://github.com/pallets/click/blob/master/examples/repo/repo.py

This package was created with Cookiecutter_ and the _Scientific-python-cookiecutter.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _Scientific_python_cookiecutter: https://github.com/NSLS-II/scientific-python-cookiecutter

Disclaimer
----------

This software is preliminary or provisional and is subject to revision. It is
being provided to meet the need for timely best science. The software has not
received final approval by the U.S. Geological Survey (USGS). No warranty,
expressed or implied, is made by the USGS or the U.S. Government as to the
functionality of the software and related material nor shall the fact of release
constitute any such warranty. The software is provided on the condition that
neither the USGS nor the U.S. Government shall be held liable for any damages
resulting from the authorized or unauthorized use of the software.

