Writing Your First Test
=======================

Now that your environment is set up, it's time to write some tests!  Before we do,
let's take a look at our sample data integration code - user_dim_load_tr.ktr:

 .. image:: ../images/user_dim_load_tr.png

In this transformation, we have a Table Input that is pulling data from our users table (created as part of the
:doc:`Sample Database Script <etlunittest_build_script>` ), uses a String operations step to lower case the
first_name field, and then insert the data using an Insert/Update step into the user_dim table.

What to test for?
-----------------

So there are many different things that can be tested here:

* How many records do we have in the source?  How many are in the target?
* Does the data integration code actually lower case the first_name field?
* Does the data integration code inadvertently modify other data than the first_name field?

Take a few minutes as see if there are other things that could be tested to add to the list.  Okay,
got a good list?  Awesome!  Tests will usually fall within one of three categories:

* Expected results
*