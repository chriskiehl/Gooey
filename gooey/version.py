"""Definition of __version__."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("Gooey")
except PackageNotFoundError:
    __version__ = "unknown"
