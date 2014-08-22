Overview
````````
Below is an overview of what etlTest is and how it works.  It is important to understand some fundamental concepts:

* `Unit testing <http://en.wikipedia.org/wiki/Unit_testing>`_
* `Test driven development <http://en.wikipedia.org/wiki/Test-driven_development>`_
* `Continuous Integration <http://en.wikipedia.org/wiki/Continuous_integration>`_

Why etlTest?
````````````
Data integration tools do not have standard output in terms of code.  To make matters even more interesting,
many of them do not integrate with external version control systems (like `Subversion <http://subversion.apache
.org/>`_ or `Git <http://git-scm.com/>`_) let alone have a universal way to test code.  etlTest aims to change that
last part by providing a universal way to work with data integration tests.  This way,
regardless of the data source or data integration tool your tests will be able to be used with minimal effort to
convert them over when the stack you're working on changes.


How Does It Work?
`````````````````
Developing tests in etlTest is designed to be as simple as possible.  All that is required (other than installing
etlTest ;) ) is to generate a sample data file... ::

   //etltest/samples/data/etlUnitTest/users.yml
    1:
      user_id: 1
      first_name:  Bob
      last_name:  Richards
      birthday:  2000-01-04
      zipcode:  55555
    2:
      user_id: 2
      first_name:  Sarah
      last_name: Jenkins
      birthday:  2000-02-02
      zipcode:  12345
    ...

and a test file... ::

    //etltest/samples/test/dataMart/users_dim.yml
    DataMart\UsersDim:
       suites:
         - suite: dataMart
       processes:
         - tool:  PDI
           processes:
             - name:  data_mart/user_dim_jb.kjb
               type:  job
       dataset:
         - source:  etlUnitTest
           table:  users
           records:  [1, 2]
       tests:
         - name: testFirstNameLower
           desc:  Test for process that lower cases the first name field of a users table record.
           query:
             select: first_name
             from: user_dim
             where: user_id = 2
             source:  etlUnitTest
             result: {'first_name': 'sarah'}

See :doc:`sample data file standards <../standards/sample_data>` and :doc:`test file standards <../standards/test>` for
full template details.

Once your tests have been written, you can then have etlTest generate and execute your code. ::

    $ etlTest.py -f <path_to_your_test.yml> -o <path_to_your_output_dir> -g -e

Which will generate and run something similar to: ::

    //etltest/samples/output/DataMart/UsersDim.py
    #!/usr/bin/python
    #
    # This file was created by etlTest.
    #

    # These tests are also run as part of the following suites:
    #
    #    dataMart
    #
    # The following processes are executed for these tests:
    #
    #    PDI:
    #      data_mart/user_dim_jb.kjb

    import unittest
    import datetime
    from os import path

    from etltest.data_connector import DataConnector
    from etltest.process_executor import ProcessExecutor
    from etltest.utilities.settings_manager import SettingsManager


    class DataMartUsersDimTest(unittest.TestCase):

        def setUp(self):
              # Queries for loading test data.
                DataConnector("etlUnitTest").insert_data("users", [1, 2])

                PDI_settings = SettingsManager().get_tool("PDI")
                PDI_code_path = SettingsManager().system_variable_replace(PDI_settings["code_path"])
                ProcessExecutor("PDI").execute_process("job",
                path.join(PDI_code_path, "data_mart/user_dim_jb.kjb"))

        def tearDown(self):
           # Clean up testing environment.

            DataConnector("etlUnitTest").truncate_data("users")

        def testFirstNameLower(self):
            # Test for process that lower cases the first name field of a users table record.

            given_result = DataConnector("etlUnitTest").select_data("first_name",
                            "user_dim", "user_id = 2")

            expected_result = [{'first_name': 'sarah'}]

            self.assertEqual(given_result, expected_result)

    if __name__ == "__main__":
        unittest.main()

Notice that etlTest generates actual Python code so that you can leverage a full blown testing framework without
writing a single line of code!  We'll go over the various components of the test suites in :doc:`Test Components <../standards/test_components>`