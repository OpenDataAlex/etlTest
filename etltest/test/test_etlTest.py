__author__ = 'ameadows'

import unittest
import subprocess32 as subprocess
import os
import sys

from etltest.utilities.settings_manager import SettingsManager
from etltest import etlTest


class etlTestTests(unittest.TestCase):

    def setUp(self):
        SettingsManager().first_run_test()
        self.process = os.path.join(SettingsManager().get_file_location(), "etltest/etlTest.py")
        self.in_file = SettingsManager().system_variable_replace("${"
                                                                 "ETL_TEST_ROOT}/etltest/samples/test/dataMart/users_dim.yml")
        self.in_dir = SettingsManager().system_variable_replace("${ETL_TEST_ROOT}/etltest/samples/test/dataMart/")



    def test_with_empty_args(self):
        given_result = subprocess.check_output(args=[self.process])
        output_file = os.path.join(SettingsManager().get_file_location(), 'etltest/samples/output/main/no_args.txt')

        with open(output_file, 'r') as f:
            expected_result = f.read()

        self.assertEqual(given_result, expected_result)

    def test_in_file_generation(self):
        file_param = "-f {0:s}".format(self.in_file)
        output_file = os.path.join(SettingsManager().get_file_location(),
                                       'etltest/samples/output/main/in_file_generation.txt')

        given_result = subprocess.check_output(args=[self.process, file_param, "-g"])

        with open(output_file, 'r') as f:
            expected_result = f.read()

        self.assertEqual(given_result, expected_result)

    def test_in_dir_generation(self):
        file_param = "-d {0:s}".format(self.in_dir)
        output_file = os.path.join(SettingsManager().get_file_location(),
                                   'etltest/samples/output/main/in_dir_generation.txt')

        given_result = subprocess.check_output(args=[self.process, file_param, "-g"])

        with open(output_file, 'r') as f:
            expected_result = f.read()

        self.assertEqual(given_result, expected_result)

    def test_in_file_in_dir_exclusivity(self):
        file_param = "-f {0:s}".format(self.in_file)
        dir_param = "-d {0:s}".format(self.in_dir)

        with self.assertRaises(subprocess.CalledProcessError) as raises:
            subprocess.check_output(args=[self.process, file_param, dir_param, "-g"])

    def test_in_file_custom_output_generation(self):
        file_param = "-f {0:s}".format(self.in_file)
        output_file = os.path.join(SettingsManager().get_file_location(),
                                       'etltest/samples/output/main/in_file_generation.txt')

        given_result = subprocess.check_output(args=[self.process, file_param, "-g"])

        with open(output_file, 'r') as f:
            expected_result = f.read()

        self.assertEqual(given_result, expected_result)

    def test_parser_no_options(self):
        # Test if optparser is being created.
        sys.argv = [""]
        given_result = etlTest.main(sys.argv)
        expected_result = None

        self.assertEqual(given_result, expected_result)

    def test_parser_in_file_in_dir_exclusivity(self):
        #Test if in_file and in_dir are mutually exclusive.
        sys.argv = ["-f file.yml".split(), "-d /this/dir/".split(), "-g"]
        given_result = etlTest.main(sys.argv)
        expected_result = None

        self.assertEqual(given_result, expected_result)