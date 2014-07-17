__author__ = 'ameadows'

import unittest
import os
import subprocess

from etltest.utilities.settings_manager import SettingsManager
from etltest import etlTest

class CommandLineTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        parser = etlTest.create_parser()
        cls.parser = parser

class etlTestTests(CommandLineTestCase):

    def setUp(self):

        self.in_file = SettingsManager().system_variable_replace("${"
                                                                 "ETL_TEST_ROOT}/etltest/samples/test/dataMart/users_dim.yml")
        self.in_dir = SettingsManager().system_variable_replace("${ETL_TEST_ROOT}/etltest/samples/test/dataMart/")

        self.expected_output = SettingsManager().system_variable_replace("${"
                                                                         "ETL_TEST_ROOT}/etltest/samples/output/DataMart/UsersDim.py")
        self.process = os.path.join(SettingsManager().get_file_location(), "etltest/etlTest.py")

    def test_in_file_generation(self):
        file_param = "-f {0:s}".format(self.in_file)
        output_file = os.path.join(SettingsManager().get_file_location(),
                                       'etltest/samples/output/main/in_file_generation.txt')

        given_result = subprocess.check_output(args=['python', self.process, file_param, "-g"])

        with open(output_file, 'r') as f:
            expected_result = f.read()

        self.assertEqual(given_result, expected_result)

    def test_in_dir_generation(self):
        file_param = "-d {0:s}".format(self.in_dir)
        output_file = os.path.join(SettingsManager().get_file_location(),
                                   'etltest/samples/output/main/in_dir_generation.txt')

        given_result = subprocess.check_output(args=['python', self.process, file_param, "-g"])

        with open(output_file, 'r') as f:
            expected_result = f.read()

        self.assertEqual(given_result, expected_result)

    def test_in_file_custom_output_generation(self):
        file_param = "-f {0:s}".format(self.in_file)
        output_file = os.path.join(SettingsManager().get_file_location(),
                                       'etltest/samples/output/main/in_file_generation.txt')

        given_result = subprocess.check_output(args=['python', self.process, file_param, "-g"])

        with open(output_file, 'r') as f:
            expected_result = f.read()

        self.assertEqual(given_result, expected_result)

    def test_parser_no_options(self):
        # Test the results if there are no options given.
        # Should return the help listing.
        given_result = subprocess.check_output(args=['python', self.process])
        output_file = os.path.join(SettingsManager().get_file_location(), 'etltest/samples/output/main/no_args.txt')

        with open(output_file, 'r') as f:
            expected_result = f.read()

        self.assertEqual(given_result, expected_result)


    def test_parser_in_file_in_dir_exclusivity(self):
        #Test if in_file and in_dir are mutually exclusive.
        file_param = "-f {0:s}".format(self.in_file)
        dir_param = "-d {0:s}".format(self.in_dir)

        with self.assertRaises(subprocess.CalledProcessError):
            subprocess.check_output(args=['python', self.process, file_param, dir_param, "-g"])

    def test_file_dir_exclusivity(self):
        #Test if in_file and in_dir are mutually exclusive.
        args = self.parser.parse_args(['-f', 'file.yml', '-d', '/not/real/dir/', '-g'])
        with self.assertRaises(SystemExit):
            etlTest.main(args)