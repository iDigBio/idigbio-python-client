import pandas
from json_client import iDbApiJson

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

def main():
    from datetime import datetime
    api = iDbApiPandas(debug=True)
    t = datetime.now()
    print api.search_records().shape
    print datetime.now() - t

    t = datetime.now()
    print api.search_records(limit=1000).shape
    print datetime.now() - t

    t = datetime.now()
    print api.search_records(limit=10000).shape
    print datetime.now() - t    

    t = datetime.now()
    print api.search_records(limit=100000).shape
    print datetime.now() - t

    t = datetime.now()
    print api.search_media().shape
    print datetime.now() - t

    t = datetime.now()
    print api.search_media(limit=1000).shape
    print datetime.now() - t

    t = datetime.now()
    print api.search_media(limit=10000).shape   
    print datetime.now() - t

    t = datetime.now()
    print api.search_media(limit=100000).shape
    print datetime.now() - t
   

if __name__ == '__main__':
    main()