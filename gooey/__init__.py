from gooey.python_bindings.gooey_decorator import Gooey
from gooey.python_bindings.gooey_parser import GooeyParser

with open('version', 'r') as f:
	version_num = f.read()

__version__ = version_num

