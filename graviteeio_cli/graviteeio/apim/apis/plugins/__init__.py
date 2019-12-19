from pathlib import Path
import pkgutil
from importlib import import_module
import inspect

COMMANDS = []

for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
    COMMANDS.append(name[4:len(name)])
# for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
#     imported_module = import_module('.' + name, package=__name__)

# imported_module = import_module('.ps', package=__name__)

# for i in dir(imported_module):
#     attribute = getattr(imported_module, i)
#     print("type {} {}".format(type(attribute), attribute))
#     if inspect.ismethod(attribute):
#         print("ismethod{}".format(attribute))
#     if inspect.isfunction(attribute):
#         print("isfunction{}".format(attribute))
#     if inspect.isframe(attribute):
#         print("isframe{}".format(attribute))

# pkg = __import__("graviteeio_cli.graviteeio.apim.apis")
# mod = getattr(pkg, "ps")
# mod.test();