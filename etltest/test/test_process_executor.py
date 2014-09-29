"""
These are the tests for the Process Executor.
"""
__author__ = 'ameadows'

import unittest
import os
from shutil import copyfile

from etltest.process_executor import ProcessExecutor
from etltest.utilities.settings_manager import SettingsManager


class ProcessExecutorTests(unittest.TestCase):
    """
    We test the Process Executor by setting up our environment with the first run test and set up specific locations to
    ensure that they exist.  We then can run our tests.
    """
    def setUp(self):
        SettingsManager().first_run_test()
        self.executor = ProcessExecutor('PDI')
        self.process_job = SettingsManager().system_variable_replace('${ETL_TEST_ROOT}/etltest/'
                                                                     'samples/etl/data_mart/user_dim_jb.kjb')
        self.process_trans = SettingsManager().system_variable_replace('${ETL_TEST_ROOT}/etltest/'
                                                                       'samples/etl/data_mart/user_dim_load_tr.ktr')

        shared_file = SettingsManager().system_variable_replace('${ETL_TEST_ROOT}/etltest/samples/etl/shared.xml')

        kettle_settings = SettingsManager().system_variable_replace('${ETL_TEST_ROOT}/.kettle')

        if os.path.isdir(kettle_settings) is False:
            os.mkdir(kettle_settings)

        shared_file_target = SettingsManager().system_variable_replace('${ETL_TEST_ROOT}/.kettle/shared.xml')
        if os.path.isfile(shared_file_target) is False:
            copyfile(shared_file, shared_file_target)

        self.mysql_driver = SettingsManager().system_variable_replace('${TOOL_PATH}/lib/'
                                                                      'mysql-connector-java-5.1.31-bin.jar')

    def test_sample_job_exists(self):
        """
        We need to verify that the sample job exists that is to be run.  Mainly for troubleshooting.
        """
        given_result = os.path.isfile(self.process_job)
        expected_result = True

        self.assertEqual(given_result, expected_result)

    def test_sample_trans_exists(self):
        """
        Testing that the sample transformation also exists.  Mainly for troubleshooting.
        """
        given_result = os.path.isfile(self.process_trans)
        expected_result = True

        self.assertEqual(given_result, expected_result)

    def test_mysql_driver_exists(self):
        """
        Testing that the MySQL JDBC driver exists.  Mainly for troubleshooting.
        """
        given_result = os.path.isfile(self.mysql_driver)
        expected_result = True

        self.assertEqual(given_result, expected_result)

    def test_process_executor_job(self):
        """
        Testing that the process executor is able to pick up the job settings and run the sample job.
        """
        given_result = self.executor.execute_process('job', self.process_job)
        expected_result = 0

        self.assertEqual(given_result, expected_result)

    def test_process_executor_trans(self):
        """
        Testing that the process executor is able to pick up the transformation settings and run the sample
        transformation.
        """
        given_result = self.executor.execute_process('trans', self.process_trans)
        expected_result = 0

        self.assertEqual(given_result, expected_result)

    # def test_process_remote_execution_no_key(self):
    #
    # def test_process_remote_execution_key(self):