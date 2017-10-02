import os as os
import unittest

import os_helper as myos
from input import Input


class Tests(unittest.TestCase):
    ## tests for input.py
    def test_init_success_minimum(self):
        result = Input(["-r", "23", "-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order1(self):
        result = Input(["-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd", "-r", "23"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order2(self):
        result = Input(["-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd", "-hy", "-r", "23", "-a"])
        self.assertIsInstance(result, object)

    def test_init_success_minimum_mixed_order3(self):
        result = Input(
            ["-a", "-hy", "-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd", "-r", "23", "-w"])
        self.assertIsInstance(result, object)

    def test_init_success_input_list(self):
        result = Input(["-a", "-hy", "-i",
                        "../input_files/model1.prmtop ../input_files/model1.inpcrd ../input_files/F2196A.prmtop ../input_files/F2196A.inpcrd",
                        "-r", "23"])
        self.assertIsInstance(result, object)

    def test_init_success_input_list_frames_selected(self):
        result = Input(
            ["-a", "-hy", "-i", "../input_files/F2196A.prmtop ../input_files/F2196A.inpcrd 1 1", "-r",
             "23"])
        self.assertIsInstance(result, object)

    def test_input_list_absolute_path(self):
        ip = Input(
            ["-a", "-hy", "-i",
             "/l_mnt/scratch/u/rm001/Occupancy/input_files/F2196A.prmtop /l_mnt/scratch/u/rm001/Occupancy/input_files/F2196A.inpcrd 1 1",
             "-r",
             "23"])
        myos.create_output_folder(ip.folder)
        myos.copy_to_folder(ip.input[0][0], ip.folder)
        ip.set_file_paths_to_output_folder()
        myos.change_to_folder(ip.folder)
        self.assertTrue(os.path.isfile(ip.input[0][0]))
        os.chdir("..")
        os.system("rm -rf " + ip.folder)

    def test_input_list_relative_path(self):
        ip = Input(
            ["-a", "-hy", "-i",
             "../input_files/F2196A.prmtop ../input_files/F2196A.inpcrd 1 1",
             "-r",
             "23"])
        myos.create_output_folder(ip.folder)
        myos.copy_to_folder(ip.input[0][0], ip.folder)
        ip.set_file_paths_to_output_folder()
        myos.change_to_folder(ip.folder)
        self.assertTrue(os.path.isfile(ip.input[0][0]))
        os.chdir("..")
        os.system("rm -rf " + ip.folder)

    def test_input_list_output_folder_specified(self):
        ip = Input(
            ["-a", "-hy", "-i",
             "../input_files/F2196A.prmtop ../input_files/F2196A.inpcrd 1 1",
             "-r",
             "23",
             "-f",
             "output"])
        myos.create_output_folder(ip.folder)
        self.assertTrue(os.path.isdir(ip.folder))
        os.removedirs(ip.folder)

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

    # tests for mutation argument
    def test_mutation_flag_not_present(self):
        self.assertRaises(IOError, Input, ["", "23", "-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd"])

    def test_mutation_flag_followed_by_int(self):
        self.assertRaises(IOError, Input, ["-r", 1, "-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd"])

    def test_mutation_flag_followed_by_non_int_castable_string(self):
        self.assertRaises(ValueError, Input,
                          ["-r", "no_int", "-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd"])

    def test_mutation_flag_followed_by_negative_number(self):
        self.assertRaises(ValueError, Input,
                          ["-r", "-1", "-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd"])

    def test_mutation_flag_followed_by_flag(self):
        self.assertRaises(ValueError, Input,
                          ["-r", "-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd", "-ate"])

    def test_mutation_flag_followed_by_empty_string(self):
        self.assertRaises(ValueError, Input,
                          ["-r", "", "-i", "../input_files/model1.prmtop ../input_files/model1.inpcrd"])

    # tests for input list argument
    def test_input_flag_not_present(self):
        self.assertRaises(IOError, Input,
                          ["-r", "23", "-a", "../input_files/model1.prmtop ../input_files/model1.inpcrd"])

    def test_input_flag_followed_by_single_string(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", "../input_files/F2196A.prmtop"])

    def test_input_flag_followed_by_empty_string(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i", ""])

    # tests for input list
    def test_input_list_not_even_number(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i",
                                              "../input_files/model1.prmtop ../input_files/model1.inpcrd ../input_files/F2196A.prmtop"])

    def test_input_list_not_starting_with_topology(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i",
                                              "../input_files/model1.prmtop ../input_files/model1.inpcrd prod_20.nc ../input_files/F2196A.prmtop"])

    def test_input_list_topology_not_followed_by_trajectory(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i",
                                              "../input_files/F2196A.prmtop 1 2 ../input_files/F2196A.inpcrd prod_20.nc ../input_files/F2196A.prmtop"])

    def test_input_list_trajectory_not_followed_by_topology(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i",
                                              "../input_files/F2196A.prmtop ../input_files/F2196A.inpcrd ../input_files/model1.inpcrd ../input_files/model1.prmtop"])

    def test_input_list_trajectory_not_followed_by_int_castable(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i",
                                              "../input_files/F2196A.prmtop ../input_files/F2196A.inpcrd last last ../input_files/F2196A.prmtop prod_1.out"])

    def test_input_list_end_le_start_frame(self):
        self.assertRaises(ValueError, Input, ["-r", "23", "-i",
                                              "../input_files/F2196A.prmtop ../input_files/prod_20.nc 2 1 ../input_files/F2196A.prmtop prod_1.inpcrd"])

    # ## tests for cpptraj_helper.py
    def test_specified_frames_exeeding_trajectory_frames(self):
        self.assertRaises(ValueError, Input,
                          ["-a", "-hy", "-i",
                           "/l_mnt/scratch/u/rm001/Occupancy/input_files/F2196A.prmtop /l_mnt/scratch/u/rm001/Occupancy/input_files/F2196A.inpcrd 1 100",
                           "-r",
                           "23"])

if __name__ == '__main__':
    unittest.main()
