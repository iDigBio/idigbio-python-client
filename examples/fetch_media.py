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
    returned by an iDigBio search query.

    The iDigBio Query Format is documented at

      https://github.com/idigbio/idigbio-search-api/wiki/Query-Format

    Notes on the --output-dir / -o parameter:

        If the specified output directory does not exist, it will be created.
        Omitting this parameter will cause a new directory to be created
        under the current directory, named in a timestamp-like style.


    Example, download media for scientific name Elephantopos elatus:

        $ python fetch_media.py  \\
            -q '{"scientificname": "elephantopus elatus"}'

    The defaults of this script will create a subdirectory under the current
    directory with the images inside named in a timestamp-like style.

### need an example here:
    $ ls -latr 201705171XXXXXX | head -n3

"""

SIZES = ["thumbnail", "webview", "fullsize"]
DEFAULT_SIZE = "webview"
DEFAULT_MAX_COUNT = 100
MAX_MAX_COUNT = 5000
DEFAULT_OUTPUT_DIR = None
#RECORD_TYPES = ["record", "mediarecord"]
#DEFAULT_UUID_FILENAME_TYPE = "mediarecord"

argparser = argparse.ArgumentParser(description=help_blob, formatter_class=argparse.RawDescriptionHelpFormatter)
argparser.add_argument("-m", "--max", type=int, default=DEFAULT_MAX_COUNT,
                       help="Maximum number of records to be returned from search query. Default: {0}".format(DEFAULT_MAX_COUNT))
argparser.add_argument("-s", "--size", choices=SIZES, default=DEFAULT_SIZE, 
                       help="Size of derivative to download. Default: '{0}'".format(DEFAULT_SIZE))
argparser.add_argument("-o", "--output-dir", default=DEFAULT_OUTPUT_DIR, 
                       help="Directory path for downloaded media files. Default: a new directory will be created under current directory")
#argparser.add_argument("-f", "--output-filename-format", choices=RECORD_TYPES, default=DEFAULT_UUID_FILENAME_TYPE, 
#                       help="Type of iDigBio identifier to use in the output filename. Default: '{0}'".format(DEFAULT_UUID_FILENAME_TYPE))
arg_group = argparser.add_mutually_exclusive_group(required=True)
arg_group.add_argument("-q", "--query", 
                       help="query in iDigBio Query Format.")
arg_group.add_argument("--query-file",
                       help="file path containing query string in iDigBio Query Format")
arg_group.add_argument("--records-uuids-file",
                       help="file path containing list of iDigBio record uuids, one per line")
arg_group.add_argument("--mediarecords-uuids-file",
                       help="file path containing list of iDigBio mediarecord uuids, specified one per line")
args = argparser.parse_args()

MAX_RESULTS = args.max
SIZE = args.size

output_directory = args.output_dir
#output_filename_format = args.output_filename_format


def read_query_file(inputfilename):
    return '{"genus":"acer"}'


if args.query:
    # use the query as supplied on the command line
    query = args.query
if args.query_file:
    query = read_query_file(args.query_file)
if args.records_uuids_file:
    #print (args.records-uuids-file)
    query = args.records_uuids_file
if args.mediarecords_uuids_file:
    query = args.mediarecords_uuids_file


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

print (query)
print (query_json)
print (MAX_RESULTS)
print (SIZE)
print (output_directory)

raise SystemExit

## here parse the parameters




################

# Edit the 'query' variable to change the search query. The query is used to filter
# specimen records, the script downloads associated media.

# See iDigBio Query Format for help on query syntax
#    https://github.com/idigbio/idigbio-search-api/wiki/Query-Format

query = {"scientificname": "elephantopus elatus"}


################

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
        #            r.
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print('Error: ' + e)
        return False

    # Output filenames will be of the form: {record_uuid}_{SIZE}.jpg
    local_filepath = os.path.join(output_dir,  uuid + '_' + SIZE + '.jpg')

    try:
        with open(local_filepath, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        return True
    except:
        return False


if __name__ == '__main__':

    api = iDbApiJson()

    print ("Begin!")
    print ("MAX_RESULTS is set to: '{0}'".format(MAX_RESULTS))
    print ("Executing search query: {0}".format(query))
    results = api.search_media(rq=query, limit=MAX_RESULTS)
    print ("Search Query produced '{0}' results.".format(results['itemCount']))

    # The following should work whether one has specified an existing directory name, created a new directory by name,
    # or left the output_directory unspecified.
    if output_directory is None:
        now_ms = str(time.time())
        output_directory = time.strftime("%Y%m%d%H%M%S") + "." + str(time.time()).rsplit('.')[ len(now_ms.rsplit('.')) - 1]
        try:
            os.makedirs(output_directory)
        except:
            print ("ERROR! Could not create directroy for output: '{0}'".format(os.path.abspath(output_directory)))
            raise SystemExit
    else:
        if not os.path.exists(output_directory):
            try:
                os.makedirs(output_directory)              
            except:
                print ("ERROR! Could not create directroy for output: '{0}'".format(os.path.abspath(output_directory)))
                raise SystemExit
    
    print ("Using Output Directory: '{0}'".format(os.path.abspath(output_directory)))

    successes = 0
    failures = 0

    print ("Starting downloads...")
    for each in results['items']:
        # Note that this will only get the first specimen uuid that is related to the media,
        # it will not download multiple copies of the media.
        specimen_record_uuid = each['indexTerms']['records'][0]
        media_record_uuid = each['indexTerms']['uuid']
        media_url = 'https://api.idigbio.org/v2/media/' + media_record_uuid + '?size=' + SIZE
        print ("Downloading: '{0}'".format(media_url))
        if get_media_with_naming(output_directory, media_url, specimen_record_uuid, SIZE):
            successes += 1
        else:
            failures += 1
        
    print ("Finished downloads to output directory: '{0}' with '{1}' successes and '{2}' failures".format(output_directory, successes, failures))
