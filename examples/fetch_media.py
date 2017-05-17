from __future__ import print_function
try:
    from idigbio.json_client import iDbApiJson
    import requests
    import shutil
    import os
    import time
    import argparse
except ImportError as e:
    print ("IMPORT ERROR (This exception is likely caused by a missing module): '{0}'".format(e))
    raise SystemExit



help_blob = """
    Descriptive text goes here.

    Lorem ipsum dolor sit amet, consectetuer adipiscing elit, sed diam
    nonummy nibh euismod tincidunt ut laoreet dolore magna aliquam erat
    volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation
    ullamcorper suscipit lobortis nisl ut aliquip ex ea commodo consequat.

    Notes on the --output-dir / -o parameter:

        If the specified output directory does not exist, it will be created.
        Omitting this parameter will cause a new directory to be created
        under the current directory, named with a timestamp-like style.

"""

DEFAULT_SIZE = 'webview'
DEFAULT_MAX = 100
DEFAULT_OUTPUT_DIR = None

argparser = argparse.ArgumentParser(description=help_blob, formatter_class=argparse.RawDescriptionHelpFormatter)
argparser.add_argument("-m", "--max", help="Maximum number of records to be returned from search query.\nDefault: {0}".format(DEFAULT_MAX))
argparser.add_argument("-s", "--size", help="Size of derivative to download. Valid values are 'thumbnail', 'webview', and 'fullsize'.\nDefault: '{0}'".format(DEFAULT_SIZE))
argparser.add_argument("-o", "--output-dir", help="Directory path for downloaded media files. Default: a new directory will be created under current directory")
#argparser.add_argument("-b", "--bucket", required=True, help="Name of s3 bucket. Example: idigbio-images-prod")
#argparser.add_argument("-t", "--type", required=True, help="Type of media object, used to construct bucket names. Example: images")

arg_group_outfname = argparser.add_mutually_exclusive_group(required=False)
arg_group_outfname.add_argument("-g", help="Output filename based on record uuid.")  # should be default
arg_group_outfname.add_argument("-j", help="Output filename based on mediarecord uuid.")


arg_group = argparser.add_mutually_exclusive_group(required=True)
arg_group.add_argument("-q", "--query", help="query in iDigBio query format")
arg_group.add_argument("--query-file", help="file path containing query string in iDigBio Query Format")
arg_group.add_argument("--records-uuids-file", help="file path containing list of iDigBio record uuids, one per line")
arg_group.add_argument("--mediarecords-uuids-file", help="file path containing list of iDigBio mediarecord uuids, specified one per line")

args = argparser.parse_args()


raise SystemExit

## here parse the parameters



################

# Edit the 'query' variable to change the search query. The query is used to filter
# specimen records, the script downloads associated media.

# See iDigBio Query Format for help on query syntax
#    https://github.com/idigbio/idigbio-search-api/wiki/Query-Format

query = {"scientificname": "elephantopus elatus", "hasImage": True}

# Edit the 'size' variable to change which variant of the media derivative to download.
# Valid sizes are 'thumbnail', 'webview', and 'fullsize'

size = 'webview'


# Edit the 'output_directory' variable to specific a full file path or directory for the 
# downloads. Leaving as-is will download to temporary directory under the current dir.

output_directory = None
#output_directory = '/path/to/place/for/media'

MAX_RESULTS = 1000

################

def get_media_with_naming (output_dir, media_url, uuid, size):
    """
Download a media file to a directory and name it based on the input parameters.

 'output_dir' controls where the download is placed.

 'media_url' is the url / link to the media that will be downloaded.

 'uuid' is used to uniquely identify the output filename.

 'size' is the class of image derivative, useful in the output filename.

"""
    try:
        response = requests.get(media_url, stream=True)
        response.raise_for_status()
        #            r.
    except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
        print('Error: ' + e)
        return False

    # Output filenames will be of the form: {record_uuid}_{size}.jpg
    local_filepath = os.path.join(output_dir,  uuid + '_' + size + '.jpg')

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
        media_url = 'https://api.idigbio.org/v2/media/' + media_record_uuid + '?size=' + size
        print ("Downloading: '{0}'".format(media_url))
        if get_media_with_naming(output_directory, media_url, specimen_record_uuid, size):
            successes += 1
        else:
            failures += 1
        
    print ("Finished downloads to output directory: '{0}' with '{1}' successes and '{2}' failures".format(output_directory, successes, failures))
