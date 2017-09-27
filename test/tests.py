import unittest

from input import Input


class Tests(unittest.TestCase):
    def test_init_success_minimum(self):
        result = Input(["-r", "23", "-i", "pdb1.prmtop pdb1.inpcrd"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order1(self):
        result = Input(["-i", "pdb1.prmtop pdb1.inpcrd", "-r", "23"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order2(self):
        result = Input(["-i", "pdb1.prmtop pdb1.inpcrd", "-hy", "-r", "23", "-a"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order3(self):
        result = Input(["-a", "-hy", "-i", "pdb1.prmtop pdb1.inpcrd", "-r", "23", "-w"])
        self.assertIsInstance(result, object)

    def test_init_success_input_list(self):
        result = Input(["-a", "-hy", "-i", "pdb1.prmtop pdb1.inpcrd pdb2.prmtop pdb2.inpcrd", "-r", "23"])
        self.assertIsInstance(result, object)

    def test_init_fail(self):
        self.assertRaises(TypeError, Input)

    def test_init_with_int(self):
        self.assertRaises(TypeError, Input, 1)

    def test_init_with_string(self):
        self.assertRaises(TypeError, Input, "string")

    def test_init_no_arguments(self):
        self.assertRaises(TypeError, Input, [])

    def test_init_to_few_arguments(self):
        self.assertRaises(TypeError, Input, ["1", "2", "3"])

    def test_init_to_many_arguments(self):
        self.assertRaises(TypeError, Input, ["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    # tests for mutation argument
    def test_mutation_flag_not_present(self):
        self.assertRaises(IOError, Input, ["", "23", "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_not_found(self):
        self.assertRaises(IOError, Input, ["r", "23", "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_followed_by_int(self):
        self.assertRaises(IOError, Input, ["-r", 1, "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_followed_by_non_int_castable_string(self):
        self.assertRaises(ValueError, Input, ["-r", "no_int", "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_followed_by_negative_number(self):
        self.assertRaises(ValueError, Input, ["-r", "-1", "-i", "pdb1.prmtop pdb1.inpcrd"])

    def test_mutation_flag_followed_by_flag(self):
        self.assertRaises(ValueError, Input, ["-r", "-i", "pdb1.prmtop pdb1.inpcrd", "-ate"])

    def test_mutation_flag_followed_by_empty_string(self):
        self.assertRaises(ValueError, Input, ["-r", "", "-i", "pdb1.prmtop pdb1.inpcrd"])

    # tests for input list argument
    def test_input_flag_not_present(self):
        self.assertRaises(IOError, Input, ["-r", "23", "-a", "pdb1.prmtop pdb1.inpcrd"])

    def test_input_flag_followed_by_single_string(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", "pdb1.prmtop"])

    def test_input_flag_followed_by_empty_string(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", ""])

    # tests for input list
    def test_input_list_not_even_number(self):
        self.assertRaises(IOError, Input, ["-r", "23", "-i", "pdb1.prmtop pdb1.inpcrd pdb1.prmtop"])

    def test_input_list_not_starting_with_topology(self):
        self.assertRaises(IOError, Input, ["-r", "23", "-i", "pdb1.inpcrd pdb1.prmtop prod_1.nc pdb1.prmtop"])

    def test_input_list_not_every_second_topology(self):
        self.assertRaises(IOError, Input, ["-r", "23", "-i", "pdb1.prmtop pdb1.inpcrd prod_1.nc pdb1.prmtop"])

    def test_input_list_second_element_not_trajectory(self):
        self.assertRaises(IOError, Input, ["-r", "23", "-i", "pdb1.prmtop pdb1.out pdb1.prmtop prod_1.nc"])

    def test_input_list_not_every_second_trajectory(self):
        self.assertRaises(IOError, Input, ["-r", "23", "-i", "pdb1.prmtop pdb1.nc pdb1.prmtop prod_1.out"])


        ## test pdb class ##


if __name__ == '__main__':
    unittest.main()
