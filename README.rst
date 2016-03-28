idigbio-python-client
=====================

.. image:: https://img.shields.io/pypi/v/idigbio.svg
    :target: https://pypi.python.org/pypi/idigbio

.. image:: https://img.shields.io/travis/iDigBio/idigbio-python-client.svg
        :target: https://travis-ci.org/iDigBio/idigbio-python-client

A python client for the `iDigBio <https://www.idigbio.org/>`_ iDigBio v2 API.

Installation
------------

.. code-block::

    pip install idigbio

If you want to use the Pandas Data Frame interface you need to install
pandas as well.

.. code-block::

    pip install idigbio pandas

Basic Usage
-----------

Returning JSON from the API.

.. code-block:: python

    import idigbio
    api = idigbio.json()
    json_output = api.search_records()

Returning a Pandas Data Frame.

.. code-block:: python

    import idigbio
    api = idigbio.pandas()
    pandas_output = api.search_records()

See the `Search API docs
<https://github.com/idigbio/idigbio-search-api/wiki>`_ for info about
the endpoint parameters.


Examples
++++++++

View a Record By UUID

.. code-block:: python

    import idigbio
    api = idigbio.json()
    record = api.view("records","1db58713-1c7f-4838-802d-be784e444c4a")

Search for a Record by scientific name

.. code-block:: python

    import idigbio
    api = idigbio.json()
    record_list = api.search_records(rq={"scientificname": "puma concolor"})

Search for Records that have images

.. code-block:: python

    import idigbio
    api = idigbio.json()
    record_list = api.search_records(rq={"scientificname": "puma concolor", "hasImage": True})

Search for a MediaRecords by record property

.. code-block:: python

    import idigbio
    api = idigbio.json()
    mediarecord_list = api.search_media(rq={"scientificname": "puma concolor", "hasImage": True})

Create a heat map for a genus

.. code-block:: python

    import idigbio
    api = idigbio.json()
    m = api.create_map(rq={"genus": "acer"}, t="geohash")
    m.save_map_image("acer_map_geohash", 2)

Create a point map for a genus

.. code-block:: python

    import idigbio
    api = idigbio.json()
    m = api.create_map(rq={"genus": "acer"}, t="points")
    m.save_map_image("acer_map_points", 2)

Create a zoomed in point map for a bounding box

.. code-block:: python

    import idigbio
    api = idigbio.json()
    bbox = {"type": "geo_bounding_box", "bottom_right": {"lat": 29.642979999999998, "lon": -82.00}, "top_left": {"lat": 29.66298, "lon": -82.35315800000001}}
    m = api.create_map(
        rq={"geopoint": bbox}
    )
    m.save_map_image("test.png", None, bbox=bbox)


Create a summary of kingdom and phylum data

.. code-block:: python

    import idigbio
    api = idigbio.json()
    summary_data = api.top_records(fields=["kingdom", "phylum"])

Get the number of Records for a search by scientific name

.. code-block:: python

    import idigbio
    api = idigbio.json()
    count = api.count_records(rq={"scientificname": "puma concolor"})

Get the number of MediaRecords for a search by scientific name

.. code-block:: python

    import idigbio
    api = idigbio.json()
    count = api.count_media(rq={"scientificname": "puma concolor"})

Get the histogram of Collection Dates for a search by record property, for the last 10 years

.. code-block:: python

    import idigbio
    api = idigbio.json()
    histogram_data = api.datehist(
        rq={"scientificname": "puma concolor"},
        top_fields=["institutioncode"], min_date="2005-01-01")
