Preparing Your Environment
==========================

When you run etlTest for the first time, it checks if it has everything it needs in place to generate and execute
tests.  Let's go ahead and run etlTest from the command line::

    etlTest

This will now create a data directory (for configuration files) and a log directory (for log files).  etlTest uses
the appdirs package creating the directories specific to your operating system.  Please refer to appdirs' docs (found
`here <https://pypi.python.org/pypi/appdirs/>`_ )for details about your environment.  To keep these docs universal,
here are the standard values we will be using:

 *  Data Directory - <your_data_path>/share/etlTest/
 *  Log Directory - <your_log_path>/etlTest/log/

Let's check out the data directory and see what got added there: ::

    cd <your_data_path>/share/etlTest/

There should be three configuration files there:

 *  connections.cfg - Used for data sources and targets
 *  properties.cfg - Used for tool configuration settings
 *  tools.yml - Used for data integration tool settings

Those files are covered in more detail in the :doc:`Configuration Settings <../settings/settings>` section.  Please
feel free to make modifications as necessary.  Any references to Locations or directory paths will be based on the
defaults found in the settings files.

If we also check out the log directory, we shouldn't actually see any files there.