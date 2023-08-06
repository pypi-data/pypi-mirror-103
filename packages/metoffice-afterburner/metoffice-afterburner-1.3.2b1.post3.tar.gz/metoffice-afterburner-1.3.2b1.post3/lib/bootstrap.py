# (C) British Crown Copyright 2016, Met Office
#
# See the LICENSE.TXT file included with the Afterburner
# software distribution for full license details.
"""
Contains code for bootstrapping the Afterburner runtime environment.
"""
from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)

import sys
import os
import warnings


def add_extra_site_dirs(append=False):
    """
    Add extra site directories to Python's module search path. Extra directory
    paths are read from the Afterburner site configuration file using the key
    named 'extra_site_dirs' under the 'python' section. For example::

        [python]
        extra_site_dirs=/some/local/package_dir:/our/site/lib/python

    By default, any extra directories are added to the front of sys.path. Paths
    which do not exist are silently ignored.

    :param bool append: Set to True to append directories to sys.path rather
        than insert them at the front.
    """
    try:
        from afterburner.config import ConfigProvider
        cp = ConfigProvider()
        extra_dirs = cp.get_config_option('python', 'extra_site_dirs').strip()
        if extra_dirs:
            paths = extra_dirs.split(os.pathsep)
            if append:
                for pth in paths:
                    if os.path.exists(pth): sys.path.append(pth)
            else:
                for pth in paths[::-1]:
                    if os.path.exists(pth): sys.path.insert(0, pth)
    except:
        exc = sys.exc_info()[1]
        warnings.warn("WARNING: Problem trying to update the module search path"
            " (add_extra_site_dirs)")
        warnings.warn("%r" % exc)
