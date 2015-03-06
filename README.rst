================
idigbio-python-client
================
A python client for the idigbio v2 API

Two Forms
=============
Returning JSON from the API as an iterator.
::
  import idigbio
  api = idigbio.json()
  json_output = api.search_records()

Returning a Pandas Data Frame from the JSON API.
::
  import idigbio
  api = idigbio.pandas()
  pandas_output = api.search_records()