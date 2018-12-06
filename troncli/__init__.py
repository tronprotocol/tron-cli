#!/usr/bin/env python3

import pkg_resources

__version__ = pkg_resources.get_distribution("troncli").version

__all__ = [
    '__version__',
]