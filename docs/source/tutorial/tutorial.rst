The etlTest Tutorial
====================

This is a walk through is intended to assist new users in writing, generating,
and executing tests for data integration code.  We have tried to keep topics specific to each function of the tool in
their own section.  This guide assumes that etlTest has been installed on the environment that the tutorial is being
performed on.  Please refer to the installation instructions found on the :doc:`Setup <../setup>` page if etlTest has
not been installed.

For the purposes of this tutorial, we will assume you have access to the following:

* Local MySQL instance (software is available from `MySQL <http://dev.mysql.com/downloads/mysql/>`_ )
* Local Pentaho Data Integration instance (software is available from `SourceForge <http://sourceforge.net/projects/pentaho/files/Data%20Integration/>`_ )
* Database built using the ``etlUnitTest_build.sql`` script, found in the scripts directory of where etlTest is
  installed, or from the :doc:`Sample Database Script <etlunittest_build_script>` page
* Sample data integration code, found in the samples/etl directory of where etlTest is installed (user_dim_jb.kjb and
  user_dim_load_tr.ktr)

In addition, while you are free to make any modifications to directory locations, we will be using the defaults found
in the sample settings files.

.. toctree::
   :maxdepth: 2

   Preparing Your Environment <preparing_environment>
   Writing Your First Test <writing_first_test>
   Creating A Sample Data set <creating_sample_data_set>
   Configuring Your Data Integration Tool <configuring_data_integration_tool>
   Generating Test Code <generating_test_code>
   Executing Your Tests <executing_tests>
   Sample Database Script <etlunittest_build_script>
