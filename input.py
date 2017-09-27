class Input:
    def __init__(self, argv):
        self.argv = argv
        if not isinstance(argv,list):
            raise TypeError("Input has to be of type list. Given: %s" % type(argv))

        if len(argv) < 4:
            raise TypeError("At least four arguments needed. Given: %d" % len(argv))

        if len(argv) > 7:
            raise TypeError("A maximum of 7 arguments is allowed. Given: %d" % len(argv))

        # get specified mutation
        self.mutation = -1

        for i in range(0, len(argv)):
            if argv[i] == "-r":
                if not isinstance(argv[i + 1], str):
                    raise IOError("Argument following -r not a string. Given: %s" % type(argv[i + 1]))

                try:
                    self.mutation = int(argv[i + 1])
                    if self.mutation < 0:
                        raise ValueError("Mutation argument has to be a positive number. Given: %s" % argv[i + 1])
                except ValueError:
                    raise ValueError("Argument following -r not castable to int. Given: %s" % argv[i + 1])

        if self.mutation == -1:
            raise IOError("-r flag not found.")

        # get specified prmtop, trajectory list

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

        # for i in range(0, len(self.input) - 2):
        #     if ".prmtop" in self.input[i]:
        #         if ".prmtop" not in self.input[i + 2]:
        #             raise ValueError(
        #                 "Every second element in the input list has to be of type prmtop. Given: %s" % self.input)

        # check trajectories
        # if not any(ext in self.input[1] for ext in [".inpcrd", ".nc", ".mdcrd", ".rst"]):
        #     raise IOError(
        #         "Second input has to be a trajectory file (.nc, .inpcrd, .rst, .mdrcd). Given %s" % self.input[1])

        for i in range(1, len(self.input)):
            if any(ext in self.input[i] for ext in [".inpcrd", ".nc", ".mdcrd", ".rst"]):
                if i + 1 < len(self.input):
                    if ".prmtop" not in self.input[i + 1]:
                        if i + 2 < len(self.input):
                            if not self.input[i + 1].isdigit() or not self.input[i + 2].isdigit():
                                raise ValueError(
                                    "Trajectory file has to be followed by a topology or start and end frame. Given: "
                                    "%s" % self.input[i + 1])

        # other flags
        self.strip_hydro = bool([s for s in self.argv if "-hy" in s])
        self.strip_water = bool([s for s in self.argv if "-w" in s])
        self.calc_averages = bool([s for s in self.argv if "-a" in s])

        # output folder
        self.folder = "occupancies/"
