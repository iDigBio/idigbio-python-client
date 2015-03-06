idigbio-python-client
=====================

A python client for the idigbio v2 API

Two Forms
---------

Returning JSON from the API as an iterator.

.. code-block:: python
    import idigbio
    api = idigbio.json()
    json_output = api.search_records()
    ...

Returning a Pandas Data Frame from the JSON API.

.. code-block:: python
    import idigbio
    api = idigbio.pandas()
    pandas_output = api.search_records()
    ...