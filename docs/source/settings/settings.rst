Configuration Settings
======================
Below are the various configuration files used by etlTest.

Variable Replacement
````````````````````
Many of the values in these configuration files can be platform dependant.  It makes sense to create system variables
 so that the tests are more portable.  To use a system variable, enclose the name in ``${your_value_here}`` .  For
 instance, to use a system variable named ``$TOOL_HOME`` call it as part of a configuration value like so:
 ``${TOOL_HOME}/some/other/subdirectory`` . The variable will be replaced with it's proper value.

.. toctree::
   :maxdepth: 2

   etlTest Settings <etltest>
   Data Connections <connections>
   User Properties <properties>
   Data Integration Tools <data_integration>