import unittest

import cpptraj_helper as cpp
from input import Input


class Tests(unittest.TestCase):
    ## tests for input.py
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

    def test_init_success_input_list_frames_selected(self):
        result = Input(
            ["-a", "-hy", "-i", "pdb1.prmtop pdb1.inpcrd pdb2.prmtop pdb2.nc 1 200 pdb3.prmtop pdb3.nc 1 1", "-r",
             "23"])
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
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", "pdb1.prmtop pdb1.inpcrd pdb1.prmtop"])

    def test_input_list_not_starting_with_topology(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", "pdb1.inpcrd pdb1.prmtop prod_1.nc pdb1.prmtop"])

    def test_input_list_topology_not_followed_by_trajectory(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", "pdb1.prmtop 1 2 pdb1.inpcrd prod_1.nc pdb1.prmtop"])

    def test_input_list_trajectory_not_followed_by_topology(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", "pdb1.prmtop pdb1.nc prod_1.nc pdb2.prmtop"])

    def test_input_list_trajectory_not_followed_by_int_castable(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", "pdb1.prmtop pdb1.nc last last pdb1.prmtop prod_1.out"])

    ## tests for cpptraj_helper.py
    def test_specified_frames_exeeding_trajectory_frames(self):
        self.assertRaises(IOError, cpp.get_occupancy_of_atoms("input_files/F2196A.prmtop", "input_files/F2196A.inpcrd",
                                                              "1", "100", ["47@C", "24@CG2"], 1, 1))

if __name__ == '__main__':
    unittest.main()
