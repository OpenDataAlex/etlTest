__author__ = 'ameadows'

from etltest.utilities.settings_manager import SettingsManager

test_dir = SettingsManager.get_file_location() + '/samples/test/'


# class CodeGeneratorTest(unittest.TestCase):
#
#     def test_generate_single_test_file(self):
#         test_file = test_dir + 'dataMart/users.yml'
#
#         CodeGenerator(in_file=test_file)

#
#
# def test_generate_single_data_file():
#
# def test_generate_multiple_test_file():
#
# def test_generate_multiple_data_file():