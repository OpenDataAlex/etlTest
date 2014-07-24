etlTest User Properties Settings
================================
This section describes the settings file used for the user's environment settings.

Default Settings
----------------
Here is the default sample for ``properties.cfg``.  This file can be found in the application settings directory,
as described in :doc:`Settings <./settings>`
::

    [Locations]
    tests: ${ETL_TEST_ROOT}/Documents/etlTest/tests
    data: ${ETL_TEST_ROOT}/Documents/etlTest/data
    output: ${ETL_TEST_ROOT}/Documents/etlTest/output
    [Results]
    Verbose: True
    FailureRate: 10
    ReportType: Normal

While the sample is written with example paths, any valid directory path can be used.  If the directory does not
exist, it will be created.

* ``[Locations]`` - This section of the properties configuration file contains locations for the various inputs and outputs of etlTest.
*    ``tests:``  - The location where the YAML test files are stored.
*    ``data:``  - The location where the YAML data files are stored.
*    ``output:`` - The location where the generated test scripts are created.
*  ``[Results]`` - This section is currently not in use.  The intent is to create user/environment based parameters
for how tests are run and the results shown.  The parameters underneath are just examples and are ignored by etlTest.
