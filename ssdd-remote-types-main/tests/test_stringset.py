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
