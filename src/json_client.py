import requests
import json
import urllib
import traceback
import os

global_disable_images = False
try:
    import PIL.Image as Image
except:
    global_disable_images = True

try:
    from cStringIO import StringIO
except:
    from StringIO import StringIO

class BadEnvException(Exception):
    pass

class MapNotCreatedException(Exception):
    pass

class ImagesDisabledException(Exception):
    pass

class iDigBioMap(object):
    def __init__(self,api,rq={},style=None,t="auto",disable_images=False):
        self.__api = api
        self._disable_images = disable_images or global_disable_images
        self._map_def = self.__api._api_post("/v2/mapping",rq=rq,style=style,type=t)
        if self._map_def is None:
            raise MapNotCreatedException()
        self._short_code = self._map_def["shortCode"]
        self._tiles = self._map_def["tiles"]

    def definition(self):
        return self.__api._api_get("/v2/mapping/{0}".format(self._short_code))

    def json_tile(self,z,x,y):
        return self.__api._api_get("/v2/mapping/{0}/{1}/{2}/{3}.json".format(self._short_code,z,x,y))        

    def utf8grid_tile(self,z,x,y):
        return self.__api._api_get("/v2/mapping/{0}/{1}/{2}/{3}.grid.json".format(self._short_code,z,x,y))        

    def png_tile(self,z,x,y):
        if self._disable_images:
            raise ImagesDisabledException()
        tile = self.__api._api_get("/v2/mapping/{0}/{1}/{2}/{3}.png".format(self._short_code,z,x,y),raw=True)
        if tile is None:
            return None
        else:
            return Image.open(StringIO(tile))

    def points(self,lat,lon,zoom,sort=None,limit=100,offset=None):
        return self.__api._api_get("/v2/mapping/{0}/points".format(self._short_code),lat=lat,lon=lon,zoom=zoom,sort=sort,limit=limit,offset=offset)

    def save_map_image(self, filename, zoom):
        s = requests.Session()
        if self._disable_images:
            raise ImagesDisabledException()        
        tiles = range(0,2**zoom)
        im = Image.new("RGB", (len(tiles)*256,len(tiles)*256))
        for x in tiles:
            for y in tiles:
                r = s.get("http://b.tile.openstreetmap.org/{z}/{x}/{y}.png".format(z=zoom, x=x, y=y))
                r.raise_for_status()
                bim = Image.open(StringIO(r.content))                
                tim = self.png_tile(zoom,x,y)
                im.paste(bim, (x*256,y*256))
                im.paste(tim, (x*256,y*256), tim)
        im.save("{0}.png".format(filename),"PNG")        


class iDbApiJson(object):
    """ iDigBio Search API Json Client """

    def __init__(self,env="beta",debug=False,retries=3):
        """
            env: Which environment to use. Defaults to beta, the only currently supported string."
        """
        self.debug = debug
        self.retries = retries

        if env == "beta":
            self._api_url = "http://beta-search.idigbio.org"
        else:
            raise BadEnvException

        self.s = requests.Session()

    def _api_get(self, slug, **kwargs):
        retries = self.retries
        raw = False
        if "raw" in kwargs:
            raw = kwargs["raw"]
            del kwargs["raw"]

        for arg in kwargs.keys():
            if isinstance(kwargs[arg],(dict,list)):
                kwargs[arg] = json.dumps(kwargs[arg])
            elif kwargs[arg] is None:
                del kwargs[arg]
        qs = urllib.urlencode(kwargs)
        while retries > 0:
            try:
                if self.debug:
                    print self._api_url + slug + "?" + qs
                r = self.s.get(self._api_url + slug + "?" + qs)
                r.raise_for_status()
                if raw:
                    return r.content
                else:
                    return r.json()    
            except:
                if self.debug:
                    traceback.print_exc()
                retries -= 1
        return None

    def _api_post(self, slug, **kwargs):
        retries = self.retries
        raw = False
        if "raw" in kwargs:
            raw = kwargs["raw"]
            del kwargs["raw"]

        for arg in kwargs.keys():
            if kwargs[arg] is None:
                del kwargs[arg]

        while retries > 0:
            try:
                body = json.dumps(kwargs)
                if self.debug:
                    print self._api_url, slug, qs
                r = self.s.post(self._api_url + slug,data=body)
                r.raise_for_status()
                if raw:
                    return r.content
                else:
                    return r.json()
            except:
                if self.debug:
                    traceback.print_exc()            
                retries -= 1
        return None

    def view(self,t,uuid):
        """
            t: the type to view. Supported types: records, media (mediarecords), recordsets, publishers
            uuid: the uuid to view.
        """
        return self._api_get("/v2/view/{0}/{1}".format(t,uuid))

    def search_records(self,rq={},limit=100,offset=0,sort=None,fields=None,fields_exclude=["data.*"]):
        """
            rq  Search Query in iDigBio Query Format, using Record Query Fields
            sort    field to sort on, pick from Record Query Fields
            fields  a list of fields to return, specified using the fieldName parameter from Fields with type records
            fields_exclude  a list of fields to exclude, specified using the fieldName parameter from Fields with type records
            limit   max results
            offset  skip results

            Returns idigbio record format (legacy api), plus additional top level keys with parsed index terms. Returns None on error.
        """        
        return self._api_post("/v2/search/records",rq=rq,limit=limit,offset=offset,sort=sort,fields=fields,fields_exclude=fields_exclude)

    def search_media(self,mq={},rq={},limit=100,offset=0,sort=None,fields=None,fields_exclude=["data.*"]):
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
        return self._api_post("/v2/search/records",rq=rq,limit=limit,offset=offset,sort=sort,fields=fields,fields_exclude=fields_exclude)

    def create_map(self,rq={},style=None,t="auto",disable_images=False):
        return iDigBioMap(self,rq=rq,style=style,t=t,disable_images=disable_images)

def main():
    api = iDbApiJson(debug=True)

if __name__ == '__main__':
    main()