# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
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

__authors__ = ["H. Payno"]
__license__ = "MIT"
__date__ = "10/03/2021"


import unittest
from nxtomomill.io.framegroup import FrameGroup
from nxtomomill.io.framegroup import filter_acqui_frame_type
from silx.io.url import DataUrl
from nxtomomill.io.acquisitionstep import AcquisitionStep


class TestFrameGroupCreator(unittest.TestCase):
    """Test FrameGroup class"""

    def setUp(self) -> None:
        self.url1 = DataUrl(
            file_path="/path/to/file/my_file", data_path="/path/to/data", scheme="silx"
        )
        self.url2 = DataUrl(file_path="my_file", data_path="/path/to/data")

    def test_default_constructor(self):
        """Test FrameGroup constructor"""
        frame_grp = FrameGroup(url=self.url1, frame_type="projection")
        self.assertEqual(frame_grp.url.path(), self.url1.path())
        self.assertEqual(frame_grp.frame_type, AcquisitionStep.PROJECTION)

        frame_grp = FrameGroup(url=self.url2, frame_type=AcquisitionStep.ALIGNMENT)
        self.assertEqual(frame_grp.url.path(), self.url2.path())
        self.assertEqual(frame_grp.frame_type, AcquisitionStep.ALIGNMENT)

        with self.assertRaises(ValueError):
            FrameGroup(url=self.url1, frame_type="toto")

        with self.assertRaises(TypeError):
            FrameGroup(url=self.url1, frame_type="projection", copy="tata")

    def test_constructor_frm_str(self):
        """Test FrameGroup.frm_str function"""
        frame_grp = FrameGroup(url=self.url1, frame_type="projection")
        frame_grp_frm_str = FrameGroup.frm_str(str(frame_grp))
        self.assertEqual(str(frame_grp), str(frame_grp_frm_str))

        grp_prefix = FrameGroup.frm_str(
            "frame_type=projections, "
            "entry=silx:///path/to/file/my_file?/path/to/data, "
            "copy=True"
        )
        self.assertTrue(isinstance(grp_prefix, FrameGroup))
        self.assertEqual(grp_prefix.copy, True)

        grp_no_prefix = FrameGroup.frm_str(
            "projections, silx:///path/to/file/my_file?/path/to/data, True"
        )
        self.assertEqual(str(grp_no_prefix), str(grp_prefix))

        with self.assertRaises(TypeError):
            FrameGroup.frm_str(
                "frame_type=projections, "
                "entry=silx:///path/to/file/my_file?/path/to/data, "
                "copy=12"
            )

        with self.assertRaises(ValueError):
            FrameGroup.frm_str("frame_type=projections")


class TestFilterCurrentAcquiFrameType(unittest.TestCase):
    """test filter_acqui_frame_type function"""

    def setUp(self) -> None:
        self.init_1 = FrameGroup(frame_type="init", url=None)
        self.sequence1 = (
            self.init_1,
            FrameGroup(frame_type="dark", url="data/to/dark/1"),
            FrameGroup(frame_type="flat", url="data/to/flat/1"),
            FrameGroup(frame_type="proj", url="data/to/proj/1"),
            FrameGroup(frame_type="proj", url="data/to/proj/2"),
        )

        self.init_2 = FrameGroup(frame_type="init", url="/path/to/init")
        self.sequence2 = (
            self.init_2,
            FrameGroup(frame_type="dark", url="data/to/dark/2"),
            FrameGroup(frame_type="proj", url="data/to/proj/3"),
            FrameGroup(frame_type="proj", url="data/to/proj/4"),
            FrameGroup(frame_type="proj", url="data/to/proj/5"),
            FrameGroup(frame_type="proj", url="data/to/proj/6"),
            FrameGroup(frame_type="flat", url="data/to/flat/2"),
            FrameGroup(frame_type="alignment", url="data/to/alignment/1"),
        )

    def test_search_init(self):
        """test filter_acqui_frame_type with init frame group"""
        with self.assertRaises(ValueError):
            filter_acqui_frame_type(
                init=self.init_1,
                sequences=self.sequence1,
                frame_type=AcquisitionStep.INITIALIZATION,
            )

    def test_search_flat(self):
        """test filter_acqui_frame_type with flat frame group"""
        flat_url = filter_acqui_frame_type(
            init=self.init_1,
            sequences=self.sequence1,
            frame_type=AcquisitionStep.REFERENCE,
        )
        self.assertEqual(len(flat_url), 1)
        self.assertEqual(flat_url[0].url.path(), self.sequence1[2].url.path())

        with self.assertRaises(ValueError):
            filter_acqui_frame_type(
                init=self.init_1,
                sequences=self.sequence2,
                frame_type=AcquisitionStep.REFERENCE,
            )

    def test_search_dark(self):
        """test filter_acqui_frame_type with dark frame group"""
        seq_sum = list(self.sequence1)
        seq_sum.extend(self.sequence2)
        dark_1 = filter_acqui_frame_type(
            init=self.init_1, sequences=tuple(seq_sum), frame_type=AcquisitionStep.DARK
        )
        self.assertEqual(len(dark_1), 1)
        self.assertEqual(dark_1[0].url.path(), self.sequence1[1].url.path())
        dark_2 = filter_acqui_frame_type(
            init=self.init_2, sequences=tuple(seq_sum), frame_type=AcquisitionStep.DARK
        )
        self.assertEqual(len(dark_2), 1)
        self.assertEqual(dark_2[0].url.path(), self.sequence2[1].url.path())

    def test_search_proj(self):
        """test filter_acqui_frame_type with projection frame group"""
        projs_1 = filter_acqui_frame_type(
            init=self.init_2,
            sequences=self.sequence2,
            frame_type=AcquisitionStep.PROJECTION,
        )
        self.assertEqual(len(projs_1), 4)
        self.assertEqual(projs_1[2].url.path(), self.sequence2[4].url.path())

        seq_sum = list(self.sequence1)
        seq_sum.extend(self.sequence2)
        projs_2 = filter_acqui_frame_type(
            init=self.init_2,
            sequences=tuple(seq_sum),
            frame_type=AcquisitionStep.PROJECTION,
        )
        self.assertEqual(len(projs_2), 4)
        self.assertEqual(projs_1[1].url.path(), projs_2[1].url.path())


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestFrameGroupCreator, TestFilterCurrentAcquiFrameType):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
