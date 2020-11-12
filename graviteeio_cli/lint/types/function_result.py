class FunctionResult:
    def __init__(
        self,
        message,
        path=None
    ):

        super().__init__()
        if path:
            new_path = []
            for p in path:
                if type(p) is str:
                    new_path.append(p)
                elif p:
                    new_path.append(str(p))
            path = new_path

        self.path = path
        self.message = message
