Configuration Settings
======================
Below are the various configuration files used by etlTest.

.. toctree::
   :maxdepth: 2

   etlTest Settings <etltest>
   Data Connections <connections>
   User Properties <properties>
   Data Integration Tools <data_integration>

.. _settings-file-location:
Settings File Location
``````````````````````
The application settings file ( ``.etltest-settings.yml`` ) stays bundled with the application.

All other configuration files go into the data directory created by etlTest and is custom to the operating system that etlTest is installed on.
etlTest takes advantage of a Python package named ``appdirs`` to handle configuration of the directories.  At runtime, two directories are created:

* log - which handles logging for etlTest.
* application - which handles all other configuration files.

The location where these directories are set up is based on the ``app_name`` and ``app_author`` parameters.  On Linux, the directories would be:

* log - ~/.cache/etlTest/log/
* application - ~/.local/share/etlTest/

Please review the `appdirs documentation <https://pypi.python.org/pypi/appdirs/>`_ for more details.

Variable Replacement
````````````````````
Many of the values in these configuration files can be platform dependant.  It makes sense to create system variables
 so that the tests are more portable.  To use a system variable, enclose the name in ``${your_value_here}`` .  For
 instance, to use a system variable named ``$TOOL_HOME`` call it as part of a configuration value like so:
 ``${TOOL_HOME}/some/other/subdirectory`` . The variable will be replaced with it's proper value.

