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
#
# ###########################################################################*/

"""
contains the HDF5Config
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "23/02/2021"


from nxtomomill import settings
from nxtomomill.utils import FileExtension
from nxtomomill.utils import Format
from nxtomomill.utils import FieldOfView
from nxtomomill.io.utils import is_url_path
from nxtomomill.io.utils import convert_str_to_tuple
from nxtomomill.io.utils import convert_str_to_frame_grp
from nxtomomill.io.utils import filter_str_def
from silx.io.url import DataUrl
from typing import Union
from typing import Iterable
import configparser
import logging
from nxtomomill.io.framegroup import FrameGroup

_logger = logging.getLogger(__name__)


def _example_fg_list(with_comment=True, with_prefix=False) -> str:
    """
    Print a simple example of providing a list of FrameGroup from str
    """

    fg_1 = FrameGroup(
        frame_type="projection",
        url=DataUrl(
            file_path="/path/to/file", data_path="/path/to/scan/node", scheme="silx"
        ),
        copy=True,
    )
    fg_2 = FrameGroup(
        frame_type="projection",
        url=DataUrl(
            file_path="/path/to/file2",
            data_path="/path_relative_to_file",
            scheme="silx",
        ),
    )
    if with_comment:
        comment = "# "
    else:
        comment = ""
    if with_prefix:
        prefix = "data_scans = "
    else:
        prefix = ""

    return """
{comment}{prefix}(
{comment}    {fg_1},
{comment}    {fg_2},
{comment})
""".format(
        prefix=prefix,
        comment=comment,
        fg_1=fg_1.str_representation(
            only_data_path=False, with_copy=True, with_prefix_key=True
        ),
        fg_2=fg_2.str_representation(
            only_data_path=True, with_copy=False, with_prefix_key=True
        ),
    )


class HDF5Config:
    """
    Configuration class to provide to the convert from h5 to nx
    """

    # General section keys

    GENERAL_SECTION_DK = "GENERAL_SECTION"

    OUTPUT_FILE_DK = "output_file"

    INPUT_FILE_DK = "input_file"

    OVERWRITE_DK = "overwrite"

    FILE_EXTENSION_DK = "file_extension"

    LOG_LEVEL_DK = "log_level"

    RAISES_ERROR_DK = "raises_error"

    NO_INPUT_DK = "no_input"

    INPUT_FORMAT_DK = "format"

    SINGLE_FILE_DK = "single_file"

    FIELD_OF_VIEW_DK = "field_of_view"

    COMMENTS_GENERAL_SECTION = {
        GENERAL_SECTION_DK: "general information. \n",
        OUTPUT_FILE_DK: "output file name. If not provided will use the input file basename and the file extension",
        INPUT_FILE_DK: "input file if not provided must be provided from the command line",
        OVERWRITE_DK: "overwrite output files if exists without asking",
        FILE_EXTENSION_DK: "file extension. Ignored if the output file is provided and contains an extension",
        LOG_LEVEL_DK: 'Log level. Valid levels are "debug", "info", "warning" and "error"',
        RAISES_ERROR_DK: "raise an error when met one. Otherwise continue and display an error log",
        NO_INPUT_DK: "Ask or not the user for any inputs (if missing information)",
        INPUT_FORMAT_DK: 'acquisition type. If not provided will try to guess it. Valid values are "standard", "xrd-ct" and "" if undetermined',
        SINGLE_FILE_DK: "If True then will create a single file for all found sequences. "
        "If false create one nexus file per sequence and one master file with links to each sequence",
        FIELD_OF_VIEW_DK: "Force output to be a `Full` or a `Half` acquisition. If not provided we parse raw data to try to find this information.",
    }

    # KEYS SECTION

    KEYS_SECTION_DK = "KEYS_SECTION"

    VALID_CAMERA_DK = "valid_camera_names"

    ROT_ANGLE_DK = "rotation_angle_keys"

    X_TRANS_KEYS_DK = "x_translation_keys"

    Y_TRANS_KEYS_DK = "y_translation_keys"

    Z_TRANS_KEYS_DK = "z_translation_keys"

    Y_ROT_KEYS_DK = "y_rot_keys"

    DIODE_KEYS_DK = "diode_keys"

    ACQUISITION_EXPO_TIME_KEYS_DK = "exposure_time_keys"

    COMMENTS_KEYS_SECTION = {
        KEYS_SECTION_DK: "Identify specific path and datasets names to retrieve information from the bliss file. \n",
        VALID_CAMERA_DK: "Nxtomomill will try to deduce cameras from  dataset "
        "metadata and shape if none provided (default)."
        "If provided take the one requested. unix "
        "shell-style wildcards are managed",
        ROT_ANGLE_DK: "List of key to look for in order to find rotation angle",
        X_TRANS_KEYS_DK: "List of keys / paths to look for in order to find translation in x",
        Y_TRANS_KEYS_DK: "List of keys / paths to look for in order to find translation in y",
        Z_TRANS_KEYS_DK: "List of /paths keys to look for in order to find translation in z",
        Y_ROT_KEYS_DK: "Key used to deduce the estimated center of rotation for half acquisition",
        DIODE_KEYS_DK: "List of keys to look for diode (if any)",
        ACQUISITION_EXPO_TIME_KEYS_DK: "List of keys to look for the exposure time",
    }

    # ENTRIES AND TITLES SECTION

    ENTRIES_AND_TITLES_SECTION_DK = "ENTRIES_AND_TITLES_SECTION"

    ENTRIES_DK = "entries"

    SUB_ENTRIES_TO_IGNORE = "sub_entries_to_ignore"

    INIT_TITLES_DK = "init_titles"

    ZSERIE_INIT_TITLES_DK = "zserie_init_titles"

    DARK_TITLES_DK = "dark_titles"

    REF_TITLES_DK = "ref_titles"

    PROJ_TITLES_DK = "proj_titles"

    ALIGNMENT_TITLES_DK = "alignment_titles"

    X_PIXEL_SIZE_KEYS_DK = "x_pixel_keys"

    Y_PIXEL_SIZE_KEYS_DK = "y_pixel_keys"

    COMMENTS_ENTRIES_TITLES_SECTION = {
        ENTRIES_AND_TITLES_SECTION_DK: "optional section \n"
        "# define titles meaning. Titles allows frame type deduction for each group.\n",
        ENTRIES_DK: "List of root entries (sequence initialization) to convert. If not provided will convert all root entries",
        SUB_ENTRIES_TO_IGNORE: "List of sub entries (non-root) to ignore",
        ACQUISITION_EXPO_TIME_KEYS_DK: "List of keys to look for the exposure time",
        INIT_TITLES_DK: "List of title to consider the group/entry as a initialization (sequence start). Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        ZSERIE_INIT_TITLES_DK: "List of title to consider the group/entry as a zserie initialization (sequence start). Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        DARK_TITLES_DK: "List of title to consider the group/entry as a dark.  Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        REF_TITLES_DK: "List of title to consider the group/entry as a reference / flat.  Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        PROJ_TITLES_DK: "List of title to consider the group/entry as a projection.  Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        ALIGNMENT_TITLES_DK: "List of title to consider the group/entry as an alignment.  Ignored if dark_groups, flat_groups, projection_groups ... are provided.",
        X_PIXEL_SIZE_KEYS_DK: "List of keys / paths to look for the x pixel size",
        Y_PIXEL_SIZE_KEYS_DK: "List of keys / paths to look for the y pixel size",
    }

    # FRAMES TYPE SECTION

    FRAME_TYPE_SECTION_DK = "FRAME_TYPE_SECTION"

    DATA_DK = "data_scans"

    DEFAULT_DATA_COPY_DK = "default_data_copy"

    COMMENTS_FRAME_TYPE_SECTION = {
        FRAME_TYPE_SECTION_DK: "optional section\n"
        "# Allows to define scan to be used for NXTomo conversion\n"
        "# The sequence order will follow the order provided.\n",
        DATA_DK: "list of scans to be converted. Frame type should be "
        "provided for each scan.\n# Expected format is:\n"
        "{}"
        "# * `frame_type` (mandatory): values can be `projection`, `flat`, "
        "`dark`, `alignment` or `init`. \n"
        "# * `entry` (mandatory): DataUrl with path to the scan to integrate. "
        "If the scan is contained in the input_file then you can only provide "
        "path/name of the scan. \n"
        "# * copy (optional): you can provide a different behavior for the "
        "this scan (should we duplicate data or not) \n"
        "# More details are available here: {}".format(
            _example_fg_list(with_prefix=True), "TODO: provide link"
        ),
        DEFAULT_DATA_COPY_DK: "You can duplicate data inside the input file or create a link to the original frames. "
        "In this case you should keep the relative position of the files",
    }

    # extra params section

    EXTRA_PARAMS_SECTION_DK = "EXTRA_PARAMS_SECTION"

    EXTRA_PARAMS_ENERGY_DK = "energy"
    EXTRA_PARAMS_X_PIXEL_SIZE_DK = "x_pixel_size"
    EXTRA_PARAMS_Y_PIXEL_SIZE_DK = "y_pixel_size"

    EXTRA_PARAMS_ENERGY_VALID_KEYS = (
        EXTRA_PARAMS_ENERGY_DK,
        EXTRA_PARAMS_X_PIXEL_SIZE_DK,
        EXTRA_PARAMS_Y_PIXEL_SIZE_DK,
    )

    COMMENTS_EXTRA_PARAMS_SECTION = {
        EXTRA_PARAMS_SECTION_DK: "optional section\n"
        "# you can predefined values which are missing in the input .h5 file\n"
        "# Handled parameters are {}".format(EXTRA_PARAMS_ENERGY_VALID_KEYS)
    }

    COMMENTS = COMMENTS_GENERAL_SECTION
    COMMENTS.update(COMMENTS_KEYS_SECTION)
    COMMENTS.update(COMMENTS_ENTRIES_TITLES_SECTION)
    COMMENTS.update(COMMENTS_FRAME_TYPE_SECTION)
    COMMENTS.update(COMMENTS_EXTRA_PARAMS_SECTION)

    def __init__(self):
        # general information
        self._output_file = None
        self._input_file = None
        self._overwrite = False
        self._file_extension = FileExtension.NX
        self._log_level = logging.WARNING
        self._raises_error = False
        self._no_input = False
        self._format = None
        self._single_file = False
        self._field_of_view = None

        # information regarding keys and paths
        self._valid_camera_names = settings.H5_VALID_CAMERA_NAMES
        self._rot_angle_keys = settings.H5_ROT_ANGLE_KEYS
        self._x_trans_keys = settings.H5_X_TRANS_KEYS
        self._y_trans_keys = settings.H5_Y_TRANS_KEYS
        self._z_trans_keys = settings.H5_Z_TRANS_KEYS
        self._y_rot_key = settings.H5_Y_ROT_KEY
        self._diode_keys = settings.H5_DIODE_KEYS
        self._expo_time_keys = settings.H5_ACQ_EXPO_TIME_KEYS

        # information regarding titles
        self._entries = None
        self._sub_entries_to_ignore = None
        self._init_titles = settings.H5_INIT_TITLES
        self._zserie_init_titles = settings.H5_ZSERIE_INIT_TITLES
        self._dark_titles = settings.H5_DARK_TITLES
        self._flat_titles = settings.H5_REF_TITLES
        self._projection_titles = settings.H5_PROJ_TITLES
        self._alignment_titles = settings.H5_ALIGNMENT_TITLES
        self._x_pixel_size_paths = settings.H5_X_PIXEL_SIZE
        self._y_pixel_size_paths = settings.H5_Y_PIXEL_SIZE

        # information regarding frames types definition
        self._data_grps_urls = tuple()
        self._default_copy_behavior = False

        # extra options
        self._param_already_defined = {}

    @property
    def input_file(self) -> Union[None, str]:
        return self._input_file

    @input_file.setter
    def input_file(self, input_file: Union[None, str]):
        if not isinstance(input_file, (str, type(None))):
            raise TypeError(
                "'input_file' should be None or an instance of Iterable. Not {}".format(
                    type(input_file)
                )
            )
        elif input_file == "":
            self._input_file = None
        else:
            self._input_file = input_file

    @property
    def output_file(self) -> Union[None, str]:
        return self._output_file

    @output_file.setter
    def output_file(self, output_file: Union[None, str]):
        if not isinstance(output_file, (str, type(None))):
            raise TypeError("'input_file' should be None or an instance of Iterable")
        elif output_file == "":
            self._output_file = None
        else:
            self._output_file = output_file

    @property
    def overwrite(self) -> bool:
        return self._overwrite

    @overwrite.setter
    def overwrite(self, overwrite: bool) -> None:
        if not isinstance(overwrite, bool):
            raise TypeError("'overwrite' should be a boolean")
        else:
            self._overwrite = overwrite

    @property
    def file_extension(self) -> FileExtension:
        return self._file_extension

    @file_extension.setter
    def file_extension(self, file_extension: str):
        self._file_extension = FileExtension.from_value(file_extension)

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, level: str):
        self._log_level = getattr(logging, level.upper())

    @property
    def raises_error(self):
        return self._raises_error

    @raises_error.setter
    def raises_error(self, raises_error: bool):
        if not isinstance(raises_error, bool):
            raise TypeError("'raises_error' should be a boolean")
        else:
            self._raises_error = raises_error

    @property
    def no_input(self):
        return self._no_input

    @no_input.setter
    def no_input(self, no_input):
        if not isinstance(no_input, bool):
            raise TypeError("'raises_error' should be a boolean")
        else:
            self._no_input = no_input

    @property
    def request_input(self) -> bool:
        return not self._no_input

    @request_input.setter
    def request_input(self, request: bool):
        assert isinstance(request, bool), "request should be a bool"
        self._no_input = not request

    @property
    def format(self):
        return self._format

    @format.setter
    def format(self, format_: Union[None, str]):
        if format_ is None:
            self._format = None
        else:
            self._format = Format.from_value(format_)

    @property
    def is_xrdc_ct(self):
        return self._format == Format.XRD_CT

    @property
    def single_file(self):
        return self._single_file

    @single_file.setter
    def single_file(self, single_file):
        if not isinstance(single_file, bool):
            raise TypeError("'single_file' should be a boolean")
        else:
            self._single_file = single_file

    @property
    def field_of_view(self) -> Union[None, FieldOfView]:
        return self._field_of_view

    @field_of_view.setter
    def field_of_view(self, fov: Union[None, FieldOfView, str]):
        if fov is None:
            self._field_of_view = fov
        elif isinstance(fov, str):
            self._field_of_view = FieldOfView.from_value(fov.title())
        elif isinstance(fov, FieldOfView):
            self._field_of_view = fov
        else:
            raise TypeError(
                "fov is expected to be None, a string or "
                "FieldOfView. Not {}".format(type(fov))
            )

    # Keys section

    @property
    def valid_camera_names(self) -> Union[None, tuple]:
        return self._valid_camera_names

    @valid_camera_names.setter
    def valid_camera_names(self, names: Union[None, Iterable]) -> None:
        if not isinstance(names, (Iterable, type(None))):
            raise TypeError("'names' should be None or an instance of Iterable")
        else:
            self._valid_camera_names = names

    @property
    def rotation_angle_keys(self) -> Iterable:
        return self._rot_angle_keys

    @rotation_angle_keys.setter
    def rotation_angle_keys(self, keys: Iterable):
        if not isinstance(keys, Iterable):
            raise TypeError("'keys' should be an Iterable")
        else:
            self._rot_angle_keys = keys

    @property
    def x_trans_keys(self) -> Iterable:
        return self._x_trans_keys

    @x_trans_keys.setter
    def x_trans_keys(self, keys) -> None:
        if not isinstance(keys, Iterable):
            raise TypeError("'keys' should be an Iterable")
        else:
            self._x_trans_keys = keys

    @property
    def y_trans_keys(self) -> Iterable:
        return self._y_trans_keys

    @y_trans_keys.setter
    def y_trans_keys(self, keys) -> None:
        if not isinstance(keys, Iterable):
            raise TypeError("'keys' should be an Iterable")
        else:
            self._y_trans_keys = keys

    @property
    def z_trans_keys(self) -> Iterable:
        return self._z_trans_keys

    @z_trans_keys.setter
    def z_trans_keys(self, keys) -> None:
        if not isinstance(keys, Iterable):
            raise TypeError("'keys' should be an Iterable")
        else:
            self._z_trans_keys = keys

    @property
    def y_rot_key(self) -> str:
        return self._y_rot_key

    @y_rot_key.setter
    def y_rot_key(self, key) -> None:
        if not isinstance(key, str):
            raise TypeError("'key' should be a string")
        else:
            self._y_rot_key = key

    @property
    def diode_keys(self) -> Iterable:
        return self._diode_keys

    @diode_keys.setter
    def diode_keys(self, keys: Iterable) -> None:
        if not isinstance(keys, Iterable):
            raise TypeError("'keys' should be an Iterable")
        else:
            self._diode_keys = keys

    @property
    def exposition_time_keys(self) -> Iterable:
        return self._expo_time_keys

    @exposition_time_keys.setter
    def exposition_time_keys(self, keys: Iterable) -> None:
        if not isinstance(keys, Iterable):
            raise TypeError("'keys' should be an Iterable")
        else:
            self._expo_time_keys = keys

    # entries section
    @property
    def entries(self) -> Union[None, tuple]:
        return self._entries

    @entries.setter
    def entries(self, entries: Union[None, tuple]):
        if not isinstance(entries, (type(None), tuple)):
            raise ValueError("entries should be None or an instance of Iterable")
        elif entries is None:
            self._entries = None
        else:
            entries = self._parse_frame_urls(entries)
            entries = tuple([self._fix_entry_name(entry) for entry in entries])
            if len(entries) == 0:
                self._entries = None
            else:
                self._entries = entries

    @staticmethod
    def _fix_entry_name(entry: DataUrl):
        """simple util function to insure the entry start by a "/"""
        if not isinstance(entry, DataUrl):
            raise TypeError("entry is expected to be a DataUrl")
        if not entry.data_path().startswith("/"):
            entry = DataUrl(
                scheme=entry.scheme(),
                data_slice=entry.scheme(),
                file_path=entry.file_path(),
                data_path="/" + entry.data_path(),
            )
        return entry

    @property
    def sub_entries_to_ignore(self) -> Union[None, tuple]:
        return self._sub_entries_to_ignore

    @sub_entries_to_ignore.setter
    def sub_entries_to_ignore(self, entries: Union[None, tuple]):
        if not isinstance(entries, (type(None), tuple)):
            raise ValueError("entries should be None or an instance of Iterable")
        elif entries is None:
            self._sub_entries_to_ignore = None
        else:
            entries = self._parse_frame_urls(entries)
            entries = tuple([self._fix_entry_name(entry) for entry in entries])
            self._sub_entries_to_ignore = entries

    # titles section
    @property
    def init_titles(self) -> Union[Iterable, None]:
        return self._init_titles

    @init_titles.setter
    def init_titles(self, titles: Union[Iterable, None]) -> None:
        if titles is None:
            self._init_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        else:
            self._init_titles = tuple(titles)

    @property
    def zserie_init_titles(self) -> Union[None, Iterable]:
        return self._zserie_init_titles

    @zserie_init_titles.setter
    def zserie_init_titles(self, titles: Union[None, Iterable]) -> None:
        if titles is None:
            self._zserie_init_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        else:
            self._zserie_init_titles = titles

    @property
    def dark_titles(self) -> Union[None, Iterable]:
        return self._dark_titles

    @dark_titles.setter
    def dark_titles(self, titles: Union[None, Iterable]) -> None:
        if titles is None:
            self._dark_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        else:
            self._dark_titles = titles

    @property
    def flat_titles(self) -> Union[None, Iterable]:
        return self._flat_titles

    @flat_titles.setter
    def flat_titles(self, titles: Union[None, Iterable]) -> None:
        if titles is None:
            self._flat_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        else:
            self._flat_titles = titles

    @property
    def projections_titles(self) -> Union[None, Iterable]:
        return self._projection_titles

    @projections_titles.setter
    def projections_titles(self, titles: Union[None, Iterable]) -> None:
        if titles is None:
            self._projection_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        else:
            self._projection_titles = titles

    @property
    def alignment_titles(self) -> Union[None, Iterable]:
        return self._alignment_titles

    @alignment_titles.setter
    def alignment_titles(self, titles: Union[None, Iterable]) -> None:
        if titles is None:
            self._alignment_titles = None
        elif not isinstance(titles, Iterable):
            raise TypeError("'titles' should be None or an Iterable")
        else:
            self._alignment_titles = titles

    @property
    def x_pixel_size_paths(self) -> Iterable:
        return self._x_pixel_size_paths

    @x_pixel_size_paths.setter
    def x_pixel_size_paths(self, paths):
        if not isinstance(paths, Iterable):
            raise TypeError("'paths should be an Iterable")
        else:
            self._x_pixel_size_paths = paths

    @property
    def y_pixel_size_paths(self) -> Iterable:
        return self._y_pixel_size_paths

    @y_pixel_size_paths.setter
    def y_pixel_size_paths(self, paths):
        if not isinstance(paths, Iterable):
            raise TypeError("'paths should be an Iterable")
        else:
            self._y_pixel_size_paths = paths

    # frame type definition

    def _parse_frame_urls(self, urls: tuple):
        """
        Insure urls is None or a list of valid DataUrl
        """
        if urls in ("", None):
            return tuple()
        res = []
        for i_url, url in enumerate(urls):
            if isinstance(url, str):
                if url == "":
                    continue
                elif is_url_path(url):
                    url = DataUrl(path=url)
                else:
                    url = DataUrl(data_path=url, scheme="silx")
            if not isinstance(url, DataUrl):
                raise ValueError(
                    "urls tuple should contains DataUrl. "
                    "Not {} at index {}".format(type(url), i_url)
                )
            else:
                res.append(url)
        return tuple(res)

    @property
    def data_frame_grps(self) -> tuple:
        return self._data_grps_urls

    @data_frame_grps.setter
    def data_frame_grps(self, frame_grps: tuple):
        for frame_grp in frame_grps:
            if not isinstance(frame_grp, FrameGroup):
                raise TypeError(
                    "frame_grps is expected to contain only "
                    "instances of FrameGroup. Not {}"
                    "".format(type(frame_grp))
                )
        self._data_grps_urls = frame_grps

    @property
    def default_copy_behavior(self):
        return self._default_copy_behavior

    @default_copy_behavior.setter
    def default_copy_behavior(self, copy_: bool):
        if not isinstance(copy_, bool):
            raise TypeError("`copy_` should be a boolean")
        else:
            self._default_copy_behavior = copy_

    # parameters already defined

    @property
    def param_already_defined(self) -> dict:
        return self._param_already_defined

    @param_already_defined.setter
    def param_already_defined(self, params: dict):
        if not isinstance(params, dict):
            raise TypeError("dict expected")
        else:
            self._param_already_defined = params

    # utils functions

    @property
    def is_using_titles(self) -> bool:
        return not self.is_using_urls

    @property
    def is_using_urls(self) -> bool:
        """
        Return true if we want to use urls for darks, flats, projections
        instead of titles
        """
        return not (len(self.data_frame_grps) == 0)

    def clear_titles(self):
        """
        set all titles to empty tuple
        """
        self.dark_titles = tuple()
        self.flat_titles = tuple()
        self.projections_titles = tuple()
        self.alignment_titles = tuple()

    def clear_entries_and_subentries(self):
        """
        clear entries and sub_entries_to_ignore
        """
        self.entries = None
        self.sub_entries_to_ignore = None

    # to_dict / from_dict functions

    def to_dict(self) -> dict:
        """convert the configuration to a dictionary"""
        return {
            self.GENERAL_SECTION_DK: {
                self.OUTPUT_FILE_DK: self.output_file or "",
                self.INPUT_FILE_DK: self.input_file or "",
                self.OVERWRITE_DK: self.overwrite,
                self.FILE_EXTENSION_DK: self.file_extension.value,
                self.LOG_LEVEL_DK: logging.getLevelName(self.log_level).lower(),
                self.RAISES_ERROR_DK: self.raises_error,
                self.NO_INPUT_DK: self.no_input,
                self.SINGLE_FILE_DK: self.single_file,
                self.INPUT_FORMAT_DK: self.format.value if self.format else "",
                self.FIELD_OF_VIEW_DK: self.field_of_view.value
                if self.field_of_view
                else "",
            },
            self.KEYS_SECTION_DK: {
                HDF5Config.VALID_CAMERA_DK: self.valid_camera_names or "",
                HDF5Config.ROT_ANGLE_DK: self.rotation_angle_keys,
                HDF5Config.X_TRANS_KEYS_DK: self.x_trans_keys,
                HDF5Config.Y_TRANS_KEYS_DK: self.y_trans_keys,
                HDF5Config.Z_TRANS_KEYS_DK: self.z_trans_keys,
                HDF5Config.Y_ROT_KEYS_DK: self.y_rot_key,
                HDF5Config.DIODE_KEYS_DK: self.diode_keys,
                HDF5Config.ACQUISITION_EXPO_TIME_KEYS_DK: self.exposition_time_keys,
                HDF5Config.X_PIXEL_SIZE_KEYS_DK: self.x_pixel_size_paths,
                HDF5Config.Y_PIXEL_SIZE_KEYS_DK: self.y_pixel_size_paths,
            },
            self.ENTRIES_AND_TITLES_SECTION_DK: {
                HDF5Config.ENTRIES_DK: self.entries or "",
                HDF5Config.SUB_ENTRIES_TO_IGNORE: self.sub_entries_to_ignore or "",
                HDF5Config.INIT_TITLES_DK: self.init_titles or "",
                HDF5Config.ZSERIE_INIT_TITLES_DK: self.zserie_init_titles or "",
                HDF5Config.DARK_TITLES_DK: self.dark_titles or "",
                HDF5Config.REF_TITLES_DK: self.flat_titles or "",
                HDF5Config.PROJ_TITLES_DK: self.projections_titles or "",
                HDF5Config.ALIGNMENT_TITLES_DK: self.alignment_titles or "",
            },
            self.FRAME_TYPE_SECTION_DK: {
                HDF5Config.DATA_DK: FrameGroup.list_to_str(self.data_frame_grps),
                HDF5Config.DEFAULT_DATA_COPY_DK: self.default_copy_behavior,
            },
            self.EXTRA_PARAMS_SECTION_DK: self._param_already_defined,
        }

    @staticmethod
    def from_dict(dict_: dict):
        """
        Create a HDF5Config object and set it from values contained in the
        dictionary
        :param dict dict_: settings dictionary
        :return: HDF5Config
        """
        config = HDF5Config()
        config.load_from_dict(dict_)
        return config

    def load_from_dict(self, dict_: dict) -> None:
        """Load the configuration from a dictionary"""
        # general section
        if HDF5Config.GENERAL_SECTION_DK in dict_:
            self.load_general_section(dict_[HDF5Config.GENERAL_SECTION_DK])
        else:
            _logger.error("No {} section found".format(HDF5Config.GENERAL_SECTION_DK))

        # keys section
        if HDF5Config.KEYS_SECTION_DK in dict_:
            self.load_keys_section(dict_[HDF5Config.KEYS_SECTION_DK])
        else:
            mess = "No {} section found".format(HDF5Config.KEYS_SECTION_DK)
            if HDF5Config.ENTRIES_AND_TITLES_SECTION_DK not in dict_:
                _logger.error(mess)
            else:
                _logger.info(mess)

        # entries and titles section
        if HDF5Config.ENTRIES_AND_TITLES_SECTION_DK in dict_:
            self.load_entries_titles_section(
                dict_[HDF5Config.ENTRIES_AND_TITLES_SECTION_DK]
            )
        else:
            mess = "No {} section found".format(
                HDF5Config.ENTRIES_AND_TITLES_SECTION_DK
            )
            if HDF5Config.KEYS_SECTION_DK not in dict_:
                _logger.error(mess)
            else:
                _logger.info(mess)

        # frame type section
        if HDF5Config.FRAME_TYPE_SECTION_DK in dict_:
            self.load_frame_type_section(dict_[HDF5Config.FRAME_TYPE_SECTION_DK])
        else:
            _logger.error(
                "No {} section found".format(HDF5Config.FRAME_TYPE_SECTION_DK)
            )

        # extra params section
        if HDF5Config.EXTRA_PARAMS_SECTION_DK in dict_:
            self.load_extra_params_section(dict_[HDF5Config.EXTRA_PARAMS_SECTION_DK])
        else:
            _logger.error(
                "No {} section found".format(HDF5Config.EXTRA_PARAMS_SECTION_DK)
            )

    def load_general_section(self, dict_):
        def cast_bool(value):
            if isinstance(value, bool):
                return value
            elif isinstance(value, str):
                if value not in ("False", "True"):
                    raise ValueError("value should be 'True' or 'False'")
                return value == "True"
            else:
                raise TypeError("value should be a string")

        self.input_file = dict_.get(HDF5Config.INPUT_FILE_DK, None)
        self.output_file = dict_.get(HDF5Config.OUTPUT_FILE_DK, None)
        overwrite = dict_.get(HDF5Config.OVERWRITE_DK, None)
        if overwrite is not None:
            self.overwrite = cast_bool(overwrite)
        file_extension = dict_.get(HDF5Config.FILE_EXTENSION_DK, None)
        if file_extension is not None:
            self.file_extension = filter_str_def(file_extension)
        log_level = dict_.get(HDF5Config.LOG_LEVEL_DK, None)
        if log_level is not None:
            self.log_level = log_level
        raises_error = dict_.get(HDF5Config.RAISES_ERROR_DK, None)
        if raises_error is not None:
            self.raises_error = cast_bool(raises_error)
        no_input = dict_.get(HDF5Config.NO_INPUT_DK, None)
        if no_input is not None:
            self.no_input = cast_bool(no_input)
        single_file = dict_.get(HDF5Config.SINGLE_FILE_DK, None)
        if single_file is not None:
            self.single_file = cast_bool(single_file)
        input_format = dict_.get(HDF5Config.INPUT_FORMAT_DK, None)
        if input_format is not None:
            if input_format == "":
                input_format = None
            self.format = filter_str_def(input_format)
        field_of_view = dict_.get(HDF5Config.FIELD_OF_VIEW_DK, None)
        if field_of_view is not None:
            if field_of_view == "":
                field_of_view = None
            self.field_of_view = field_of_view

    def load_keys_section(self, dict_):
        # handle valid camera names. empty string is consider as a valid value
        valid_camera_names = dict_.get(HDF5Config.VALID_CAMERA_DK, None)
        if valid_camera_names == "":
            valid_camera_names = convert_str_to_tuple(
                valid_camera_names, none_if_empty=True
            )
            valid_camera_names = None
        self.valid_camera_names = valid_camera_names
        # handle rotation angles.
        rotation_angle_keys = dict_.get(HDF5Config.ROT_ANGLE_DK, None)
        if rotation_angle_keys is not None:
            rotation_angle_keys = convert_str_to_tuple(
                rotation_angle_keys, none_if_empty=True
            )
            self.rotation_angle_keys = rotation_angle_keys
        # handle x translation
        x_trans_keys = dict_.get(HDF5Config.X_TRANS_KEYS_DK, None)
        if x_trans_keys is not None:
            x_trans_keys = convert_str_to_tuple(x_trans_keys, none_if_empty=True)
            self.x_trans_keys = x_trans_keys
        # handle y translation
        y_trans_keys = dict_.get(HDF5Config.Y_TRANS_KEYS_DK, None)
        if y_trans_keys is not None:
            y_trans_keys = convert_str_to_tuple(y_trans_keys, none_if_empty=True)
            self.y_trans_keys = y_trans_keys
        # handle z translation
        z_trans_keys = dict_.get(HDF5Config.Z_TRANS_KEYS_DK, None)
        if z_trans_keys is not None:
            z_trans_keys = convert_str_to_tuple(z_trans_keys, none_if_empty=True)
            self.z_trans_keys = z_trans_keys
        # handle y rotation keys
        y_rot_key = dict_.get(HDF5Config.Y_ROT_KEYS_DK, None)
        if y_rot_key is not None:
            self.y_rot_key = y_rot_key
        # handle diode keys
        diode_keys = dict_.get(HDF5Config.DIODE_KEYS_DK, None)
        if diode_keys is not None:
            diode_keys = convert_str_to_tuple(diode_keys, none_if_empty=True)
            self.diode_keys = diode_keys
        # handle exposure time
        exposition_time_keys = dict_.get(HDF5Config.ACQUISITION_EXPO_TIME_KEYS_DK, None)
        if exposition_time_keys is not None:
            exposition_time_keys = convert_str_to_tuple(
                exposition_time_keys, none_if_empty=True
            )
            self.exposition_time_keys = exposition_time_keys
        # handle x pixel paths
        x_pixel_size_paths = dict_.get(HDF5Config.X_PIXEL_SIZE_KEYS_DK, None)
        if x_pixel_size_paths is not None:
            x_pixel_size_paths = convert_str_to_tuple(
                x_pixel_size_paths, none_if_empty=True
            )
            self.x_pixel_size_paths = x_pixel_size_paths
        # handle y pixel paths
        y_pixel_size_paths = dict_.get(HDF5Config.Y_PIXEL_SIZE_KEYS_DK, None)
        if y_pixel_size_paths is not None:
            y_pixel_size_paths = convert_str_to_tuple(
                y_pixel_size_paths, none_if_empty=True
            )
            self.y_pixel_size_paths = y_pixel_size_paths

    def load_entries_titles_section(self, dict_):
        # handle entries to convert
        entries = dict_.get(HDF5Config.ENTRIES_DK)
        if entries is not None:
            entries = convert_str_to_tuple(entries, none_if_empty=True)
            self.entries = entries
        # handle init titles. empty string is consider as a valid value
        init_titles = dict_.get(HDF5Config.INIT_TITLES_DK, None)
        if init_titles is not None:
            init_titles = convert_str_to_tuple(init_titles, none_if_empty=True)
            self.init_titles = init_titles
        # handle zserie init titles. empty string is consider as a valid value
        zserie_init_titles = dict_.get(HDF5Config.ZSERIE_INIT_TITLES_DK, None)
        if zserie_init_titles is not None:
            zserie_init_titles = convert_str_to_tuple(
                zserie_init_titles, none_if_empty=True
            )
            self.zserie_init_titles = zserie_init_titles
        # handle dark titles. empty string is consider as a valid value
        dark_titles = dict_.get(HDF5Config.DARK_TITLES_DK, None)
        if dark_titles is not None:
            dark_titles = convert_str_to_tuple(dark_titles, none_if_empty=True)
            self.dark_titles = dark_titles
        # handle ref titles. empty string is consider as a valid value
        flat_titles = dict_.get(HDF5Config.REF_TITLES_DK, None)
        if flat_titles is not None:
            flat_titles = convert_str_to_tuple(flat_titles, none_if_empty=True)
            self.flat_titles = flat_titles
        # handle projection titles. empty string is consider as a valid value
        proj_titles = dict_.get(HDF5Config.PROJ_TITLES_DK, None)
        if proj_titles is not None:
            proj_titles = convert_str_to_tuple(proj_titles, none_if_empty=True)
            self.projections_titles = proj_titles
        # handle alignment titles. empty string is consider as a valid value
        alignment_titles = dict_.get(HDF5Config.ALIGNMENT_TITLES_DK, None)
        if alignment_titles is not None:
            alignment_titles = convert_str_to_tuple(
                alignment_titles, none_if_empty=True
            )
            self.alignment_titles = alignment_titles

    def load_frame_type_section(self, dict_):
        # urls
        data_urls = dict_.get(HDF5Config.DATA_DK, None)
        if data_urls is not None:
            data_urls = convert_str_to_frame_grp(data_urls)
            self.data_frame_grps = data_urls
        default_copy_behavior = dict_.get(HDF5Config.DEFAULT_DATA_COPY_DK, None)
        if default_copy_behavior is not None:
            self.default_copy_behavior = default_copy_behavior == "True"

    def load_extra_params_section(self, dict_):
        for key, value in dict_.items():
            if key in HDF5Config.EXTRA_PARAMS_ENERGY_VALID_KEYS:
                self._param_already_defined.update(
                    {
                        key: value,
                    }
                )
            else:
                _logger.warning("{} is not a key handled".format(key))

    def to_cfg_file(self, file_path: str):
        # TODO: add some generic information like:provided order of the tuple
        # will be the effective one. You can provide a key from it names if
        # it is contained in the positioners group
        # maybe split in sub section ?
        self.dict_to_cfg(file_path=file_path, dict_=self.to_dict())

    @staticmethod
    def dict_to_cfg(file_path, dict_):
        """"""
        if not file_path.lower().endswith((".cfg", ".config")):
            _logger.warning("add a valid extension to the output file")
            file_path += ".cfg"
        config = configparser.ConfigParser(allow_no_value=True)
        for section_name, values in dict_.items():
            config.add_section(section_name)
            config.set(section_name, "# " + HDF5Config.get_comments(section_name), None)
            for key, value in values.items():
                # adopt nabu design: comments are set prior to the key
                config.set(section_name, "# " + HDF5Config.get_comments(key), None)
                config.set(section_name, key, str(value))

        with open(file_path, "w") as config_file:
            config.write(config_file)

    @staticmethod
    def from_cfg_file(file_path: str, encoding=None):
        config_parser = configparser.ConfigParser(allow_no_value=True)
        config_parser.read(file_path, encoding=encoding)
        return HDF5Config.from_dict(config_parser)

    @staticmethod
    def get_comments(key):
        return HDF5Config.COMMENTS[key]

    def __str__(self):
        return str(self.to_dict())


def generate_default_h5_config() -> dict:
    """generate a default configuration for converting hdf5 to nx"""
    return HDF5Config().to_dict()
