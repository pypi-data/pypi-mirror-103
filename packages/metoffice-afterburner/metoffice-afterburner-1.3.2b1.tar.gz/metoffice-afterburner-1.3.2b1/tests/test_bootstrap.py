# (C) British Crown Copyright 2016, Met Office
#
# See the LICENSE.TXT file included with the Afterburner
# software distribution for full license details.
"""
Unit tests for the bootstrap module.
"""
from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)

import os
import sys
import tempfile
import unittest
import bootstrap

try:
    # python3
    from unittest.mock import patch
except ImportError:
    # python2
    from mock import patch

from afterburner.config import ConfigProvider


class TestBootstrap(unittest.TestCase):
    """Unit tests for the bootstrap module."""

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        try:
            os.rmdir(self.tmp_dir)
        except OSError:
            pass

    def test_insert_path(self):
        "Test prepending an extra directory to sys.path."""
        with patch.object(ConfigProvider, 'get_config_option') as mock_get_config_option:
            mock_get_config_option.return_value = self.tmp_dir
            bootstrap.add_extra_site_dirs()
            mock_get_config_option.assert_called_with('python', 'extra_site_dirs')
            self.assertEqual(sys.path[0], self.tmp_dir)

    def test_append_path(self):
        "Test appending an extra directory to sys.path."""
        with patch.object(ConfigProvider, 'get_config_option') as mock_get_config_option:
            mock_get_config_option.return_value = self.tmp_dir
            bootstrap.add_extra_site_dirs(append=True)
            mock_get_config_option.assert_called_with('python', 'extra_site_dirs')
            self.assertEqual(sys.path[-1], self.tmp_dir)

    def test_non_existent_path(self):
        "Test adding a non-existent directory to sys.path."""
        with patch.object(ConfigProvider, 'get_config_option') as mock_get_config_option:
            mock_get_config_option.return_value = "/foo/bar/baz"
            bootstrap.add_extra_site_dirs()
            mock_get_config_option.assert_called_with('python', 'extra_site_dirs')
            self.assertTrue("/foo/bar/baz" not in sys.path)


if __name__ == '__main__':
    unittest.main()
