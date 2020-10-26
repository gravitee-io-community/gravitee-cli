
import enum
from graviteeio_cli.lint.formats.openapi import isOpenApiv2, isOpenApiv3, isOpenApiv3_1


class Document:
    def __init__(self, values, doc_type, source=None,):
        super().__init__()
        # self.source = source
        self.values = values
        if doc_type == DocumentType.gio_apim:
            self.doc_format = "gio_apim"
        elif doc_type == DocumentType.oas and isOpenApiv2(values):
            self.doc_format = "oas2"
        elif doc_type == DocumentType.oas and (isOpenApiv3(values) or isOpenApiv3_1(values)):
            self.doc_format = "oas3"

    def is_format_in(self, formats):
        return self.doc_format in formats


class DocumentType(enum.Enum):
    gio_apim = 1,
    oas = 2
