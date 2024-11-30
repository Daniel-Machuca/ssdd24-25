"""Tests for StringSet class."""

import unittest

from remotetypes.customset import StringSet


STRING_VALUE = 'string value'
NON_STRING_VALUE = 0


class TestStringSet(unittest.TestCase):
    """Test cases for the StringSet class."""

    def test_instantiation(self):
        """Check initialisation is correct."""
        StringSet()
        StringSet([STRING_VALUE])
        StringSet(force_upper_case=True)

    def test_bad_instantiation(self):
        """Check initialisation with incorrect values."""
        with self.assertRaises(ValueError):
            StringSet([NON_STRING_VALUE])

    def test_add_string_value(self):
        """Check adding a str value to the StringSet."""
        a = StringSet()
        a.add(STRING_VALUE)

    def test_add_no_string_value(self):
        """Check adding a non-str value to the StringSet."""
        a = StringSet()
        with self.assertRaises(ValueError):
            a.add(NON_STRING_VALUE)
            
class MoreTestStringSet(unittest.TestCase):
    """created for the implementation of additional test cases"""
    def test_empty_initialization(self):
        a = StringSet()
        self.assertEqual(len(a), 0)
        
    def test_initialization_with_strings(self):
        a = StringSet(["a", "b", "c"])
        self.assertEqual(len(a), 3)
        self.assertIn("a", a)
        self.assertIn("b", a)
        self.assertIn("c", a)
        
    def test_initialization_with_duplicates(self):
        a = StringSet(["a", "b", "a"])
        self.assertEqual(len(a), 2)

    def test_initialization_with_non_strings(self):
        with self.assertRaises(ValueError):
            StringSet(["a", 123, "b"])
            
    def test_add_ok_string(self):
        a = StringSet()
        a.add("hello")
        self.assertIn("hello", a)
        
    def test_add_duplicate_string(self):
        a = StringSet(["hello"])
        a.add("hello")
        self.assertEqual(len(a), 1)
    
    def test_iteration(self):
        elements = ["one", "two", "three"]
        a = StringSet(elements)
        for item in a:
            self.assertIn(item, elements)