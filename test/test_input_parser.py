import unittest

from input_parser import Inputs


class TestInputParser(unittest.TestCase):
    def test_init_success_minimum(self):
        result = Inputs(["-r", "23", "-i", "pdb1.prmtop pdb1.inpcrd"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order1(self):
        result = Inputs(["-i", "pdb1.prmtop pdb1.inpcrd", "-r", "23"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order2(self):
        result = Inputs(["-i", "pdb1.prmtop pdb1.inpcrd", "-hy", "-r", "23", "-a"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order3(self):
        result = Inputs(["-a", "-hy", "-i", "pdb1.prmtop pdb1.inpcrd", "-r", "23"])
        self.assertIsInstance(result, object)

    def test_init_fail(self):
        self.assertRaises(TypeError, Inputs)

    def test_init_with_int(self):
        self.assertRaises(TypeError, Inputs, 1)

    def test_init_with_string(self):
        self.assertRaises(TypeError, Inputs, "string")

    def test_init_no_arguments(self):
        self.assertRaises(TypeError, Inputs, [])

    def test_init_to_few_arguments(self):
        self.assertRaises(TypeError, Inputs, ["1", "2", "3"])

    def test_init_to_many_arguments(self):
        self.assertRaises(TypeError, Inputs, ["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    # check mutation argument
    def test_mutation_flag_not_present(self):
        self.assertRaises(IOError, Inputs, ["", "23", "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_not_found(self):
        self.assertRaises(IOError, Inputs, ["r", "23", "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_followed_by_int(self):
        self.assertRaises(IOError, Inputs, ["-r", 1, "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_followed_by_non_int_castable_string(self):
        self.assertRaises(ValueError, Inputs, ["-r", "no_int", "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_followed_by_flag(self):
        self.assertRaises(ValueError, Inputs, ["-r", "-i", "pdb1.prmtop pdb1.inpcrd", "-ate"])

    def test_mutation_flag_followed_by_empty_string(self):
        self.assertRaises(ValueError, Inputs, ["-r", "", "-i", "pdb1.prmtop pdb1.inpcrd"])

if __name__ == '__main__':
    unittest.main()
