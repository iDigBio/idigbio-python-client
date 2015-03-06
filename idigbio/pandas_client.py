import pandas
from .json_client import iDbApiJson

class iDbApiPandas(object):
    def __init__(self,env="beta",debug=False):
        """
            env: Which environment to use. Defaults to beta, the only currently supported string."
        """
        self.__api = iDbApiJson(env=env,debug=debug)

    def __yield_dicts(self,data):
        for r in data["items"]:
            yield r["indexTerms"]

    def __yield_multi_call(self,call,offsets,kwargs):
        for offset in offsets:
            kwargs["offset"] = offset
            for r in self.__yield_dicts(call(**kwargs)):
                yield r

    def search_records(self,**kwargs):
        """
            rq  Search Query in iDigBio Query Format, using Record Query Fields
            sort    field to sort on, pick from Record Query Fields
            fields  a list of fields to return, specified using the fieldName parameter from Fields with type records
            fields_exclude  a list of fields to exclude, specified using the fieldName parameter from Fields with type records
            limit   max results
            offset  skip results

            Returns idigbio record format (legacy api), plus additional top level keys with parsed index terms. Returns None on error.
        """

        if "limit" in kwargs and kwargs["limit"] > 5000:
            if "offset" not in kwargs:
                kwargs["offset"] = 0
            total_limit = kwargs["limit"]
            kwargs["limit"] = 5000
            offsets = [kwargs["offset"]+x for x in range(0,total_limit,5000)]
            return pandas.DataFrame.from_records(self.__yield_multi_call(self.__api.search_records,offsets,kwargs),index="uuid")
        else:
            return pandas.DataFrame.from_records(self.__yield_dicts(self.__api.search_records(**kwargs)),index="uuid")

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
        if "limit" in kwargs and kwargs["limit"] > 5000:
            if "offset" not in kwargs:
                kwargs["offset"] = 0
            total_limit = kwargs["limit"]
            kwargs["limit"] = 5000
            offsets = [kwargs["offset"]+x for x in range(0,total_limit,5000)]
            return pandas.DataFrame.from_records(self.__yield_multi_call(self.__api.search_media,offsets,kwargs),index="uuid")
        else:
            return pandas.DataFrame.from_records(self.__yield_dicts(self.__api.search_media(**kwargs)),index="uuid")

    def __top_recuse(self,top_fields,top_records):
        if len(top_fields) == 0:
            yield [top_records["itemCount"]]
        else:
            for k in top_records[top_fields[0]]:
                for v in self.__top_recuse(top_fields[1:],top_records[top_fields[0]][k]):
                    yield [k] + v

    def top_records(self,top_fields=["scientificname"],**kwargs):
        r = self.__api.top_records(top_fields=top_fields,**kwargs)
        return pandas.DataFrame.from_records(self.__top_recuse(top_fields,r),columns=top_fields + ["count"])

    def top_media(self,top_fields=["flags"],**kwargs):
        r = self.__api.top_media(top_fields=top_fields,**kwargs)
        return pandas.DataFrame.from_records(self.__top_recuse(top_fields,r),columns=top_fields + ["count"])

    def count_records(self,**kwargs):
        return self.__api.count_records(**kwargs)

    def count_media(self,**kwargs):
        return self.__api.count_media(**kwargs)

    # TODO
    # def datehist(self,**kwargs):
    #     return self._api.datehist(**kwargs)

    # def stats(self,t,**kwags):
    #     return self._api.stats(t,**kwargs)