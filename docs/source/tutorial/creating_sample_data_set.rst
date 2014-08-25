Creating A Sample Data Set
==========================

Now that we have written our three tests, it's time to create a data set so that we can accurately test them.
Remember, we have three tests that will require data:

*  Does first name get lower cased?
*  Does an upper case first name not return as upper case in the target table?
*  Does the birthday field get impacted by the data integration code?

First, let's create a new folder in our data directory (default is ``${ETL_TEST_ROOT}/Documents/etlTest/data``).::

    cd ${ETL_TEST_ROOT}/Documents/etlTest/data
    mkdir etlUnitTest

We created the ``etlUnitTest`` directory because that is the source where the data set we're about to create lives.
Since the ``users`` table is the source for our data integration, we should create a new YAML file called users.yml .::

    touch etlUnitTest/users.yml
    vi etlUnitTest/users.yml

.. include:: yaml_details_stub.rst

Now let's actually build our data set.  Remember, we need a data set that will meet the requirements for our tests.
For our first record, let's include a standard, run of the mill users table record.::

    1:
    # Generic record from the users table.
      user_id: 1
      first_name:  Bob
      last_name:  Richards
      birthday:  2000-01-04
      zipcode:  55555
      is_active: 0

Notice, the record is identified uniquely with ``1`` and that all the fields for record one are indented two spaces
to indicate they are all together.  To give a value to a field, we just put a colon followed by a space and then the
value we need for it. i.e. ``column_name: column_value``.

The record we just created will work fine for our first test case, but what do we do for the next one?  We could copy
the record and change the first_name field to ``BOB``, but that could run the risk of test collision when our test
suites and data sets get larger.  Let's build a new record specific to this test: ::

    1:
    # Generic record from the users table.
      user_id: 1
      first_name:  Bob
      last_name:  Richards
      birthday:  2000-01-04
      zipcode:  55555
      is_active: 0
    2:
    # Record for first_name all upper case.
      user_id: 2
      first_name:  Sarah
      last_name: Jenkins
      birthday:  2000-02-02
      zipcode:  12345
      is_active: 1

We indicate a new record in the YAML file by removing any indentation in the next line after the zipcode column for
record one and give our record another unique identifier (this time ``2``).  We use the same column names as before,
but we now have a record that has an entirely upper-cased first_name field.

For the third test case, we could create a new record or we can utilize one of the existing records to test if the
birthday field is manipulated.  For the birthday test, we will use record one.  Now we can work on building our tests.