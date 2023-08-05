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
contains the FrameGroup
"""

__authors__ = [
    "H. Payno",
]
__license__ = "MIT"
__date__ = "17/03/2021"


from silx.io.url import DataUrl
from typing import Union
from .acquisitionstep import AcquisitionStep
from silx.utils.enum import Enum as _Enum
from typing import Iterable
import logging

_logger = logging.getLogger(__name__)


class FrameGroup:
    """class used to store information regarding a group of frame

    contains the frames type and if we should provide a copy of those in the
    outputfile or not

    :param url: url to access the frame group (bliss scan entry)
    :type url: None, str, DataUrl. If provided as a string should fit a DataUrl
               or be the data path on the input file
    :param frame_type: frame type (dark, projection ...)
    :type param_type: AcquisitionStep, str. If provided as str should be
                      an AcquisitionStep value
    :param copy: should we copy the dataframe in the output file
    :type copy: bool, None. If set to None then the value will be set to
                the default copy behavior during processing
    """

    class Info(_Enum):
        FRAME_TYPE = "frame_type"
        URL_ENTRY = "entry"
        COPY = "copy"

    def __init__(
        self,
        url: Union[DataUrl, str, None],
        frame_type: [AcquisitionStep, str],
        copy: Union[bool, None] = None,
    ):
        self._url = None
        self._frame_type = None
        self._copy = None
        self._frames_url = None

        self.url = url
        self.frame_type = frame_type
        self.copy = copy

    @property
    def copy(self) -> Union[bool, None]:
        return self._copy

    @copy.setter
    def copy(self, copy: bool):
        if not isinstance(copy, (bool, type(None))):
            raise TypeError("copy should be a bool and not {}" "".format(type(copy)))
        else:
            self._copy = copy

    @property
    def frame_type(self) -> AcquisitionStep:
        return self._frame_type

    @frame_type.setter
    def frame_type(self, frame_type: Union[str, int, AcquisitionStep]):
        self._frame_type = AcquisitionStep.from_value(frame_type)

    @property
    def url(self) -> Union[DataUrl, None]:
        return self._url

    @url.setter
    def url(self, url: Union[DataUrl, str]):
        if isinstance(url, str):
            from nxtomomill.io.utils import is_url_path

            # handle if the string path is not a "full url" then we consider
            # this is only the data path.
            self._url = DataUrl(path=url)
            # small hack. As the url constructor is not able to distinguish
            # between the data_path or the file_path and set the file path
            # on our cases we support empty file path ( in this case we
            # consider this is the input file) but not empty dataset
            if self._url.data_path() is None and self._url.file_path() is not None:
                self._url = DataUrl(
                    file_path=None,
                    data_path=self._url.file_path(),
                    scheme=self._url.scheme(),
                )
        elif isinstance(url, (DataUrl, type(None))):
            self._url = url
        else:
            raise TypeError(
                "url should be a str or a DataUrl not {}" "".format(type(url))
            )

    def __str__(self) -> str:
        return self.str_representation(
            only_data_path=False, with_copy=True, with_prefix_key=True
        )

    def str_representation(
        self, only_data_path: bool, with_copy: bool, with_prefix_key: bool
    ) -> str:
        """
        Util function to print the possible input string for this FrameGroup.

        :param only_data_path: if True consider the input file frame group is
                               contained in the input file and the string
                               representing the url can be only the data path
        :type only_data_path: bool
        :param with_copy: if true display the copy information
        :type with_copy: bool
        :param with_prefix_key: if true provide the string with the keys as
                                prefix (frame_type=XXX, copy=...)
        :type with_prefix_key: bool

        :rtype: str
        """
        if self.url is None:
            url_str = ""
        elif only_data_path:
            url_str = self.url.data_path()
        else:
            url_str = self.url.path()
        if self.copy is None:
            with_copy = False
        if with_prefix_key:
            if with_copy:
                return "({ft_key}={frame_type}, {url_key}={url}, {copy_key}={copy})".format(
                    ft_key=self.Info.FRAME_TYPE.value,
                    frame_type=self.frame_type.value,
                    url_key=self.Info.URL_ENTRY.value,
                    url=url_str,
                    copy_key=self.Info.COPY.value,
                    copy=self.copy,
                )
            else:
                return "({ft_key}={frame_type}, {url_key}={url})".format(
                    ft_key=self.Info.FRAME_TYPE.value,
                    frame_type=self.frame_type.value,
                    url_key=self.Info.URL_ENTRY.value,
                    url=url_str,
                )
        else:
            if with_copy:
                return "({frame_type}, {url}, {copy})".format(
                    frame_type=self.frame_type.value,
                    url=url_str,
                    copy=self.copy,
                )
            else:
                return "({frame_type}, {url})".format(
                    frame_type=self.frame_type.value,
                    url=url_str,
                )

    @staticmethod
    def list_to_str(urls: Iterable):
        """Convert the list of urls to a string that can be pass
        to the .cfg file"""
        if len(urls) == 0:
            return ""
        else:
            urls_str = ",\n".join(["{}".format(str(url)) for url in urls])
            return """(
{}
)           
            """.format(
                urls_str
            )

    @staticmethod
    def frm_str(input_str: str):
        """
        Create an instance of FrameGroup from it string representation.
        """
        if not isinstance(input_str, str):
            raise TypeError("input_str should be a string".format(input_str))

        from nxtomomill.io.utils import (
            remove_parenthesis_or_brackets,
        )  # avoid cyclic import
        from nxtomomill.io.utils import filter_str_def  # avoid cyclic import

        def add_info(info_type, value):
            if info_type in cst_inputs:
                err = "{} is provided twice: {} and {}".format(
                    info_type.value, value, cst_inputs[info_type]
                )
                raise ValueError(err)
            else:
                cst_inputs[info_type] = value

        input_str = remove_parenthesis_or_brackets(input_str)
        elmts = input_str.split(",")
        elmts = [elmt.lstrip(" ").rstrip(" ") for elmt in elmts]

        cst_inputs = {}

        def treat_elmt(elmt):
            assert isinstance(elmt, str)
            # first try to get elements from the "INFO=" format
            for info in FrameGroup.Info.members():
                key = "{}=".format(info.value)
                if elmt.startswith(key):
                    add_info(
                        info_type=info, value=filter_str_def(elmt.replace(key, "", 1))
                    )
                    return
            # else try to convert them according to the type
            # is this an acquisition step
            elmt = filter_str_def(elmt)
            try:
                acquisition_step = AcquisitionStep.from_value(elmt)
            except ValueError:
                pass
            else:
                add_info(info_type=FrameGroup.Info.FRAME_TYPE, value=acquisition_step)
                return

            # is this a copy element
            if elmt in ("True", "False"):
                add_info(info_type=FrameGroup.Info.COPY, value=elmt)
                return

            try:
                elmt = filter_str_def(elmt)
                DataUrl(path=elmt)
            except Exception:
                pass
            else:
                add_info(info_type=FrameGroup.Info.URL_ENTRY, value=elmt)
                return

            url_example = DataUrl(
                file_path="/path/to/my/file/file.h5",
                data_path="/data/path",
                scheme="h5py",
            )
            err_msg = (
                "Unable to interpret string. Please insure this is a "
                "either a frame type, a boolean for copy or an entry "
                "(DataUrl).\n "
                "Please prefix the value by the information type like: "
                "{}. Invalid element is {}".format(
                    FrameGroup(url=url_example, copy=True, frame_type="projection"),
                    input_str,
                )
            )
            raise ValueError(err_msg)

        [treat_elmt(elmt) for elmt in elmts]

        # insure we have at least the frame type and the DataUrl
        inputs = {}
        if FrameGroup.Info.FRAME_TYPE not in cst_inputs:
            raise ValueError("Unable to find frame type from {}".format(input_str))
        else:
            inputs["frame_type"] = cst_inputs[FrameGroup.Info.FRAME_TYPE]
        if FrameGroup.Info.URL_ENTRY not in cst_inputs:
            raise ValueError("Unable to find entry from {}".format(input_str))
        else:
            inputs["url"] = cst_inputs[FrameGroup.Info.URL_ENTRY]
        if FrameGroup.Info.COPY in cst_inputs:
            inputs["copy"] = cst_inputs[FrameGroup.Info.COPY]

        if "copy" in inputs and inputs["copy"] in ("True", "False"):
            inputs["copy"] = inputs["copy"] == "True"

        return FrameGroup(**inputs)


def filter_acqui_frame_type(
    init: FrameGroup, sequences: tuple, frame_type: AcquisitionStep
) -> tuple:
    """compute the list of urls representing projections
    from init until the next Initialization step

    :param FrameGroup init: frame group creating the beginning of the
                            acquisition sequence
    :param tuple sequences: list of FrameGroup representing the sequence
    :param AcquisitionStep frame_type: type of frame to filer (cannot be Initialization step)
    """
    frame_type = AcquisitionStep.from_value(frame_type)
    if frame_type is AcquisitionStep.INITIALIZATION:
        raise ValueError("{} is not handled".format(AcquisitionStep.INITIALIZATION))
    if init not in sequences:
        raise ValueError("{} cannot be find in the provided sequence".format(init))

    frame_types = [frm_grp.frame_type for frm_grp in sequences]
    current_acqui_idx = sequences.index(init)
    if len(sequences) == current_acqui_idx - 1:
        # in case the initialization sequence is the last element of the
        # sequence (if people make strange stuff...)
        return ()
    sequence_target = sequences[current_acqui_idx + 1 :]
    frame_types = frame_types[current_acqui_idx + 1 :]
    try:
        next_acqui = frame_types.index(AcquisitionStep.INITIALIZATION) - 1
    except ValueError as e:
        next_acqui = -1
    sequence_target = sequence_target[:next_acqui]
    filter_fct = lambda a: a.frame_type is frame_type
    return tuple(filter(filter_fct, sequence_target))
