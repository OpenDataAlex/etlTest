__author__ = 'ameadows'

import unittest

import os

from etltest.utilities.settings_manager import SettingsManager
from etltest.code_generator import CodeGenerator


class CodeGeneratorTest(unittest.TestCase):

    def setUp(self):
        self.out_dir = SettingsManager().find_setting('Locations', 'tests')
        self.main_path = SettingsManager().get_file_location()
        self.test_dir = os.path.join(self.main_path, '/etltest/samples/test/')
        self.test_file = os.path.join(self.test_dir, 'dataMart/users_dim.yml')

    def test_generate_single_test_file(self):

        CodeGenerator(in_file=self.test_file).generate_test()
        sample_file = os.path.join(self.main_path, '/etltest/samples/output/DataMart/UserDim.py')
        output_file = os.path.join(self.out_dir, 'DataMart/UserDim.py')
        given_result = file.read(open(output_file, 'r'))

        expected_result = file.read(open(sample_file, 'r'))

        self.assertEqual(given_result, expected_result)

#
#
#
# def test_generate_multiple_test_file():