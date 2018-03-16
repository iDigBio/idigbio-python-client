.. :changelog:

Release History
---------------

0.8.5 (2018-03-16)
++++++++++++++++++

**New**

- add debug command-line option

0.8.4 (2017-06-07)
++++++++++++++++++

**New**

- add full-featured example script fetch_media.py to download media from iDigBio
- add documentation for fetch_media

**Changes**

- remove fetch_media_based_on_query.py which is superceded by fetch_media.py

0.8.3.3 (2017-05-17)
++++++++++++++++++++

**New**

- add an example to examples directory to download media based on search query

**Changes**

- minor changes to documentation, unit tests
- remove hard-coded path to tmp directory

0.8.2 (2017-05-10)
++++++++++++++++++

**New**

- count_recordsets() function returns number of recordsets in iDigBio


0.8.1 (2016-08-29)
++++++++++++++++++

- Send etag with file on upload to verify correctness

0.6.1 (2016-04-08)
++++++++++++++++++

**Changes**

- Add media_type to upload functionality.

0.6.0 (2016-03-30)
++++++++++++++++++

**Changes**

- Make pandas an extra requirements, update docs

**New**

- Specify auth for api backend
- Upload image capability (requires auth)



0.5.0 (2016-02-24)
++++++++++++++++++

**Changes**

- Don't exclude ``data.*`` fields if requested specifically
- Fix ``stats`` and ``datehist`` api calls to respect parameters;
  param names changed to use python style and match server params.


0.4.3 (2016-02-23)
++++++++++++++++++

**Bugfixes**

- no results no longer errs in the pandas client.
- limit correctly limits to specified record, not next larger batch size

**Miscellaneous**

- Clarify targetted python versions
