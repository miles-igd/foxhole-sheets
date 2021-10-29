import cv2
import unittest

from sheets.core import process

class TestData(unittest.TestCase):

    def test_data_gammas(self):
        im_mid = cv2.imread(r"tests/sp_mid_gamma.png")
        im_max = cv2.imread(r"tests/sp_max_gamma.png")

        data_mid = process(im_mid)[0]
        data_max = process(im_max)[0]

        self.assertGreater(len(data_mid), 0)
        self.assertEqual(data_mid, data_max)

    def test_data_different(self):
        print("tests/sp1.png")

        im1 = cv2.imread(r"tests/sp1.png")
        im2 = cv2.imread(r"tests/sp2.png")

        data1 = process(im1)[0]
        data2 = process(im2)[0]

        self.assertGreater(len(data1), 0)
        self.assertNotEqual(data1, data2)