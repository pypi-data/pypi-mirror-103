========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - tests
      - | |travis| |codeclimate|
    * - package
      - | |version| |wheel| |supported-versions|

.. |travis| image:: https://travis-ci.com/mdhor/pj-scraper.svg?token=pMbsEqR4Vk8Qac97cZXa&branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/mdhor/pj-scraper

.. |codeclimate| image:: https://codeclimate.com/github/mdhor/pj-scraper/badges/gpa.svg
   :target: https://codeclimate.com/github/mdhor/pj-scraper
   :alt: CodeClimate Quality Status


.. |version| image:: https://img.shields.io/pypi/v/pj-scraper.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/pj-scraper

.. |wheel| image:: https://img.shields.io/pypi/wheel/pj-scraper.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/pj-scraper

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/pj-scraper.svg
    :alt: Supported versions
    :target: https://pypi.org/project/pj-scraper




.. end-badges

none

* Free software: MIT license

Installation
============

::

    pip install pj-scraper

Documentation
=============


To use the project:

.. code-block:: python

    from pj_scraper.scraper import Scraper
    s = Scraper()
    products = s.get_all_products_from_category("smartklokker")
    sellers_and_prices = s.get_sellers_and_prices_of_product_list(
        products["product_number"]
    )
