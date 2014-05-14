__author__ = 'ameadows'

import unittest

from etltest.utilities.settings_manager import SettingsManager
from etltest.utilities.settings import etltest_config, console
from etltest.utilities.yaml_validate import YAMLValidate

validation_templates = SettingsManager.get_file_location() + "/templates/yaml"


class YamlValidateTest(unittest.TestCase):

    #def test_single_test_file_validate(self):


    #def test_multiple_test_file_validate(self):


    #def test_single_data_file_validate(self):


    #def test_multiple_data_file_validate(self):