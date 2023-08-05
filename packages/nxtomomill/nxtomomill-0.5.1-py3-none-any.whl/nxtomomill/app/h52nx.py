# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2015-2020 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/

"""
This module provides global definitions and methods to transform
a tomo dataset written in edf into and hdf5/nexus file
"""

__authors__ = ["C. Nemoz", "H. Payno", "A.Sole"]
__license__ = "MIT"
__date__ = "16/01/2020"

import logging
from nxtomomill import utils
from nxtomomill.utils import Progress
from nxtomomill.converter import from_h5_to_nx
from nxtomomill.io.confighandler import HDF5ConfigHandler
from nxtomomill.io.confighandler import SETTABLE_PARAMETERS_UNITS
from collections.abc import Iterable
import argparse


logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)


def _getPossibleInputParams():
    """

    :return: string with param1 (expected unit) ...
    """
    res = []
    for key, value in SETTABLE_PARAMETERS_UNITS.items():
        res.append("{} ({})".format(key, value))
    return ", ".join(res)


def _ask_for_selecting_detector(det_grps: Iterable):
    res = input(
        "Several detector found. Only one detector is managed at the "
        "time. Please enter the name of the detector you want to use "
        'or "Cancel" to stop translation ({})'.format(det_grps)
    )
    if res == "Cancel":
        return None
    elif res in det_grps:
        return res
    else:
        print("detector name not recognized.")
        return _ask_for_selecting_detector(det_grps)


def main(argv):
    """"""
    parser = argparse.ArgumentParser(
        description="convert data acquired as "
        "hdf5 from bliss to nexus "
        "`NXtomo` classes. For `zseries` it will create one entry per `z`"
    )
    parser.add_argument(
        "input_file", help="master file of the " "acquisition", default=None, nargs="?"
    )
    parser.add_argument(
        "output_file", help="output .nx or .h5 file", default=None, nargs="?"
    )
    parser.add_argument(
        "--file-extension",
        "--file_extension",
        default=None,
        help="extension of the output file. Valid values are "
        "" + "/".join(utils.FileExtension.values()),
    )
    parser.add_argument(
        "--single-file",
        help="merge all scan sequence to the same output file. "
        "By default create one file per sequence and "
        "group all sequence in the output file",
        dest="single_file",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "--overwrite",
        help="Do not ask for user permission to overwrite output files",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "--debug",
        help="Set logs to debug mode",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "--entries",
        help="Specify (root) entries to be converted. By default it will try "
        "to convert all existing entries.",
        default=None,
    )
    parser.add_argument(
        "--ignore-sub-entries",
        help="Specify (none-root) sub entries to ignore.",
        default=None,
    )
    parser.add_argument(
        "--raises-error",
        help="Raise errors if some data are not met instead of providing some"
        " default values",
        action="store_true",
        default=None,
    )
    parser.add_argument(
        "--field-of-view",
        help="Force the output to be `Half`  or `Full` acquisition. Otherwise "
        "parse raw data to find this information.",
        default=None,
    )
    parser.add_argument(
        "--no-input",
        "--no-input-for-missing-information",
        help="The user won't be ask for any inputs",
        dest="request_input",
        action="store_false",
        default=None,
    )
    parser.add_argument(
        "--standard-format",
        help="Format of the input file is the 'standard' tomography format",
        dest="is_xrd_ct_format",
        action="store_false",
        default=None,
    )
    parser.add_argument(
        "--xrd-ct-format",
        help="Format of the input file is the 'XRD-CT' tomography format",
        dest="is_xrd_ct_format",
        action="store_true",
        default=None,
    )

    parser.add_argument(
        "--x_trans_keys",
        "--x-trans-keys",
        default=None,
        help="x translation key in bliss HDF5 file",
    )
    parser.add_argument(
        "--y_trans_keys",
        "--y-trans-keys",
        default=None,
        help="y translation key in bliss HDF5 file",
    )
    parser.add_argument(
        "--z_trans_keys",
        "--z-trans-keys",
        default=None,
        help="z translation key in bliss HDF5 file",
    )
    parser.add_argument(
        "--valid_camera_names",
        "--valid-camera-names",
        default=None,
        help="Valid NXDetector dataset name to be considered. Otherwise will"
        "try to deduce them from NX_class attibute (value should be"
        "NXdetector) or from instrument group child structure.",
    )
    parser.add_argument(
        "--rot_angle_keys",
        "--rot-angle-keys",
        default=None,
        help="Valid dataset name for rotation angle",
    )
    parser.add_argument(
        "--acq_expo_time_keys",
        "--acq-expo-time-keys",
        default=None,
        help="Valid dataset name for acquisition exposure time",
    )
    parser.add_argument(
        "--x_pixel_size_key",
        "--x-pixel-size-key",
        default=None,
        help="X pixel size key to read",
    )
    parser.add_argument(
        "--y_pixel_size_key",
        "--y-pixel-size-key",
        default=None,
        help="Y pixel size key to read",
    )

    # scan titles
    parser.add_argument(
        "--init_titles",
        "--init-titles",
        default=None,
        help="Titles corresponding to init scans",
    )
    parser.add_argument(
        "--init_zserie_titles",
        "--init-zserie-titles",
        default=None,
        help="Titles corresponding to zserie init scans",
    )
    parser.add_argument(
        "--dark_titles",
        "--dark-titles",
        default=None,
        help="Titles corresponding to dark scans",
    )
    parser.add_argument(
        "--ref_titles",
        "--ref-titles",
        default=None,
        help="Titles corresponding to ref scans",
    )
    parser.add_argument(
        "--proj_titles",
        "--proj-titles",
        default=None,
        help="Titles corresponding to projection scans",
    )
    parser.add_argument(
        "--align_titles",
        "--align-titles",
        default=None,
        help="Titles corresponding to alignment scans",
    )
    parser.add_argument(
        "--set-params",
        default=None,
        nargs="*",
        help="Allow manual definition of some parameters. "
        "Valid parameters (and expected input unit) "
        "are: {}. Should be added at the end of the command line because "
        "will try to cover all text set after this "
        "option.".format(_getPossibleInputParams()),
    )

    parser.add_argument(
        "--config",
        "--config-file",
        "--configuration",
        "--configuration-file",
        default=None,
        help="file containing the full configuration to convert from h5 "
        "bliss to nexus",
    )
    options = parser.parse_args(argv[1:])
    if options.request_input:
        callback_det_sel = _ask_for_selecting_detector
    else:
        callback_det_sel = None
    try:
        configuration_handler = HDF5ConfigHandler(options, raise_error=True)
    except Exception as e:
        _logger.error(e)
        return
    else:
        for title in configuration_handler.configuration.init_titles:
            assert title != ""
        from_h5_to_nx(
            configuration=configuration_handler.configuration,
            progress=Progress(""),
            input_callback=None,
            detector_sel_callback=callback_det_sel,
        )
    exit(0)


if __name__ == "__main__":
    import sys

    main(sys.argv[1:])
