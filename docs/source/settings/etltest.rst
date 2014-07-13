etlTest Settings
================
This section describes the application-level configuration file and it's various options.  It is not recommended to make changes to this section.

Default Settings
````````````````
Here is the default ``.etltest-settings.yml`` file:
::

    app_name: etlTest
    logging_level: 20
    app_author:  etlTest
    settings_file:  properties.cfg
    connection_file: connections.cfg
    tools_file:  tools.yml

These are the settings used by etlTest when running.

*  ``app_name`` is the name of the application.  This should remain the default 'etlTest'.
*  ``logging_level`` is the level of logging desired while etlTest is running.  The default is '20', which is the numerical value for logging at the 'INFO' level.
    * 5  - TRACE
    * 21 - TESTING
    * Standard logging level for Python are defined in the official `docs <https://docs.python.org/2/library/logging.html>`_ .
*  ``app_author`` is the name of the application author group.  This should remain the default 'etlTest'.
*  ``settings_file`` is the name of the file used for user-defined settings.  The default is 'properties.cfg'.
*  ``connection_file`` is the name of the file used for data tool connections.  The default is 'connections.cfg'.
*  ``tools_file`` is the name of the file used for data integration tool configuration.  The default is 'tools.yml'.