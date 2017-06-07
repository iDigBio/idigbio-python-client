# fetch_media.py

An example script that leverages the iDigBio search API to download media that match a query.

## Usage

```
$ python fetch_media.py --help
usage: fetch_media.py [-h] [-m MAX] [-s {thumbnail,webview,fullsize}]
                      [-o OUTPUT_DIR]
                      (-q QUERY | --query-file QUERY_FILE | --records-uuids-file RECORDS_UUIDS_FILE | --mediarecords-uuids-file MEDIARECORDS_UUIDS_FILE)

    This script will download media that are associated with the specimens
    returned by an iDigBio specimen record search query.

    The iDigBio Query Format is documented at

      https://github.com/idigbio/idigbio-search-api/wiki/Query-Format

    Notes on the --output-dir / -o parameter:

        If the specified output directory does not exist, it will be created.
        Omitting this parameter will cause a new directory to be created
        under the current directory, named in a timestamp-like style.

    ### Sample ###

    $ python fetch_media.py -o /tmp/idigbio_media_downloads -m 5 -q '{"genus": "acer"}'
    <snip>
    DOWNLOADING FINISHED with 5 successes and 0 failures

    Media downloads are in output directory: '/tmp/idigbio_media_downloads'

    $ ls -l /tmp/idigbio_media_downloads
    total 604
    -rw-rw-r-- 1 dstoner dstoner  93767 Jun  6 09:19 0c9b4669-edaa-467d-b240-f3311c764c04_webview.jpg
    -rw-rw-r-- 1 dstoner dstoner 114132 Jun  6 09:19 1f2dbb2b-75ba-48cb-b34c-1ca003b4a38d_webview.jpg
    -rw-rw-r-- 1 dstoner dstoner 147900 Jun  6 09:19 56f84bfe-5095-4fbb-b9e0-08cef3fdb448_webview.jpg
    -rw-rw-r-- 1 dstoner dstoner 117882 Jun  6 09:19 6a0d0c92-d2be-4ae5-9fef-60453778b0f0_webview.jpg
    -rw-rw-r-- 1 dstoner dstoner 136202 Jun  6 09:19 b98b9704-5ac5-4b53-b74d-d2d4d7d46ddd_webview.jpg
    ###

    The media record for the first download above would be viewable in the iDigBio portal at
    https://www.idigbio.org/portal/mediarecords/0c9b4669-edaa-467d-b240-f3311c764c04

optional arguments:
  -h, --help            show this help message and exit
  -m MAX, --max MAX     Maximum number of records to be returned from search
                        query. Default: 100, Maximum allowed value: 100000
  -s {thumbnail,webview,fullsize}, --size {thumbnail,webview,fullsize}
                        Size of derivative to download. Default: 'webview'
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        Directory path for downloaded media files. Default: a
                        new directory will be created under current directory
  -q QUERY, --query QUERY
                        query in iDigBio Query Format.
  --query-file QUERY_FILE
                        file path containing query string in iDigBio Query
                        Format
  --records-uuids-file RECORDS_UUIDS_FILE
                        file path containing list of iDigBio record uuids, one
                        per line
  --mediarecords-uuids-file MEDIARECORDS_UUIDS_FILE
                        file path containing list of iDigBio mediarecord
                        uuids, one per line

```

## Examples

Some of these example queries are taken directly from the iDigBio Query Format portion of the Search API documentation:

https://github.com/idigbio/idigbio-search-api/wiki/Query-Format


### Specify a query on the command-line

It is best to wrap the query string in single quotes to protect the contents from shell interpretation.


```
$ python fetch_media.py -q '{"scientificname":"isotelus maximus"}'

Using query:

{"scientificname":"isotelus maximus"}

OPERATING PARAMETERS...

Maximum number of media to fetch: 100
Media derivative size: webview
Output directory: /home/dstoner/git/idigbio-python-client/examples/fetch_media/20170607094735.99
Query Type: rq

EXECUTING SEARCH QUERY...


Search query produced 10 results.


BEGINNING DOWNLOADS NOW...

Downloading: 'https://api.idigbio.org/v2/media/267e2624-641f-4e34-9fdc-df59b14a5571?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/597f3eba-e40a-411f-af3e-5e6bb2d77c5c?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/f610a25a-ea1f-4f8b-9905-68523ff9e876?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/9ceb0644-03ea-47cb-9b58-bbb8ffd22a5b?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/c4aa9d24-8284-4207-8df1-294cbd80f634?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/1db5c01d-a54f-4049-b4cd-ffceda60a920?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/3e20720a-2f1b-4891-9d00-80028a3222b4?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/efd6753c-f276-4836-a05a-8771bd934ee5?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/c1bedf6b-2ddc-418f-aa9f-a4e69ec811fc?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/d29d364e-72f2-407c-9c81-428e14c7a2c3?size=webview'

DOWNLOADING FINISHED with 10 successes and 0 failures

Media downloads are in output directory: '/home/dstoner/git/idigbio-python-client/examples/fetch_media/20170607094735.99'

```

### Use a query specified in a file

```
$ cat query.txt
{
  "scientificname": "Anastrepha pallens Coquillett, 1904"
}


$ python fetch_media.py --query-file query.txt

Using query:

{
  "scientificname": "Anastrepha pallens Coquillett, 1904"
}



OPERATING PARAMETERS...

Maximum number of media to fetch: 100
Media derivative size: webview
Output directory: /home/dstoner/git/idigbio-python-client/examples/fetch_media/20170607095607.19
Query Type: rq

EXECUTING SEARCH QUERY...


Search query produced 7 results.


BEGINNING DOWNLOADS NOW...

Downloading: 'https://api.idigbio.org/v2/media/5cf7837c-7535-4263-a9a9-cfcf3a45b251?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/cd4fa6ce-95d3-4445-8733-75a6908944d8?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/ba7322f1-6468-4739-be87-a98ef8eb8bfc?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/0d0e07fa-9e86-4b71-8abf-140d163f9c16?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/8a0229f9-0b58-4017-af6e-f55121c28cab?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/500ba0ee-2e70-46ea-b80f-9e5a29753923?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/fbc36e25-16db-4828-a4c9-98049f0663fc?size=webview'

DOWNLOADING FINISHED with 7 successes and 0 failures

Media downloads are in output directory: '/home/dstoner/git/idigbio-python-client/examples/fetch_media/20170607095607.19'

```


### Searching within a radius around a geopoint

In addition to specifying a query file, the following command limits the number of media to 5 and specifies an output directory.

```
$ python fetch_media.py -m 5 --query-file query_geo.txt -o /tmp/idigbio_media_downloads

Using query:

{
  "geopoint": {
    "type": "geo_distance",
    "distance": "100km",
    "lat": -41.1119,
    "lon": 145.323
  }
}


OPERATING PARAMETERS...

Maximum number of media to fetch: 5
Media derivative size: webview
Output directory: /tmp/idigbio_media_downloads
Query Type: rq

EXECUTING SEARCH QUERY...


Search query produced 588 results.

*** WARNING: search query produced more results than the designated maximum number of media to fetch.
*** Use the -m or --max parameter to increase the maximum number of media to fetch.

BEGINNING DOWNLOADS NOW...

Downloading: 'https://api.idigbio.org/v2/media/63d218ad-4788-45ef-a11d-6d5ae75e9c19?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/81769eba-4c23-4dd7-8d1f-40a57d0cee94?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/90979c0b-1807-42c8-9180-cbc95a696d0a?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/9d6efc2a-ffec-4866-b3fc-2f0c7d3340d1?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/a01348b0-bed7-447d-982d-2e946db7ac5b?size=webview'

DOWNLOADING FINISHED with 5 successes and 0 failures

Media downloads are in output directory: '/tmp/idigbio_media_downloads'

```


### Specify a geo bounding box

```
$ cat query_geo_bounding.txt 
{
  "geopoint": {
    "type": "geo_bounding_box",
    "top_left": {
      "lat": 19.23,
      "lon": -130
    },
    "bottom_right": {
      "lat": -45.1119,
      "lon": 179.99999
    }
  }
}
```

In addition to specifying a query file, the following command limits the number of media to 5 and specifies an output directory.


```
$ python fetch_media.py -m 5 --query-file query_geo_bounding.txt  -o /tmp/idigbio_media_downloads

Using query:

{
  "geopoint": {
    "type": "geo_bounding_box",
    "top_left": {
      "lat": 19.23,
      "lon": -130
    },
    "bottom_right": {
      "lat": -45.1119,
      "lon": 179.99999
    }
  }
}


OPERATING PARAMETERS...

Maximum number of media to fetch: 5
Media derivative size: webview
Output directory: /tmp/idigbio_media_downloads
Query Type: rq

EXECUTING SEARCH QUERY...


Search query produced 1260449 results.

*** WARNING: search query produced more results than the designated maximum number of media to fetch.
*** Use the -m or --max parameter to increase the maximum number of media to fetch.

BEGINNING DOWNLOADS NOW...

Downloading: 'https://api.idigbio.org/v2/media/3a12b56f-70fd-4f14-aa9f-feead4aa4a9d?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/3b94d07c-31d9-42bb-b31c-708c20ff56f0?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/3bb22506-bcd9-4a56-bcd2-94d4b3cdfd46?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/3c1ae3e3-3df0-43cb-9864-c0b34f41e491?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/3c663c42-2f7e-435d-89eb-39e35961f0ed?size=webview'

DOWNLOADING FINISHED with 5 successes and 0 failures

Media downloads are in output directory: '/tmp/idigbio_media_downloads'

```

### Specify a query based on a list of uuids

If you have already processed a list of downloaded iDigBio records and have a list of record
or mediarecord uuids, those uuids can be placed in a text file, one per line, and fetch_media
can download the associated media.

#### iDigBio record uuids

Note that in this case the records have more than one media associated with them so we end up with more than 3 images after specifying only 3 record uuids.

```
$ cat record_uuids_list.txt 
a494a2a6-b64b-4f99-b26c-53bfdcd54876
ddc56589-7009-4fe6-81d8-d9c9219a503f
9f7f4ba7-0def-4b01-b806-9089dcb7382c

$ python fetch_media.py --records-uuids-file record_uuids_list.txt -o /tmp/idigbio_media_downloads

Using query:

{"uuid":["a494a2a6-b64b-4f99-b26c-53bfdcd54876", "ddc56589-7009-4fe6-81d8-d9c9219a503f", "9f7f4ba7-0def-4b01-b806-9089dcb7382c"]}

OPERATING PARAMETERS...

Maximum number of media to fetch: 100
Media derivative size: webview
Output directory: /tmp/idigbio_media_downloads
Query Type: rq

EXECUTING SEARCH QUERY...


Search query produced 6 results.


BEGINNING DOWNLOADS NOW...

Downloading: 'https://api.idigbio.org/v2/media/24be5c10-9b1d-418f-85d4-f13b52e9644e?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/6976b7a3-1547-49a7-8601-febfb90d5e44?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/8fc71122-9fc9-4d5c-8bb2-17a315847f9c?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/88e21956-702d-4e1a-ba71-0d695159b9a9?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/b7cf0d3b-be0f-4d47-9361-0ef0521df28f?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/fbc3237a-1816-4cee-8025-c364d37280d4?size=webview'

DOWNLOADING FINISHED with 6 successes and 0 failures

Media downloads are in output directory: '/tmp/idigbio_media_downloads'

```

#### iDigBio mediarecord uuids

```
$ python fetch_media.py --mediarecords-uuids-file mediarecord_uuids_list.txt -o /tmp/idigbio_media_downloads

Using query:

{"uuid":["787d60f7-3fb7-4b82-8846-b5b4123761c1", "9c84908f-170f-44eb-ad6d-6d3fec5032a6", "845f80e8-02d7-49dd-aef7-fc58cec36c89"]}

OPERATING PARAMETERS...

Maximum number of media to fetch: 100
Media derivative size: webview
Output directory: /tmp/idigbio_media_downloads
Query Type: mq

EXECUTING SEARCH QUERY...


Search query produced 3 results.


BEGINNING DOWNLOADS NOW...

Downloading: 'https://api.idigbio.org/v2/media/845f80e8-02d7-49dd-aef7-fc58cec36c89?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/9c84908f-170f-44eb-ad6d-6d3fec5032a6?size=webview'
Downloading: 'https://api.idigbio.org/v2/media/787d60f7-3fb7-4b82-8846-b5b4123761c1?size=webview'

DOWNLOADING FINISHED with 3 successes and 0 failures

Media downloads are in output directory: '/tmp/idigbio_media_downloads'


```