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
from nxtomomill.io import utils
from nxtomomill.io.framegroup import FrameGroup


class TestConvertStrToTuple(unittest.TestCase):
    """
    test convert_str_to_tuple function
    """

    def testStr1(self):
        self.assertEqual(utils.convert_str_to_tuple("toto, tata"), ("toto", "tata"))

    def testStr2(self):
        self.assertEqual(
            utils.convert_str_to_tuple("'toto', \"tata\""), ("toto", "tata")
        )

    def testStr3(self):
        self.assertEqual(utils.convert_str_to_tuple("test"), ("test",))

    def testStr4(self):
        self.assertEqual(
            utils.convert_str_to_tuple("(this is a test)"), ("this is a test",)
        )

    def testStr5(self):
        self.assertEqual(
            utils.convert_str_to_tuple("(this is a test, 'and another one')"),
            ("this is a test", "and another one"),
        )


class TestIsUrlPath(unittest.TestCase):
    """test the is_url function"""

    def test_invalid_url_1(self):
        self.assertFalse(utils.is_url_path("/toto/tata"))

    def test_invalid_url_2(self):
        self.assertFalse(utils.is_url_path("tata"))

    def test_valid_url_1(self):
        self.assertTrue(utils.is_url_path("silx:///data/image.h5?path=/scan_0/data"))

    def test_valid_url_2(self):
        self.assertTrue(utils.is_url_path("silx:///data/image.edf"))

    def test_valid_url_3(self):
        self.assertTrue(utils.is_url_path("silx://image.h5"))

    def test_valid_url_4(self):
        self.assertTrue(
            utils.is_url_path("silx:///data/image.h5?path=/scan_0/data&slice=1,5")
        )


class TestConvertStrToFrameGrp(unittest.TestCase):
    """
    test the `convert_str_to_frame_grp` function
    """

    def test_valid_1(self):
        dg1 = FrameGroup(
            frame_type="dark", url="silx:///file.h5?data_path=/dark", copy=True
        )
        dg2 = FrameGroup(
            frame_type="flat", url="silx:///file.h5?data_path=/flat", copy=True
        )
        dg3 = FrameGroup(
            frame_type="projection",
            url="silx:///file.h5?data_path=/projection1",
            copy=True,
        )
        dg4 = FrameGroup(
            frame_type="alignment",
            url="silx:///file.h5?data_path=/projection2",
            copy=True,
        )

        my_str = "({dg1}, {dg2}, {dg3}, {dg4}, )".format(
            dg1=dg1, dg2=dg2, dg3=dg3, dg4=dg4
        )
        frame_grps = utils.convert_str_to_frame_grp(my_str)
        self.assertTrue(isinstance(frame_grps, tuple))
        self.assertTrue(len(frame_grps) == 4)
        for o_fg, i_fg in zip((dg1, dg2, dg3, dg4), frame_grps):
            self.assertEqual(str(o_fg), str(i_fg))

    def test_valid_2(self):
        pass

    def test_invalid_1(self):
        pass


def suite():
    test_suite = unittest.TestSuite()
    for ui in (TestConvertStrToTuple, TestIsUrlPath):
        test_suite.addTest(unittest.defaultTestLoader.loadTestsFromTestCase(ui))
    return test_suite


if __name__ == "__main__":
    unittest.main(defaultTest="suite")
