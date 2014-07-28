Data Integration Tool Settings
==============================
This section describes the settings file used for Data Integration tool connectivity.

Default Settings
----------------
Here is the default sample for ``tools.yml``.  This file can be found in the application settings directory, as described in :doc:`Settings <./settings>`
::

    PDI:
      host_name:  localhost
      port:
      user_name:
      password:
      private_key: '~/.ssh/id_rsa'
      tool_path:  ${TOOL_PATH}
      code_path:  ${ETL_TEST_ROOT}/etltest/samples/etl/
      process_param:  "/file:"
      params:  "/level: Detailed"
      logging_filename_format:  ${name}_%Y-%m-%d
      script_types:
        - type: job
          script:  kitchen.sh
        - type: trans
          script:  pan.sh

While the sample is written for Pentaho Data Integration, it can be configured for any data integration tool that can be run from the command line.

* ``PDI:`` - The unique name of the tool.  Can be any string as long as it does not break YAML standards.
*   ``host_name:`` - The unique name or ip address of the host the tool lives on.
*   ``port:`` - The port used to ssh onto the host box.
*   ``user_name:`` - The name of the user account that is used to run data integration code.
*   ``password:`` - The password of the user account that is used to run data integration code.
*   ``private_key:`` - The private key to tunnel onto the box, if needed.
*   ``tool_path:`` - The install location of the data integration tool.
*   ``code_path:`` - The location of the data integration tool's code base.  This is where etlTest will look for executable code.
*   ``process_param:`` - Any custom parameters that have to be used to call the code.  In PDI's case, files are called with the ``/file:`` property.
*   ``params:`` - Any parameters that need to be tacked onto the back of the command.  In PDI's case, logging is handled by the ``/level:`` parameter.
*   ``logging_filename_format:`` - If storing of the process logs is desired, this is the format of the logging file name.
*   ``script_types:`` - Multiple script types are allowed in the event that there are different components to the data integration tool.

  * ``type:`` - The callable type of script.
  * ``script:`` - The script that handles the type of process.  This is located where the data integration tool is installed.

Sample Configurations
---------------------
Here are some sample configurations for various tools that have been used with etlTest:

* :ref:`contributing-new-tools`
* :ref:`pentaho-file`

.. _contributing-new-tools:

Contributing New Tool Configurations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Are you using etlTest with a tool not listed here?  Please consider contributing a sample tool setup!  Find out how on our `How to Contribute <../contributing>`_ page.


.. _pentaho-file:

Pentaho Data Integration (file-based)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
::

    PDI:
      tool_path:  ${TOOL_PATH}
      code_path:  ${ETL_TEST_ROOT}/etltest/samples/etl/
      process_param:  "/file:"
      params:  "/level: Detailed"
      logging_filename_format:  ${name}_%Y-%m-%d
      script_types:
        - type: job
          script:  kitchen.sh
        - type: trans
          script:  pan.sh

Special note:  This sample takes advantage of two system variables:

* TOOL_PATH - Where the tool is installed (~/data-integration).
* ETL_TEST_ROOT - Where etlTest is installed, since we used the test samples for this sample tool configuration.