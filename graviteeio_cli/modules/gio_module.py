import enum


class GioModule(enum.IntEnum):
    APIM = 0
    AM = 1

    @staticmethod
    def list_name():
        return list(map(lambda c: c.name.lower(), GioModule))
