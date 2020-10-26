class FunctionResult:
    def __init__(
        self,
        message,
        path=None
    ):

        super().__init__()

        new_path = []
        for p in path:
            if type(p) is str:
                new_path.append(p)
            elif p:
                new_path.append(str(p))

        self.path = new_path
        self.message = message

    def printPath(self):
        return ".".join(self.path)
        # if self.path and len(self.path) > 0:
        # else:
        #     return ""
