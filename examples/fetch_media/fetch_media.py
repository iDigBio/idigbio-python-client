from __future__ import print_function
try:
    from idigbio.json_client import iDbApiJson
    import requests
    import shutil
    import os
    import time
    import argparse
    import json
except ImportError as e:
    print ("IMPORT ERROR (This exception is likely caused by a missing module): '{0}'".format(e))
    raise SystemExit

help_blob = """

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

"""

# MAX_MAX_COUNT is a safety limit to keep an erroneous query from downloading all of iDigBio's media.
# Change this value if you are legitimately trying to download more than 100k media.
# Also, please consider letting us know that you are doing this because we are interested
# in these kinds of use cases.   idigbio@acis.ufl.edu
MAX_MAX_COUNT = 100000

DEFAULT_MAX_COUNT = 100
SIZES = ["thumbnail", "webview", "fullsize"]
DEFAULT_SIZE = "webview"
DEFAULT_OUTPUT_DIR = None

argparser = argparse.ArgumentParser(description=help_blob, formatter_class=argparse.RawDescriptionHelpFormatter)
argparser.add_argument("-m", "--max", type=int, default=DEFAULT_MAX_COUNT,
                       help="Maximum number of records to be returned from search query. Default: {0}, Maximum allowed value: {1}".format(DEFAULT_MAX_COUNT,MAX_MAX_COUNT))
argparser.add_argument("-s", "--size", choices=SIZES, default=DEFAULT_SIZE, 
                       help="Size of derivative to download. Default: '{0}'".format(DEFAULT_SIZE))
argparser.add_argument("-o", "--output-dir", default=DEFAULT_OUTPUT_DIR, 
                       help="Directory path for downloaded media files. Default: a new directory will be created under current directory")
arg_group = argparser.add_mutually_exclusive_group(required=True)
arg_group.add_argument("-q", "--query", 
                       help="query in iDigBio Query Format.")
arg_group.add_argument("--query-file",
                       help="file path containing query string in iDigBio Query Format")
arg_group.add_argument("--records-uuids-file",
                       help="file path containing list of iDigBio record uuids, one per line")
arg_group.add_argument("--mediarecords-uuids-file",
                       help="file path containing list of iDigBio mediarecord uuids, one per line")
args = argparser.parse_args()

MAX_RESULTS = max(0,(min(args.max, MAX_MAX_COUNT)))
SIZE = args.size

output_directory = args.output_dir

QUERY_TYPE = 'rq'

def read_query_file(query_filename):
    if os.path.isfile(query_filename):
        with open(query_filename, 'r') as queryfile:
            q = queryfile.read()
            return q
    else:
        print ("*** Error: query file could not be read or does not exist.")
        raise SystemExit

def get_query_from_uuids_list_file(uuids_file):
    uuids_from_file = []
    with open(uuids_file) as uf:
        for line in uf:
            uuids_from_file.append(line.strip())
    
    q = '{"uuid":'
    q += json.dumps(uuids_from_file)
    q += '}'
    return q

query = None

if args.query:
    # use the query as supplied on the command line
    query = args.query
if args.query_file:
    # use the query as supplied in a file
    query = read_query_file(args.query_file)
if args.records_uuids_file:
    # generate a query from a list of record uuids
    query = get_query_from_uuids_list_file(args.records_uuids_file)
if args.mediarecords_uuids_file:
    # generate a query from a list of mediarecord uuids
    query = get_query_from_uuids_list_file(args.mediarecords_uuids_file)
    QUERY_TYPE = 'mq'

# Verify that the provided query string is valid JSON
if query is None:
    print ("*** ERROR! Query source is empty or unusable.")
else:
    try:
        query_json = json.loads(query)
    except Exception as e:
        print ('*** FATAL ERROR parsing query string:')
        print (e)
        print ('*** Supplied query string:')
        print (query)
        raise SystemExit


# The following should work whether one has specified an existing directory name, created a new directory by name,
# or left the output_directory unspecified.
if output_directory is None:
    now_ms = str(time.time())
    output_directory = time.strftime("%Y%m%d%H%M%S") + "." + str(time.time()).rsplit('.')[ len(now_ms.rsplit('.')) - 1]
    try:
        os.makedirs(output_directory)
    except:
        print ("*** ERROR! Could not create directroy for output: '{0}'".format(os.path.abspath(output_directory)))
        raise SystemExit
else:
    if not os.path.exists(output_directory):
        try:
            os.makedirs(output_directory)              
        except:
            print ("*** ERROR! Could not create directroy for output: '{0}'".format(os.path.abspath(output_directory)))
            raise SystemExit



def get_media_with_naming (output_dir, media_url, uuid, size):
    """
Download a media file to a directory and name it based on the input parameters.

 'output_dir' controls where the download is placed.

 'media_url' is the url / link to the media that will be downloaded.

 'uuid' is used to uniquely identify the output filename.

 'SIZE' is the class of image derivative, useful in the output filename.

"""
    try:
        response = requests.get(media_url, stream=True)
        response.raise_for_status()
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print('*** HTTP ERROR: {0}'.format(e))
        return False

    ### iDigBio returns 200 OK and displays an SVG status image when a derivative
    ### is not present.  Check for "Content-Type: image/svg+xml" header to notice this condition.
    if response.headers['Content-Type'] == 'image/svg+xml':
        print("*** WARNING - No media at '{0}'".format(media_url))
        return False

    # Output filenames will be of the form: {mediarecord_uuid}_{SIZE}.jpg
    local_filepath = os.path.join(output_dir,  uuid + '_' + SIZE + '.jpg')

    try:
        with open(local_filepath, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return True
    except:
        return False


if __name__ == '__main__':

    api = iDbApiJson()

    print ()
    print ("Using query:")
    print ()
    print (query)
    print ()
    print ("OPERATING PARAMETERS...")
    print ()
    print ("Maximum number of media to fetch: {:d}".format(MAX_RESULTS))
    print ("Media derivative size: {0}".format(SIZE))
    print ("Output directory: {0}".format(os.path.abspath(output_directory)))
    print ("Query Type: {0}".format(QUERY_TYPE))

    print ()
    print ("EXECUTING SEARCH QUERY...")
    print ()
    if QUERY_TYPE == 'mq':
        results = api.search_media(mq=query, limit=MAX_RESULTS)
    else:
        results = api.search_media(rq=query, limit=MAX_RESULTS)
    print ()
    print ("Search query produced {:d} results.".format(results['itemCount']))
    print ()
    if results['itemCount'] == 0 or MAX_RESULTS == 0:
        print ("Nothing to download. Exiting.")
        raise SystemExit
    if results['itemCount'] > MAX_RESULTS:
        print ("*** WARNING: search query produced more results than the designated maximum number of media to fetch.")
        print ("*** Use the -m or --max parameter to increase the maximum number of media to fetch.")
    print ()
    print("BEGINNING DOWNLOADS NOW...")
    print ()

    successes = 0
    failures = 0

    for each in results['items']:
        media_record_uuid = each['indexTerms']['uuid']
        media_url = 'https://api.idigbio.org/v2/media/' + media_record_uuid + '?size=' + SIZE
        print ("Downloading: '{0}'".format(media_url))
        if get_media_with_naming(output_directory, media_url, media_record_uuid, SIZE):
            successes += 1
        else:
            failures += 1

    print () 
    print ("DOWNLOADING FINISHED with {0:d} successes and {1:d} failures".format(successes, failures))
    print ()
    print ("Media downloads are in output directory: '{0}'".format(os.path.abspath(output_directory)))
