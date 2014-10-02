Test Template Overview
======================
This template is used to build unit test sets.  This overview will break down the template file and describe the various sections.::



    {{ header }}
    # These tests are also run as part of the following suites:
    #
    {% for suite in tests.suites %}
    #    {{ suite.suite }}
    {% endfor %}
    #
    # The following processes are executed for these tests:
    #
    {% for proc in tests.processes %}
    #    {{ proc.tool }}:
      {% for p in proc.processes %}
    #      {{ p.name }}
      {% endfor %}
    {% endfor %}

This is the header section for our test files.  It describes which test suites it is a part of (either unit test suites or others) as well as any ETL processes and tools that are used.
::

    import unittest
    import datetime
    from os import path

    from etltest.data_connector import DataConnector
    from etltest.process_executor import ProcessExecutor
    from etltest.utilities.settings_manager import SettingsManager

These are all of the requirements for the tests - both external (from other packages) and internal (from etlTest).

::

    class {{ testGroup }}Test(unittest.TestCase):

Using the name of the testGroup (from the yaml test file) as part of the name of the test class.
::

    @classmethod
        def setUpClass(cls):
              # Queries for loading test data.
          {% for set in tests.dataset %}
                DataConnector("{{ set.source }}").insert_data("{{ set.table }}", {{ set.records }})
          {% endfor %}

          {% for tool in tests.processes %}
                {{ tool.tool }}_settings = SettingsManager().get_tool("{{ tool.tool }}")
                {{ tool.tool }}_code_path = SettingsManager().system_variable_replace({{ tool.tool }}_settings["code_path"])
          {% for job in tool.processes %}
                ProcessExecutor("{{ tool.tool }}").execute_process("{{ job.type }}",
                path.join({{ tool.tool }}_code_path, "{{ job.name }}"))
          {% endfor %}
          {% endfor %}

During the setup phase of the test the records that are used are inserted into the source database.  The ETL processes that are listed in the header are executed here.
This is only run once at the start of the run.
::

    @classmethod
    def tearDownClass(cls):
       # Clean up testing environment.

      {% for set in tests.dataset %}
        DataConnector("{{ set.source }}").truncate_data("{{ set.table }}")
      {% endfor %}
During the teardown phase of the test, the tables that had records inserted are truncated (this is a current limitation that we are trying to find a work around for).
The teardown phase is only run once at the end of the run.
::

    {% for test in tests.tests %}
        def {{ test.name }}(self):
            # {{ test.desc }}

            given_result = DataConnector("{{ test.query.source }}").select_data("{{ test.query.select }}",
                            "{{ test.query.from }}", "{{ test.query.where }}")
          {% if test.query.result is defined and test.query.result not in ('BooleanTrue', 'BooleanFalse', 'IsNone', 'IsNotNone')%}

            expected_result = [{{ test.query.result }}]
          {% endif %}

          {% if test.type == 'Equal' or test.type is not defined %}
            self.assertEqual(given_result, expected_result)
          {% elif test.type == 'NotEqual' %}
            self.assertNotEqual(given_result, expected_result)
          {% elif test.type == 'BooleanTrue' %}
            self.assertTrue(given_result)
          {% elif test.type == 'BooleanFalse' %}
            self.assertFalse(given_result)
          {% elif test.type == 'Is' %}
            self.assertIs(given_result, expected_result)
          {% elif test.type == 'IsNot' %}
            self.assertIsNot(given_result, expected_result)
          {% elif test.type == 'IsNone' %}
            self.assertIsNone(given_result)
          {% elif test.type == 'IsNotNone' %}
            self.assertIsNotNone(given_result)
          {% elif test.type == 'In' %}
            self.assertIn(given_result, expected_result)
          {% elif test.type == 'NotIn' %}
            self.assertNotIn(given_result, expected_result)
          {% elif test.type == 'IsInstance' %}
            self.assertIsInstance(given_result, expected_result)
          {% elif test.type == 'IsNotInstance' %}
            self.assertIsNotInstance(given_result, expected_result)
          {% else %}
            self.assertEqual(given_result, expected_result)
          {% endif %}

    {% endfor %}
This is the actual test being generated.  The test name is used for it's code equivalent.  The query used for the test is put in as the given result while the expected result
gets stored accordingly (if needed).  Depending on the type of test used will determine the type of assertion used (which is the if statement that checks the test type).
::

    if __name__ == "__main__":
        unittest.main()

This piece allows for the unit tests to be called based on the file name.