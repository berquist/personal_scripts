#!/usr/bin/env python

# -*- coding: utf-8 -*-
import unittest

def f(x):
    """
    A function to test.  You can also test functions inside classes.
    """
    return x + 1

# name of the testing class does not matter
class Test_f(unittest.TestCase):
    """
    1.  Make a class derived from unittest.TestCase
    2.  Define functions that start with 'test_'
    3.  Have those functions call methods of unittest.TestCase
    4.  There are many useful testing methods in unittest.TestCase
    """
    # function must start with 'test_'
    def test_f_1(self):
        """
        An example that should work.
        """
        self.assertEquals(f(1), 2)

    # function must start with 'test_'
    def test_f_2(self):
        """
        An example that will fail.
        """
        self.assertEquals(f(2), 1)

if __name__ == '__main__':
    # call unittest.main() to automatically run tests found in this file
    unittest.main()
