"""Python library to talk to the iDigBio search api

This has two main client interfaces:

 * ``idigbio.json``: basic access that talks JSON to the server and
   returns python dictionaries

 * ``idigbio.pandas``: uses the json library underneath but returns
   pandas dataframes for more advanced data processing


Both interfaces take parameters:

 * ``env``: Which environment to use {beta, prod}; defaults to prod
 * ``user``: api username; not necesary for searching
 * ``password``: api password; not necessary for searching


"""
from __future__ import absolute_import

import logging

__version__ = '0.7.1'


def json(*args, **kwargs):
    from .json_client import iDbApiJson
    return iDbApiJson(*args, **kwargs)


def pandas(*args, **kwargs):
    from .pandas_client import iDbApiPandas
    return iDbApiPandas(*args, **kwargs)

__all__ = ['json', 'pandas']

logging.getLogger(__name__).addHandler(logging.NullHandler())
