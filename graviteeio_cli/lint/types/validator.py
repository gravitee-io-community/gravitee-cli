class Validator:
    def __init__(
        self,
        func,
        func_args
    ):

        super().__init__()
        self.func = func
        self.args = func_args
