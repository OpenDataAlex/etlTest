.. _standards_test:

Test File Standards
===================

Here are the standards for building test files.

Available Test Types
--------------------
The types of tests available are a subset of the assertion types that are made available with Python's unittest framework.
To see more about the tests available in unittest, check out `their documentation <https://docs.python.org/2/library/unittest.html#assert-methods>`_ .

The list of available tests in etlTest is as follows:

=============  ====================  ============================================
etlTest Type   unittest Type         Test Description
=============  ====================  ============================================
Equal          assertEqual           Are given and expected equal?
NotEqual       assertNotEqual        Are given and expected no equal?
BooleanTrue    assertTrue            Is given true?
BooleanFalse   assertFalse           Is given false?
Is             assertIs              Are given and expected the same object?
IsNot          assertIsNot           Are given and expected not the same object?
IsNone         assertIsNone          Is given None?
IsNotNone      assertIsNotNone       Is given not None?
In             assertIn              Is given in expected?
NotIn          assertNotIn           Is given not in expected?
IsInstance     assertIsInstance      Is given an instance of expected?
IsNotInstance  assertIsNotInstance   Is given not an instance of expected?
=============  ====================  ============================================
