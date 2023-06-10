import os

from hyfi import HyFI, about, global_config

from ._version import __version__

# Read the package name from the current directory
__package_name__ = os.path.basename(os.path.dirname(__file__))

# Extract package information
about.__package_name__ = __package_name__


def get_version() -> str:
    """This is the cli function of the package"""
    return __version__
