import pkg_resources  # part of setuptools

__version__ = pkg_resources.require("gear_score")[0].version
