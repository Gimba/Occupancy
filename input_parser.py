class InputParser():
    def __init__(self, argv):
        self.argv = argv
        if not isinstance(argv,list):
            raise TypeError("Input has to be of type list. Given: %s" % type(argv))

        if len(argv) < 5:
            raise TypeError("At least four arguments needed. Given: %d" % len(argv))

        if len(argv) > 8:
            raise TypeError("A maximum of 8 arguments is allowed. Given: %d" % len(argv))
