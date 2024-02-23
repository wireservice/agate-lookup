0.3.3 - February 23, 2024
-------------------------

* Add Python 3.12 support.
* Drop Python 3.7 support (end-of-life was June 27, 2023).

0.3.2 - June 13, 2023
---------------------

* Use ``yaml.safe_load``.

0.3.1 - December 19, 2016
-------------------------

* Add missing module.

0.3.0 - December 19, 2016
-------------------------

* Remove monkeypatching pattern.
* Upgrade required agate to ``1.5.0``.

0.2.1 - March 9, 2016
---------------------

* Reorganize docs.
* Add caching to docs.
* Reversed order of source and table keys in lookup method.

0.2.0 - March 8, 2016
---------------------

* Update to latest `lookup` metadata format.
* Implement local caching for offline usage. (#14)
* Remove options to :class:`Source` for generating custom file paths.

0.1.1 - March 8, 2016
---------------------

* Added CPI calculation example to docs.
* Improvements to error handling.
* Fetched lookup tables now automatically have row names assigned.
* :meth:`TableLookup.from_table` class method implemented.

0.1.0 - February 28, 2016
-------------------------

* Initial version.
