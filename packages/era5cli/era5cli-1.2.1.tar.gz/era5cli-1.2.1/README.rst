era5cli
=======
.. image:: https://img.shields.io/badge/License-Apache%202.0-blue.svg
    :target: https://opensource.org/licenses/Apache-2.0
    :alt: License

.. image:: https://img.shields.io/badge/docs-latest-brightgreen.svg
   :target: http://era5cli.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

.. image:: https://github.com/eWaterCycle/era5cli/actions/workflows/test_codecov.yml/badge.svg
   :target: https://github.com/eWaterCycle/era5cli/actions/workflows/test_codecov.yml
   :alt: Github Actions

.. image:: https://codecov.io/gh/eWaterCycle/era5cli/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/eWaterCycle/era5cli
   :alt: Test coverage

.. image:: https://badge.fury.io/py/era5cli.svg
    :target: https://badge.fury.io/py/era5cli

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3252665.svg
   :target: https://doi.org/10.5281/zenodo.3252665

.. inclusion-marker-start-do-not-remove

A command line interface to download ERA5 data from the `Copernicus Climate Data Store <https://climate.copernicus.eu/>`_.

With era5cli you can:

- download meteorological data in GRIB/NetCDF, including ERA5 data from the preliminary back extension, and ERA5-Land data.
- list and retrieve information on available variables and pressure levels
- select multiple variables for several months and years
- split outputs by years, producing a separate file for every year instead of merging them in one file
- download multiple files at once
- extract data for a sub-region of the globe

.. inclusion-marker-end-do-not-remove

| Free software: Apache Software License 2.0
| Documentation: https://era5cli.readthedocs.io
