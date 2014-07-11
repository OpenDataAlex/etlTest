.. etlTest documentation master file, created by
   sphinx-quickstart on Wed Jul  2 09:00:21 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

etlTest
=======

 .. image:: https://travis-ci.org/OpenDataAlex/etlTest.png?branch=dev
    :target: https://travis-ci.org/OpenDataAlex/etlTest

 .. image:: https://coveralls.io/repos/OpenDataAlex/etlTest/badge.png?branch=dev
    :target: https://coveralls.io/r/OpenDataAlex/etlTest?branch=dev

 .. image:: https://api.coderwall.com/dbaalex/endorsecount.png
    :target: https://coderwall.com/dbaalex

etlTest is a testing framework for data integration code.

The home for etlTest is on `GitHub <https://github.com/OpenDataAlex/etlTest/>`_.

The goal of etlTest is to make creating and executing tests for data integration code as simple as possible.  We
 have achieved this through the use of `YAML <http://www.yaml.org/>`_ files to store test data sets and the actual
 tests.  Those files then get translated into `Python unittests <https://docs.python.org/2/library/unittest.html>`_
 and can be executed from the command line.  The results will show where there is more work to be done.

We have initially focused on unit tests, but we are planning on building out to cover other types of testing as well.

We are always looking for new feature requests, bugs, and other contributions!  To learn more on how to contribute,
please refer to our :doc:`Contributing <./contributing>` page.  To see what is on the roadmap,
please check out our `Issue Board <https://github.com/OpenDataAlex/etlTest/issues?state=open>`_.

.. toctree::
   :maxdepth: 2
   :numbered:

   Introduction <intro/intro.rst>
   Contributing <contributing.rst>
   setup.rst
   Configuration Settings <settings/settings.rst>
   Development Standards <standards/standards.rst>