from pathlib import Path
import pkgutil

COMMANDS = []

for (_, name, _) in pkgutil.iter_modules([Path(__file__).parent]):
    COMMANDS.append(name[4:len(name)])
