__author__ = 'ameadows'

import unittest
from etltest.process_executor import ProcessExecutor
from etltest.utilities.settings_manager import SettingsManager

class ProcessExecutorTests(unittest.TestCase):

    def setUp(self):
        SettingsManager().first_run_test()
        self.executor = ProcessExecutor('PDI')
        self.process_job = SettingsManager().system_variable_replace('ETL_TEST_ROOT',
                                                                 '$ETL_TEST_ROOT/samples/etl/data_mart/user_dim_jb.kjb')
        self.process_trans = SettingsManager().system_variable_replace('ETL_TEST_ROOT',
                                                                       '$ETL_TEST_ROOT/samples/etl/data_mart/user_dim_load_tr.ktr')

        self.tool_path = SettingsManager().system_variable_replace('ETL_TEST_ROOT', '$ETL_TEST_ROOT/data-integration')

    def test_process_executor(self):
        given_result = self.executor.execute_process('job', self.process_job)
        expected_result = 0

        self.assertEqual(given_result, expected_result)