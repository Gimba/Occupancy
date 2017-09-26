class Inputs():
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
                except ValueError:
                    raise ValueError("Argument following -r not castable to int. Given: %s" % argv[i + 1])

        if self.mutation == -1:
            raise IOError("-r flag not found.")
