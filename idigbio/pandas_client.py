import logging
import pandas
from .json_client import iDbApiJson
from itertools import chain
try:
    from future_builtins import map
except ImportError:
    pass

MAX_BATCH_SIZE = 5000

log = logging.getLogger(__name__)


class iDbApiPandas(object):
    def __init__(self, env="prod", user=None, password=None):
        """
            env: Which environment to use. Defaults to prod."
        """
        self.__api = iDbApiJson(env=env, user=user, password=password)

    def __search_base(self, apifn, **kwargs):
        def yd(data):
            for r in data["items"]:
                yield r["indexTerms"]

        if "limit" in kwargs and kwargs["limit"] > MAX_BATCH_SIZE:
            def one(offset, total_limit):
                while offset < total_limit:
                    batch = min(MAX_BATCH_SIZE, total_limit - offset)
                    log.debug("Querying at offset %s", offset)
                    data = apifn(offset=offset, limit=batch, **kwargs)
                    yield data
                    if len(data["items"]) < batch:
                        log.debug("Exiting early, no more records on server")
                        break
                    offset += batch
            datagen = one(kwargs.pop("offset", 0), kwargs.pop("limit"))
            data = next(datagen)
            if data and len(data["items"]) > 0:
                records = chain(
                    yd(data),
                    chain.from_iterable(map(yd, datagen)))
                return pandas.DataFrame.from_records(records, index="uuid")
        else:
            data = apifn(**kwargs)
            if data["itemCount"] > 0:
                return pandas.DataFrame.from_records(yd(data), index="uuid")
        return None

    def search_records(self, **kwargs):
        """
            rq  Search Query in iDigBio Query Format, using Record Query Fields
            sort    field to sort on, pick from Record Query Fields
            fields  a list of fields to return, specified using the fieldName parameter from Fields with type records
            fields_exclude  a list of fields to exclude, specified using the fieldName parameter from Fields with type records
            limit   max results
            offset  skip results

            Returns idigbio record format (legacy api), plus additional top level keys with parsed index terms. Returns None on error.
        """

        return self.__search_base(apifn=self.__api.search_records, **kwargs)

    def search_media(self,**kwargs):
        """
            mq  Search Query in iDigBio Query Format, using Media Query Fields
            rq  Search Query in iDigBio Query Format, using Record Query Fields
            sort    field to sort on, pick from Media Query Fields
            fields  a list of fields to return, specified using the fieldName parameter from Fields with type mediarecords
            fields_exclude  a list of fields to exclude, specified using the fieldName parameter from Fields with type records
            limit   max results
            offset  skip results

            Returns idigbio record format (legacy api), plus additional top level keys with parsed index terms. Returns None on error.
        """
        return self.__search_base(apifn=self.__api.search_media, **kwargs)

    def __top_recuse(self, top_fields, top_records):
        if len(top_fields) == 0:
            yield [top_records["itemCount"]]
        else:
            for k in top_records[top_fields[0]]:
                for v in self.__top_recuse(top_fields[1:], top_records[top_fields[0]][k]):
                    yield [k] + v

    def top_records(self, top_fields=["scientificname"], **kwargs):
        r = self.__api.top_records(top_fields=top_fields, **kwargs)
        return pandas.DataFrame.from_records(
            self.__top_recuse(top_fields, r), columns=top_fields + ["count"])

    def top_media(self, top_fields=["flags"], **kwargs):
        r = self.__api.top_media(top_fields=top_fields, **kwargs)
        return pandas.DataFrame.from_records(
            self.__top_recuse(top_fields, r), columns=top_fields + ["count"])

    def count_records(self, **kwargs):
        return self.__api.count_records(**kwargs)

    def count_media(self, **kwargs):
        return self.__api.count_media(**kwargs)

    # TODO
    # def datehist(self,**kwargs):
    #     return self._api.datehist(**kwargs)

    # def stats(self,t,**kwags):
    #     return self._api.stats(t,**kwargs)
