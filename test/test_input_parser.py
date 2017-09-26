import unittest
from input_parser import InputParser

class TestInputParser(unittest.TestCase):

    def test_init_success(self):
        result = InputParser(["1","2"])
        self.assertIsInstance(result, object)

    def test_init_fail(self):
        self.assertRaises(TypeError, InputParser)

    def test_init_with_int(self):
        self.assertRaises(TypeError, InputParser, 1)

    def test_init_with_string(self):
        self.assertRaises(TypeError, InputParser, "string")

    def test_init_to_few_arguments(self):
        self.assertRaises(TypeError, InputParser, [])

    def test_init_no_arguments(self):
        self.assertRaises(TypeError, InputParser, [])

    def test_init_to_few_arguments(self):
        self.assertRaises(TypeError, InputParser, ["1"])

    def test_init_to_many_arguments(self):
        self.assertRaises(TypeError, InputParser, ["1", "2", "3", "4", "5", "6"])


if __name__ == '__main__':
    unittest.main()
