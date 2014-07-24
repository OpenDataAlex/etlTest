Data Connections
================
This section describes the setting file used for all data source and target connectivity.

Default Settings
----------------

Here is the default sample of the ``connections.cfg`` file.  This file can be found in the application settings directory, as described in :doc:`Settings <./settings>`

::

    [etlUnitTest]
    hostname:  127.0.0.1
    username:  root
    password:
    port:  3306
    type:  mysql
    dbname:  etlUnitTest


While this sample is written for MySQL/MariaDB, you can connect to any data source supported by SQLAlchemy.  The full
 list of SQLAlchemy supported data sources can be found in their official `documentation <http://docs.sqlalchemy
 .org/en/rel_0_9/core/engines.html#database_urls>`_ .

* ``[etlUnitTest]`` - The distinct name of the data source/target.  Can be any valid string, as long as it does not break configuration file standards.
*  ``hostname:`` - The host name or the ip address of the system that hosts the data source/target.
*  ``username:`` - The username that will be used to connect to the data source/target.
*  ``password:`` - The password for the user account connecting to the data source/target.
*  ``port:`` - The port on the host that allows for connections to the data source/target.
*  ``type:`` - The type of data source/target being connected to.  Must be compliant with the types of SQLAlchemy dialects.
*  ``dbname:`` - The name of the schema/database being connected to.  Does not have to match the name used to define
the data source/target.