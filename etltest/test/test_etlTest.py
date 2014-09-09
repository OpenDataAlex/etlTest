# __author__ = 'ameadows'
#
# import unittest
# import os
# import subprocess
# import sys
#
# from etltest.utilities.settings_manager import SettingsManager
# from etltest import etlTest
#
#
# class CommandLineTestCase(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#         parser = etlTest.create_parser()
#         cls.parser = parser
#
#
# class etlTestTests(CommandLineTestCase):
#
#     def setUp(self):
#         SettingsManager().first_run_test()
#
#         self.in_file = SettingsManager().system_variable_replace("${"
#                                                                  "ETL_TEST_ROOT}/etltest/samples/test/dataMart/users_dim.yml")
#         self.in_dir = SettingsManager().system_variable_replace("${ETL_TEST_ROOT}/etltest/samples/test/dataMart/")
#
#         self.expected_output = SettingsManager().system_variable_replace("${"
#                                                                          "ETL_TEST_ROOT}/etltest/samples/output/DataMart/UsersDim.py")
#         self.process = os.path.join(SettingsManager().get_file_location(), "etltest/etlTest.py")
#
#     def test_in_file_generation_output(self):
#         file_param = "-f {0:s}".format(self.in_file)
#         output_file = os.path.join(SettingsManager().get_file_location(),
#                                        'etltest/samples/output/main/in_file_generation.txt')
#
#         given_result = subprocess.check_output(args=['python', self.process, file_param, "-g"])
#
#         with open(output_file, 'r') as f:
#             expected_result = f.read()
#
#         self.assertEqual(given_result, expected_result)
#
#     def test_in_dir_generation_output(self):
#         file_param = "-d {0:s}".format(self.in_dir)
#         output_file = os.path.join(SettingsManager().get_file_location(),
#                                    'etltest/samples/output/main/in_dir_generation.txt')
#
#         given_result = subprocess.check_output(args=['python', self.process, file_param, "-g"])
#
#         with open(output_file, 'r') as f:
#             expected_result = f.read()
#
#         self.assertEqual(given_result, expected_result)
#
#     def test_in_file_custom_output_generation_output(self):
#         file_param = "-f {0:s}".format(self.in_file)
#         output_file = os.path.join(SettingsManager().get_file_location(),
#                                        'etltest/samples/output/main/in_file_generation.txt')
#
#         given_result = subprocess.check_output(args=['python', self.process, file_param, "-g"])
#
#         with open(output_file, 'r') as f:
#             expected_result = f.read()
#
#         self.assertEqual(given_result, expected_result)
#
#     def test_parser_no_options(self):
#         # Test the results if there are no options given.
#         # Should return the help listing.
#         given_result = subprocess.check_output(args=['python', self.process])
#         output_file = os.path.join(SettingsManager().get_file_location(), 'etltest/samples/output/main/no_args.txt')
#
#         with open(output_file, 'r') as f:
#             expected_result = f.read()
#
#         self.assertEqual(given_result, expected_result)
#
#     def test_parser_in_file_in_dir_exclusivity(self):
#         #Test if in_file and in_dir are mutually exclusive.
#         file_param = "-f {0:s}".format(self.in_file)
#         dir_param = "-d {0:s}".format(self.in_dir)
#
#         with self.assertRaises(subprocess.CalledProcessError):
#             subprocess.check_output(args=['python', self.process, file_param, dir_param, "-g"])
#
#     def test_parser_no_args(self):
#         #Test if no args returns help options.
#         subprocess.check_output(args=['python', self.process], stderr=subprocess.STDOUT)
#
#     def test_parser_in_file_generation(self):
#         #Test if in_file generation exits appropriately.
#         subprocess.check_output(args=['python', self.process, '-f', self.in_file, '-g'])
#
#     def test_parser_in_dir_generation(self):
#         #Test if in_dir generation exits appropriately.
#         subprocess.check_output(args=['python', self.process, '-d', self.in_dir, '-g'])
#
#     def test_parser_in_file_custom_output_generation(self):
#         #Test if custom output generation exits appropriately.
#         output_loc = SettingsManager().find_setting('Locations', 'output')
#         subprocess.check_output(args=['python', self.process, '-f', self.in_file, '-g', '-o', str(output_loc)])
#
#     def test_parser_test_execution(self):
#         subprocess.check_output(args=['python', self.process, '-e'])
