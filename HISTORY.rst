.. :changelog:

Release History
---------------

0.6.1 (2016-04-08)
++++++++++++++++++

** Changes **

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
