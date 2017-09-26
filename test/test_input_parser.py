import unittest
from input_parser import InputParser

class TestInputParser(unittest.TestCase):

    def test_init_success(self):
        result = InputParser(['test'])
        self.assertIsInstance(result, object)

    def test_init_fail(self):
        self.assertRaises(TypeError, InputParser)

    def test_init_with_int(self):
        self.assertRaises(TypeError, InputParser, 1)

    def test_init_with_string(self):
        self.assertRaises(TypeError, InputParser, "string")

if __name__ == '__main__':
    unittest.main()
