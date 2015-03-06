idigbio-python-client
=====================

.. image:: https://img.shields.io/pypi/v/idigbio.svg
    :target: https://pypi.python.org/pypi/idigbio

.. image:: https://img.shields.io/travis/iDigBio/idigbio-python-client.svg
        :target: https://travis-ci.org/iDigBio/idigbio-python-client

A python client for the idigbio v2 API

.. code-block:: 

    pip install idigbio

For documentation of the endpoint parameters go to: https://github.com/idigbio/idigbio-search-api/wiki

Two Forms
---------

Returning JSON from the API as an iterator.

.. code-block:: python

    import idigbio
    api = idigbio.json()
    json_output = api.search_records()

Returning a Pandas Data Frame from the JSON API.

.. code-block:: python

    import idigbio
    api = idigbio.pandas()
    pandas_output = api.search_records()
