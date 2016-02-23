from __future__ import absolute_import

import logging
from .json_client import iDbApiJson as json
from .pandas_client import iDbApiPandas as pandas

__all__ = ['json', 'pandas']
__version__ = '0.4.3'

logging.getLogger(__name__).addHandler(logging.NullHandler())
