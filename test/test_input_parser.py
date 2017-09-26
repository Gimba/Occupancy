import unittest
from input_parser import InputParser

class TestInputParser(unittest.TestCase):

    def test_init_success(self):
        result = InputParser(['test'])
        self.assertIsInstance(result, object)

    def test_init_fail(self):
        self.assertRaises(TypeError, InputParser)

    def test_init_not_list(self):
        self.assertRaises(TypeError, InputParser, 1)

if __name__ == '__main__':
    unittest.main()
