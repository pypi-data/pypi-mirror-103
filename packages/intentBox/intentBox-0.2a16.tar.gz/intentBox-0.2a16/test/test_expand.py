import unittest
from intentBox.utils import expand_parentheses


class TestIntentSyntax(unittest.TestCase):
    def test_one_of(self):
        self.assertEqual(
            expand_parentheses("(hey|hello) world"),
            [['h', 'e', 'y', ' ', 'w', 'o', 'r', 'l', 'd'],
             ['h', 'e', 'l', 'l', 'o', ' ', 'w', 'o', 'r', 'l', 'd']])
        self.assertEqual(
            expand_parentheses("(hey|hello) world", as_strings=True),
            ['hey world', 'hello world'])

    def test_optional(self):
        self.assertEqual(
            expand_parentheses("(hey|hello) [world]", as_strings=True),
            ['hey world', 'hey ', 'hello world', 'hello '])
