import cv2
import unittest

from sheets.core import process

class TestData(unittest.TestCase):

    def test_data_gammas(self):
        im_mid = cv2.imread(r"tests/sp_mid_gamma.png")
        im_max = cv2.imread(r"tests/sp_max_gamma.png")

        data_mid, _ = process(im_mid)
        data_max, _ = process(im_max)

        self.assertGreater(len(data_mid), 0)
        self.assertEqual(data_mid, data_max)

    def test_data_different(self):
        print("tests/sp1.png")

        im1 = cv2.imread(r"tests/sp1.png")
        im2 = cv2.imread(r"tests/sp2.png")

        data1, _ = process(im1)
        data2, _ = process(im2)

        self.assertGreater(len(data1), 0)
        self.assertNotEqual(data1, data2)