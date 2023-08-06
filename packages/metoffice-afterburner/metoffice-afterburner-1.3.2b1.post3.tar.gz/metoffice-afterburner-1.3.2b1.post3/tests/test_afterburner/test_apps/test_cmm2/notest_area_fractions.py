# (C) British Crown Copyright 2018, Met Office
#
# See the LICENSE.TXT file included with the Afterburner
# software distribution for full license details.
"""
Test the handling of land-area and sea-area fraction corrections in the
afterburner.apps.model_monitor2.ModelMonitor2 application.

NOTE: This module is functionally equivalent to the test_area_fractions.py
module but is considerably more compact owing to the use of parameterised test
cases. Unfortunately the nosetests utility doesn't appear to work correctly with
these tests. Accordingly, this module has been retained for future reference
purposes, but has been renamed so as to prevent it being picked up by automated
testing tasks. 
"""
from __future__ import (absolute_import, division, print_function)
from six.moves import (filter, input, map, range, zip)

import os
import sys
import shutil
import tempfile
import unittest
import warnings
import logging
import numpy as np
import numpy.ma as ma

try:
    # python3
    from unittest import mock
except ImportError:
    # python2
    import mock

import iris
from iris.fileformats.pp import STASH

try:
    from afterburner.apps.model_monitor2 import ModelMonitor2
    from afterburner.misc import stockcubes
    got_rose_config = True
except ImportError:
    got_rose_config = False

# Template for a CMM2 app config file.
_app_config_template = """
    [file:models.nl]
    source=namelist:models(:)

    [file:diags.nl]
    source=namelist:diags(:)

    [general]
    sync_with_mass=false
    cache_type=VarSplit
    cache_dir=$RUNTIME_DIR/varsplit
    output_dir=$RUNTIME_DIR/output

    [namelist:models(anqjm)]
    enabled=true
    label=ANQJM
    name=anqjm
    plot_order=1
    laf_threshold={0}

    [namelist:diags(tas_global)]
    enabled=true
    stashcode=m01s00i024
    statistic=mean
    apply_laf_corr={1}
    apply_saf_corr={2}
"""

# Define test arguments to pass to the init method of the TestAreaFractions
# class.
test_args = [
    {'test_name': 'laf_w_defaults', 'result': 7.5, 'laf_corr': True,
        'masked_laf': False, 'land_frac': 0.75, 'sea_frac': 0.25, 'laf_threshold': 0.5},
    {'test_name': 'laf_w_zero_threshold', 'result': 2.5, 'laf_corr': True,
        'masked_laf': False, 'land_frac': 0.25, 'sea_frac': 0.0, 'laf_threshold': 0.0},
    {'test_name': 'laf_w_masked_laf', 'result': 10.0, 'laf_corr': True,
        'masked_laf': True, 'land_frac': 1.0, 'sea_frac': 0.0, 'laf_threshold': 0.5},
    {'test_name': 'saf_w_defaults', 'result': 7.5, 'laf_corr': False,
        'masked_laf': False, 'land_frac': 0.75, 'sea_frac': 0.25, 'laf_threshold': 0.5},
    {'test_name': 'saf_w_zero_threshold', 'result': 10.0, 'laf_corr': False,
        'masked_laf': False, 'land_frac': 0.75, 'sea_frac': 0.0, 'laf_threshold': 0.0},
    {'test_name': 'saf_w_masked_laf', 'result': 10.0, 'laf_corr': True,
        'masked_laf': True, 'land_frac': 1.0, 'sea_frac': 0.0, 'laf_threshold': 0.5},
]


# Use the load_tests() function to specify a suite of test cases to run based on
# the test arguments defined above via the test_args variable. 
def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for argdict in test_args:
        test = TestAreaFractions('runTest', **argdict)
        suite.addTest(test)
    return suite


@unittest.skipUnless(got_rose_config, "rose config module not found")
class TestAreaFractions(unittest.TestCase):
    """
    Test the handling of land-area and sea-area fraction corrections in the
    afterburner.apps.model_monitor2.ModelMonitor2 application.
    """
    def __init__(self, method_name, test_name='', result=None, laf_corr=True,
            masked_laf=False, land_frac=1.0, sea_frac=0.0, laf_threshold=0.5):
        super(TestAreaFractions, self).__init__(method_name)

        self.test_name = test_name
        self.result = result
        self.laf_corr = laf_corr
        self.saf_corr = not laf_corr
        self.masked_laf = masked_laf
        self.land_frac = land_frac
        self.sea_frac = sea_frac
        self.laf_threshold = laf_threshold

    def shortDescription(self):
        return self.test_name

    def setUp(self):
        self.runtime_dir = tempfile.mkdtemp()
        os.environ['RUNTIME_DIR'] = self.runtime_dir
        _fd, self.cfg_file = tempfile.mkstemp(suffix='.conf', dir=self.runtime_dir)

        # Patch the ModelMonitor._load_latest_model_data() function.
        patch = mock.patch('afterburner.apps.model_monitor2.ModelMonitor2._load_latest_model_data')
        self.mock_load_model_data = patch.start()
        self.addCleanup(patch.stop)

        # Patch the ModelMonitor._load_laf_data() function.
        patch = mock.patch('afterburner.apps.model_monitor2.ModelMonitor2._load_laf_data')
        self.mock_load_laf_data = patch.start()
        self.addCleanup(patch.stop)

        # Disable logging.
        lgr = logging.getLogger('afterburner.apps')
        self.log_level = lgr.level
        lgr.level = 100

    def tearDown(self):
        if os.path.isdir(self.runtime_dir):
            shutil.rmtree(self.runtime_dir, ignore_errors=True)

        # Re-enable logging
        lgr = logging.getLogger('afterburner.apps')
        lgr.level = self.log_level

    def runTest(self):

        # create a test cube with all data values the same
        test_value = 10.0
        test_cube = stockcubes.geo_tyx(test_value)
        test_cube.attributes['STASH'] = STASH.from_msi('m01s00i024')
        self.mock_load_model_data.return_value = iris.cube.CubeList([test_cube])

        # create a LAF cube with an approx 50-50 split of land and sea points
        laf_cube = _create_laf_cube(test_cube, land_frac=self.land_frac,
            sea_frac=self.sea_frac)
        if self.masked_laf: laf_cube.data = ma.masked_equal(laf_cube.data, 0)
        self.mock_load_laf_data.return_value = laf_cube

        app_config = _app_config_template.format(self.laf_threshold, self.laf_corr,
            self.saf_corr)
        _create_app_config_file(self.cfg_file, app_config)
        args = ['-c', self.cfg_file, '-q']
        app = ModelMonitor2(args)
        app.run()

        self.mock_load_model_data.assert_called_once()
        self.mock_load_laf_data.assert_called_once()

        # test for existence of 1 netcdf file
        nc_dir = os.path.join(app.nc_output_dir, 'mean')
        nc_files = os.listdir(nc_dir)
        self.assertEqual(len(nc_files), 1)

        nc_file = os.path.join(nc_dir, nc_files[0])
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cube = iris.load_cube(nc_file)
            self.assertAlmostEqual(cube.data[0], self.result, places=5)


def _create_app_config_file(config_file, config_text):
    "Create a CMM2 app config file from the given text string."
    with open(config_file, 'w') as fh:
        fh.writelines([line.strip()+'\n' for line in config_text.split('\n')])


def _create_laf_cube(test_cube, land_frac=1.0, sea_frac=0.0):
    "Create a land-area fraction cube with a ~50-50 split of land and sea points."
    npts = np.product(test_cube.shape[-2:])
    laf_data = np.zeros(npts, dtype=np.float32)
    laf_data[:] = land_frac
    laf_data[::2] = sea_frac
    laf_data.shape = test_cube.shape[-2:]
    laf_cube = iris.cube.Cube(laf_data, standard_name='land_area_fraction',
        units='1')
    return laf_cube


if __name__ == '__main__':
    unittest.main()
