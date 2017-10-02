import cpptraj_helper as cpp
class Input:
    def __init__(self, argv):
        self.argv = argv
        if not isinstance(argv,list):
            raise TypeError("Input has to be of type list. Given: %s" % type(argv))

        if len(argv) < 4:
            raise TypeError("At least four arguments needed. Given: %d" % len(argv))

        if len(argv) > 13:
            raise TypeError("A maximum of 13 arguments is allowed. Given: %d" % len(argv))

        # get specified mutation
        self.mutation = -1

        for i in range(0, len(argv)):
            if argv[i] == "-r":
                if not isinstance(argv[i + 1], str):
                    raise IOError("Argument following -r not a string. Given: %s" % type(argv[i + 1]))

                try:
                    self.mutation = argv[i + 1]
                    if not self.mutation.isdigit():
                        raise ValueError("Mutation argument has to be a positive number. Given: %s" % argv[i + 1])
                except ValueError:
                    raise ValueError("Argument following -r not castable to int. Given: %s" % argv[i + 1])

        if self.mutation == -1:
            raise IOError("-r flag not found.")

        # get specified prmtop, trajectory list with start and end frames

        self.input = []

        for i in range(0, len(argv)):
            if argv[i] == "-i":

                try:
                    self.input = (argv[i + 1]).split()
                    if len(self.input) < 2:
                        raise ValueError("Too few input topologies and trajectories. Given: %s" % len(self.input))

                except ValueError:
                    raise ValueError("Argument following -i not castable to list. Given: %s" % argv[i + 1])

        if self.input == []:
            raise IOError("-i flag not found.")

        ## check input list ##
        if len(self.input) % 2 == 1:
            raise ValueError("Every topology has to be followed by a trajectory or a start and and frame (e.g. 1 200), "
                             "therefore the number of inputs has to be even. Given inputs: %d" % len(self.input))

        # check topologies
        if ".prmtop" not in self.input[0]:
            raise ValueError("List of inputs has to start with a topology (prmtop) file")

        for i in range(1, len(self.input)):
            if any(ext in self.input[i] for ext in [".inpcrd", ".nc", ".mdcrd", ".rst"]):
                if i + 1 < len(self.input):
                    if ".prmtop" not in self.input[i + 1]:
                        if i + 2 < len(self.input):
                            if not self.input[i + 1].isdigit() or not self.input[i + 2].isdigit():
                                raise ValueError(
                                    "Trajectory file has to be followed by a topology or start and end frame. Given: "
                                    "%s" % self.input[i + 1])

        # add start and end frames to trajectories
        temp_list = []
        for i in range(0, len(self.input)):
            if ".prmtop" in self.input[i]:
                item = [self.input[i], self.input[i + 1], "1", "1"]
                if i + 3 < len(self.input):
                    if self.input[i + 2].isdigit() and self.input[i + 3].isdigit():
                        item[2] = self.input[i + 2]
                        item[3] = self.input[i + 3]
                        if int(item[2]) > int(item[3]):
                            raise ValueError("Start frame higher than end frame. Given: %s " % item[2])
                temp_list.append(item)
        self.input = temp_list

        # check if trajectory contains enough frames
        for item in self.input:
            traj_frames = cpp.get_trajectory_length(item[0], item[1])
            if int(item[3]) > int(traj_frames):
                raise ValueError("Specified last frame %s greater than trajectory length %s." % (item[3], traj_frames))

        # other flags
        self.strip_hydro = bool([s for s in self.argv if "-hy" in s])
        self.strip_water = bool([s for s in self.argv if "-w" in s])
        self.calc_averages = bool([s for s in self.argv if "-a" in s])

        # output folder
        self.folder = "occupancies/"

        for i in range(0, len(argv)):
            if argv[i] == "-f":
                self.folder = argv[i + 1]

        # masks
        self.mask1 = 0
        self.mask2 = 0
        for i in range(0, len(argv)):
            if argv[i] == "-m1":
                self.mask1 = argv[i + 1]
            if argv[i] == "-m2":
                self.mask2 = argv[i + 1]

    # change path of files to output folder
    def set_file_paths_to_output_folder(self):
        for item in self.input:
            item[0] = item[0].split("/")[-1]
            item[1] = item[1].split("/")[-1]

    # get list of file names
    def get_file_names(self):
        file_names = []
        for item in self.input:
            file_names.append(" ".join(item))

        return file_names
