import enum


class DiagSeverity(enum.Enum):

    # Something not allowed by the rules of a language or other means.
    Error = 0,
    # Something suspicious but allowed.
    Warn = 1,
    # Something to inform about but not a problem.
    Info = 2,
    # Something to hint to a better way of doing it, like proposing
    #  a refactoring.
    Hint = 3

    @staticmethod
    def value_of(value):
        for level in DiagSeverity:
            if level.name == value:
                return level
