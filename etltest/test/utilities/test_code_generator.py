__author__ = 'ameadows'

import unittest

from etltest.utilities.settings_manager import SettingsManager
from etltest.code_generator import CodeGenerator

test_dir = SettingsManager.get_file_location() + '/etltest/samples/test/'
test_file = test_dir + 'dataMart/users_dim.yml'


class CodeGeneratorTest(unittest.TestCase):

    def test_generate_single_test_file(self):
        sample_file = SettingsManager.get_file_location() + '/etltest/samples/output/UserDim.py'

        given_result = CodeGenerator(in_file=test_file).generate_test()
        expected_result = file.read(sample_file)

        self.assertEqual(given_result, expected_result)

#
#
#
# def test_generate_multiple_test_file():