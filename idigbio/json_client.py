import logging
import math
import requests
import json
import traceback

from idigbio import util

try:
    # Python 2
    from urllib import urlencode
except:
    # Python 3
    from urllib.parse import urlencode

global_disable_images = False
try:
    import PIL.Image as Image
except:
    global_disable_images = True

try:
    # Python 2 C
    from cStringIO import StringIO as io_ify
except:
    try:
        # Python 2 native
        from StringIO import StringIO as io_ify
    except:
        # Python 3
        from io import BytesIO as io_ify

log = logging.getLogger(__name__)


FIELDS_EXCLUDE_DEFAULT = ['data.*']


def level_dic():
    '''
    http://wiki.openstreetmap.org/wiki/Zoom_levels
    '''
    # return data
    data = {0: 360.0,
            1: 180.0,
            2: 90.0,
            3: 45.0,
            4: 22.5,
            5: 11.25,
            6: 5.625,
            7: 2.813,
            8: 1.406,
            9: 0.703,
            10: 0.352,
            11: 0.176,
            12: 0.088,
            13: 0.044,
            14: 0.022,
            15: 0.011,
            16: 0.005,
            17: 0.003,
            18: 0.001,
            19: 0.0005}
    return data


def getzoom(min_lon, max_lon, min_lat, max_lat):
    data = level_dic()  # our presets
    r = 4
    dne = max(round(max_lat - min_lat, r),
              round(max_lon - min_lon, r))  # ne: North East point
    mylist = [round(i, r) for i in data.values()] + [dne]
    new = sorted(mylist, reverse=True)
    return new.index(dne)


def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = int((lon_deg + 180.0) / 360.0 * n)
    ytile = int((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return (xtile, ytile)


class BadEnvException(Exception):
    pass


class MapNotCreatedException(Exception):
    pass


class ImagesDisabledException(Exception):
    pass


def make_session(user=None, password=None):
    import idigbio
    s = requests.Session()
    if user and password:
        s.auth = (user, password)
    s.headers["User-Agent"] = "idigbio-python-client/" + idigbio.__version__
    return s


class iDigBioMap(object):
    def __init__(self, api, rq={}, style=None, t="auto", disable_images=False):
        self.__api = api
        self._disable_images = disable_images or global_disable_images
        self._map_def = self.__api._api_post(
            "/v2/mapping", rq=rq, style=style, type=t)
        if self._map_def is None:
            raise MapNotCreatedException()
        self._short_code = self._map_def["shortCode"]
        self._tiles = self._map_def["tiles"]

    def definition(self):
        return self.__api._api_get("/v2/mapping/{0}".format(self._short_code))

    def json_tile(self, z, x, y):
        return self.__api._api_get(
            "/v2/mapping/{0}/{1}/{2}/{3}.json".format(
                self._short_code, z, x, y))

    def utf8grid_tile(self, z, x, y):
        return self.__api._api_get(
            "/v2/mapping/{0}/{1}/{2}/{3}.grid.json".format(
                self._short_code, z, x, y))

    def png_tile(self, z, x, y):
        if self._disable_images:
            raise ImagesDisabledException()
        tile = self.__api._api_get(
            "/v2/mapping/{0}/{1}/{2}/{3}.png".format(
                self._short_code, z, x, y), raw=True)
        if tile is None:
            return None
        else:
            return Image.open(io_ify(tile))

    def points(self, lat, lon, zoom, sort=None, limit=100, offset=None):
        return self.__api._api_get(
            "/v2/mapping/{0}/points".format(self._short_code),
            lat=lat, lon=lon, zoom=zoom, sort=sort, limit=limit, offset=offset)

    def save_map_image(self, filename, zoom, bbox=None):
        x_tiles = None
        y_tiles = None

        if zoom is None and bbox is not None:
            zoom = getzoom(
                bbox["bottom_right"]["lat"],
                bbox["top_left"]["lat"],
                bbox["top_left"]["lon"],
                bbox["bottom_right"]["lon"]
            )

        if bbox is not None:
            top_left_tile = deg2num(
                bbox["top_left"]["lat"],
                bbox["top_left"]["lon"],
                zoom
            )

            bottom_right_tile = deg2num(
                bbox["bottom_right"]["lat"],
                bbox["bottom_right"]["lon"],
                zoom
            )

            x_tiles = range(top_left_tile[0], bottom_right_tile[0]+1)
            y_tiles = range(top_left_tile[1], bottom_right_tile[1]+1)

        if x_tiles is None:
            x_tiles = range(0, 2**zoom)
        if y_tiles is None:
            y_tiles = range(0, 2**zoom)

        s = make_session()
        if self._disable_images:
            raise ImagesDisabledException()
        im = Image.new("RGB", (len(x_tiles) * 256, len(y_tiles) * 256))
        x_tile_count = 0
        for x in x_tiles:
            y_tile_count = 0
            for y in y_tiles:
                r = s.get(
                    "http://b.tile.openstreetmap.org/{z}/{x}/{y}.png".format(
                        z=zoom, x=x, y=y))
                r.raise_for_status()
                bim = Image.open(io_ify(r.content))
                tim = self.png_tile(zoom, x, y)
                im.paste(bim, (x_tile_count * 256, y_tile_count * 256))
                im.paste(tim, (x_tile_count * 256, y_tile_count * 256), tim)
                y_tile_count += 1
            x_tile_count += 1
        im.save("{0}.png".format(filename), "PNG")
        s.close()


class iDbApiJson(object):
    """ iDigBio Search API Json Client """

    def __init__(self, env="prod", retries=3, user=None, password=None):
        """
            env: Which environment to use. Defaults to prod."
        """
        self.retries = retries

        if env == "prod":
            self._api_urls = {
                "base": "https://search.idigbio.org",
                "/v2/media": "https://api.idigbio.org",
                "/v2/download": "https://api.idigbio.org"
            }
        elif env == "beta":
            self._api_urls = {
                "base": "https://beta-search.idigbio.org",
                "/v2/media": "https://beta-api.idigbio.org",
                "/v2/download": "https://beta-api.idigbio.org"
            }
        elif env == "dev":
            self._api_urls = {
                "base": "https://localhost:19196",
                "/v2/media": "http://localhost:19197",
                "/v2/download": "http://localhost:19197"
            }
        else:
            raise BadEnvException()

        self.s = make_session(user=user, password=password)

    def __del__(self):
        self.s.close()

    def _api_get(self, slug, **kwargs):
        retries = self.retries
        raw = kwargs.pop('raw', False)

        api_url = self._api_urls.get(slug, self._api_urls.get("base"))

        for arg in list(kwargs):
            if isinstance(kwargs[arg], (dict, list)):
                kwargs[arg] = json.dumps(kwargs[arg])
            elif kwargs[arg] is None:
                del kwargs[arg]
        qs = urlencode(kwargs)
        while retries > 0:
            try:
                log.debug("Querying: %r", api_url + slug + "?" + qs)
                r = self.s.get(api_url + slug + "?" + qs)
                r.raise_for_status()
                if raw:
                    return r.content
                else:
                    return r.json()
            except:
                log.debug(traceback.print_exc())
                retries -= 1
        return None

    def _api_post(self, slug, **kwargs):
        retries = self.retries
        raw = kwargs.pop('raw', False)
        files = kwargs.pop('files', None)
        params = kwargs.pop('params', None)

        api_url = self._api_urls.get(slug, self._api_urls.get("base"))

        for arg in list(kwargs):
            if kwargs[arg] is None:
                del kwargs[arg]

        while retries > 0:
            try:
                body = json.dumps(kwargs)
                if files is None:
                    log.debug("POSTing: %r\n%s", slug, body)
                    r = self.s.post(
                        api_url + slug,
                        data=kwargs,
                        params=params
                    )
                else:
                    # you must seek the file before sending,
                    # especially on the retry loop
                    for k in files:
                        files[k].seek(0)
                    log.debug("POSTing + Files: %r\n%s", slug, body)
                    r = self.s.post(
                        api_url + slug,
                        data=kwargs,
                        files=files,
                        params=params
                    )

                r.raise_for_status()
                if raw:
                    return r.content
                else:
                    return r.json()
            except:
                log.exception("Error posting: %s", r.content)
                retries -= 1
        return None

    def view(self, t, uuid):
        """
            t: the type to view. Supported types: records, media (mediarecords), recordsets, publishers
            uuid: the uuid to view.
        """
        return self._api_get("/v2/view/{0}/{1}".format(t, uuid))

    def search_records(self, rq={}, limit=100, offset=0, sort=None,
                       fields=None, fields_exclude=FIELDS_EXCLUDE_DEFAULT):
        """
            rq  Search Query in iDigBio Query Format, using Record Query Fields
            sort    field to sort on, pick from Record Query Fields
            fields  a list of fields to return, specified using the fieldName parameter from Fields with type records
            fields_exclude  a list of fields to exclude, specified using the fieldName parameter from Fields with type records
            limit   max results
            offset  skip results

            Returns idigbio record format (legacy api), plus additional top level keys with parsed index terms. Returns None on error.
        """
        if fields is not None and fields_exclude is FIELDS_EXCLUDE_DEFAULT:
            fields_exclude = None

        return self._api_post("/v2/search/records",
                              rq=rq, limit=limit, offset=offset, sort=sort,
                              fields=fields, fields_exclude=fields_exclude)

    def search_media(self, mq={}, rq={}, limit=100, offset=0, sort=None,
                     fields=None, fields_exclude=FIELDS_EXCLUDE_DEFAULT):
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
        if fields is not None and fields_exclude is FIELDS_EXCLUDE_DEFAULT:
            fields_exclude = None
        return self._api_post("/v2/search/records",
                              rq=rq, limit=limit, offset=offset, sort=sort,
                              fields=fields, fields_exclude=fields_exclude)

    def create_map(self, rq={}, style=None, t="auto", disable_images=False):
        return iDigBioMap(
            self, rq=rq, style=style, t=t, disable_images=disable_images)

    def top_records(self, rq={}, top_fields=None, count=None):
        return self._api_post("/v2/summary/top/records",
                              rq=rq, top_fields=top_fields, count=count)

    def top_media(self, mq={}, rq={}, top_fields=None, count=None):
        return self._api_post("/v2/summary/top/media", mq=mq, rq=rq,
                              top_fields=top_fields, count=count)

    def count_records(self, rq={}):
        r = self._api_post("/v2/summary/count/records", rq=rq)
        if r is not None:
            return r["itemCount"]
        else:
            return None

    def count_media(self, mq={}, rq={}):
        r = self._api_post("/v2/summary/count/media", mq=mq, rq=rq)
        if r is not None:
            return r["itemCount"]
        else:
            return None

    def datehist(self, rq={}, top_fields=None, count=None, date_field=None,
                 min_date=None, max_date=None, date_interval=None):
        return self._api_post(
            "/v2/summary/datehist",
            rq=rq, top_fields=top_fields, count=count, date_field=date_field,
            min_date=min_date, max_date=max_date, date_interval=date_interval)

    def stats(self, t, recordset=None, min_date=None, max_date=None,
              date_interval=None):
        return self._api_post("/v2/summary/stats/{0}".format(t),
                              recordset=recordset,
                              min_date=min_date, max_date=max_date,
                              date_interval=date_interval)

    def upload(self, filereference, localfile, media_type=None):
        if not self.s.auth:
            raise Exception("Unauthorized")
        if not localfile:
            raise ValueError("Must have local copy of file to upload")
        files = {'file': open(localfile, 'rb')}
        p = {
            "filereference": filereference,
            "media_type": media_type
        }
        return self._api_post("/v2/media", files=files, params=p)

    def addreference(self, filereference, localfile):
        if not self.s.auth:
            raise Exception("Unauthorized")
        if not localfile:
            raise ValueError("Must have local copy of file to upload")
        etag = util.calcFileHash(localfile)
        p = {'filereference': filereference,
             'etag': etag}
        return self._api_post("/v2/media", params=p)

    def addurl(self, filereference, media_type=None, mime_type=None):
        if not self.s.auth:
            raise Exception("Unauthorized")
        p = {
            "filereference": filereference,
            "media_type": media_type,
            "mime": mime_type
        }
        return self._api_post("/v2/media", **p)

if __name__ == '__main__':
    api = iDbApiJson()
    bbox = {"type": "geo_bounding_box",
            "bottom_right": {"lat": 29.642979999999998, "lon": -82.00},
            "top_left": {"lat": 29.66298, "lon": -82.35315800000001}}
    m = api.create_map(
        rq={"geopoint": bbox}
    )
    m.save_map_image("test.png", None, bbox=bbox)
