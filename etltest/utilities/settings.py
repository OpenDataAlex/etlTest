"""
    This file reads the etltest-settings.yml file and loads application settings.

    Having a settings file in the users home directory overrides the one in the application directory.
"""

__author__ = 'coty'

import logging
import pprint

import os
import yaml

from .settings_manager import SettingsManager



# Begin CustomLogging
# this import adds the additional log levels I created

# create console handler and set level to info
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# set formatter
console.setFormatter(formatter)
# End CustomLogging

etltest_config = {}

settings_log = logging.getLogger(name="settings")
settings_log.setLevel(logging.DEBUG)
settings_log.addHandler(console)

pp = pprint.PrettyPrinter(indent=4)

settings_filename = os.path.join(SettingsManager.get_file_location(), '.etltest-settings.yml')

settings_fs_locs = ["{}/{}".format('', settings_filename), "".join(settings_filename)]

settings_loaded = False
for the_path in settings_fs_locs:
    settings_log.debug("Attempting to load {}".format(the_path))
    try:
        with open(the_path, 'r') as f:
            prop_list = yaml.load(f.read())
            for key, value in list(prop_list.items()):
                etltest_config[key] = value

            settings_log.debug("Settings loaded from {0}, {1}".format(the_path, etltest_config))
            settings_loaded = True
            break
    except (OSError, IOError) as e:
        settings_log.warn("{} {}".format(e.strerror, the_path))


if not settings_loaded:
    settings_log.warn("Could not find settings file in {}. Using defaults where present.".format(','.join(settings_fs_locs)))
    # For now there is nothing in the settings file that is required for operation. Removing the exit call.
    # exit()

# INFO = 20
# TESTING = 21
# DEBUG = 10
# TRACE = 5
try:
    console.level = etltest_config['logging_level']
except KeyError:
    etltest_config['logging_level'] = 20  # set default level to info
    console.level = etltest_config['logging_level']
