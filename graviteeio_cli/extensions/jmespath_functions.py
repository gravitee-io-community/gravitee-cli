from jmespath import functions
from datetime import datetime


class GioFunctions(functions.Functions):

    @functions.signature({'types': ['number']}, {'types': ['string']})
    def _func_datetime(self, timestamp, str_format=""):
        t = datetime.fromtimestamp(timestamp / 1000)
        if not str_format or len(str_format) == 0:
            return t.isoformat()
        else:
            return t.strftime(str_format)

    @functions.signature({'types': ['string']})
    def _func_upper(self, value):
        return value.upper()
