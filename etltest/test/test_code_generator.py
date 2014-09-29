"""
These are the tests for the Code Generator Module.
"""
__author__ = 'ameadows'

import unittest
import os

from etltest.utilities.settings_manager import SettingsManager
from etltest.code_generator import CodeGenerator


class CodeGeneratorTest(unittest.TestCase):
    """
        We start our tests by ensuring the environment is set up correctly using the first_run_rest.  We then define
        an output directory, and the location of our test files.
    """
    def setUp(self):
        SettingsManager().first_run_test()
        self.out_dir = SettingsManager().find_setting('Locations', 'output')
        self.main_path = SettingsManager().get_file_location()
        self.test_dir = self.main_path + '/etltest/samples/test/'
        self.test_file = self.test_dir + '/dataMart/users_dim.yml'


    def test_generate_single_test_file(self):
        """
        Testing that we can generate a good PyUnit test file from a single yaml test file.
        """
        CodeGenerator(in_file=self.test_file).generate_test('unit')
        # Testing the in_file option of code_generator
        sample_file = os.path.join(self.main_path, 'etltest/samples/output/DataMart/UsersDim.py')
        output_file = os.path.join(self.out_dir, 'DataMart/UsersDim.py')

        with open(output_file, 'r') as f:
            expected_result = f.read()

        with open(sample_file, 'r') as f:
            given_result = f.read()


        self.assertEqual(given_result, expected_result)

    def test_generate_multiple_test_file(self):
        """
        Testing that we can generate good PyUnit test files from a directory of yaml test files.
        """
        # Testing the in_dir option of code_generator.
        CodeGenerator(in_dir=self.test_dir).generate_test('unit')
        sample_dir = os.path.join(self.main_path, 'etltest/samples/output/DataMart/')
        output_dir = os.path.join(self.out_dir, 'DataMart')

        given_result = len([name for name in os.listdir(output_dir) if os.path.isfile(name)])
        expected_result = len([name for name in os.listdir(sample_dir) if os.path.isfile(name)])

        self.assertEqual(given_result, expected_result)

    def test_get_template_unit(self):
        """
        Testing the get_template method to return the value for unit tests.
        """
        given_result = CodeGenerator().get_template('unit')
        expected_result = 'test.jinja2'

        self.assertEqual(given_result, expected_result)

    def test_get_template_suite(self):
        """
        Testing the get_template method to return the value for suite tests.
        """
        given_result = CodeGenerator().get_template('suite')
        expected_result = 'suite.jinja2'

        self.assertEqual(given_result, expected_result)

    def test_get_template_default(self):
        """
        Testing the get_template method to return the default value if no test types are passed.
        """
        given_result = CodeGenerator().get_template()
        expected_result = 'test.jinja2'

        self.assertEqual(given_result, expected_result)

    # def test_generate_code_no_option(self):
    #     CodeGenerator(in_dir=self.test_dir).generate_test('unit')
    #     # Testing if neither in_file or in_dir are provided.
    #     sample_dir = os.path.join(self.main_path, 'etltest/samples/output/DataMart/')
    #     output_dir = os.path.join(self.out_dir, 'DataMart')
    #
    #     given_result = len([name for name in os.listdir(output_dir) if os.path.isfile(name)])
    #     expected_result = len([name for name in os.listdir(sample_dir) if os.path.isfile(name)])
    #
    #     self.assertEqual(given_result, expected_result)