__author__ = 'ameadows'

import unittest
import os
from shutil import copyfile

from etltest.process_executor import ProcessExecutor
from etltest.utilities.settings_manager import SettingsManager

class ProcessExecutorTests(unittest.TestCase):

    def setUp(self):
        SettingsManager().first_run_test()
        self.executor = ProcessExecutor('PDI')
        self.process_job = SettingsManager().system_variable_replace('ETL_TEST_ROOT',
                                                                 '$ETL_TEST_ROOT/PycharmProjects/etlTest/etltest/samples/etl/data_mart/user_dim_jb.kjb')
        self.process_trans = SettingsManager().system_variable_replace('ETL_TEST_ROOT',
                                                                       '$ETL_TEST_ROOT/PycharmProjects/etlTest/etltest/samples/etl/data_mart/user_dim_load_tr.ktr')

        self.tool_path = SettingsManager().system_variable_replace('ETL_TEST_ROOT', '$ETL_TEST_ROOT/data-integration')

        shared_file = SettingsManager().system_variable_replace('ETL_TEST_ROOT',
                                                                '$ETL_TEST_ROOT/etltest/samples/etl/shared.xml')
        shared_file_target = SettingsManager().system_variable_replace('ETL_TEST_ROOT',
                                                                       '$ETL_TEST_ROOT/.kettle/shared.xml')

        copyfile(shared_file, shared_file_target)

    def test_sample_job_exists(self):
        given_result = os.path.isfile(self.process_job)
        expected_result = True

        self.assertEqual(given_result, expected_result)

    def test_sample_trans_exists(self):

    def test_process_executor_job(self):
        given_result = self.executor.execute_process('job', self.process_job)
        expected_result = 0

        self.assertEqual(given_result, expected_result)

    def test_process_executor_trans(self):
        given_result = self.executor.execute_process('trans', self.process_trans)
        expected_result = 0

        self.assertEqual(given_result, expected_result)