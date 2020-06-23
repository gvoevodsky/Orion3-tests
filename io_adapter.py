class IOAdapter:
    xxx = 123
    io_object = None
    open_cli_function = None

    def __init__(self, io_object, io_method, open_cli):
        self.io_method = io_method
        self.io_object = io_object
        self.open_cli_function = open_cli

    def send(self, *pargs):
        return self.io_method(self.io_object, pargs)

    def open_cli(self):
        if self.open_cli_function is not None:
            self.open_cli_function(self.io_object)