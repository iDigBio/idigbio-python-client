from __future__ import print_function
try:
    from idigbio.json_client import iDbApiJson
    import requests
    import argparse
except ImportError as e:
    print ("IMPORT ERROR (This exception is likely caused by a missing module): '{0}'".format(e))
    raise SystemExit

help_blob = """

    This script will print information about recordsets and their indexed pubdate, contacts.

    Input list of recordset uuids is specified by putting them in a file and using --uuids-file option.

"""

argparser = argparse.ArgumentParser(description=help_blob, formatter_class=argparse.RawDescriptionHelpFormatter)
argparser.add_argument("-d", "--debug", default=False, action='store_true',
                       help="enable debugging output")
arg_group = argparser.add_mutually_exclusive_group(required=True)
arg_group.add_argument("-u", "--uuid", 
                       help="single iDigBio recordset uuid to query")
arg_group.add_argument("--uuids-file",
                       help="file path containing list of iDigBio recordset uuids to query, one per line")
args = argparser.parse_args()

QUERY_TYPE = 'rq'

debug_flag = args.debug
if debug_flag:
    print ()
    print ("** DEBUGGING ENABLED **")
    print ()
    print ()
    modulenames = set(sys.modules)&set(globals())
    allmodules = [sys.modules[name] for name in modulenames]
    print ("Loaded modules...")
    for each_mod in allmodules:
        print (each_mod)
    print ()

def get_list_of_uuids_from_file(uuids_file):
    uuids_from_file = []
    with open(uuids_file) as uf:
        for line in uf:
            uuids_from_file.append(line.strip())
    return uuids_from_file


def check_archive_status(url):
    try:
        r = requests.head(url, timeout=5)
        r.raise_for_status()
        return r.reason
    except:
        return "NO_ARCHIVE_AVAILABLE"


def print_recordset_view_data(api,uuid):
    recordset_item_from_api = api.view("recordsets", uuid)
    the_important_data = [
        recordset_item_from_api["uuid"],
        recordset_item_from_api["indexTerms"]["indexData"]["update"],
        recordset_item_from_api["indexTerms"]["name"],
        recordset_item_from_api["indexTerms"]["indexData"]["link"],
        # Does not yet include contacts or other data.
        # recordset_item_from_api[""],
        check_archive_status(recordset_item_from_api["indexTerms"]["indexData"]["link"])
        ]
    line = "\t".join(the_important_data)
    print(line.encode("utf-8"))
    

if args.uuids_file:
    uuid_list = get_list_of_uuids_from_file(args.uuids_file)
else:
    uuid_list = [args.uuid]

if __name__ == '__main__':

    api = iDbApiJson()

    print ()
    for each in uuid_list:
        print_recordset_view_data(api,each)


    print ()
    print ("***END***")
