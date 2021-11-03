import cv2
import json
import unittest

from sheets.stockpile import Stockpile

class TestData(unittest.TestCase):

    def test_data_gammas(self):
        im_mid = cv2.imread(r"tests/sp_mid_gamma.png")
        im_max = cv2.imread(r"tests/sp_max_gamma.png")

        sp_mid_gamma = Stockpile(im_mid)
        sp_max_gamma = Stockpile(im_max)

        print(sp_mid_gamma)

        self.assertGreater(len(sp_mid_gamma.data), 0)
        self.assertEqual(sp_mid_gamma.data,sp_max_gamma.data)

    def test_data_different(self):
        im1 = cv2.imread(r"tests/sp1.png")
        im2 = cv2.imread(r"tests/sp2.png")

        sp1 = Stockpile(im1)
        sp2 = Stockpile(im2)

        self.assertGreater(len(sp1.data), 0)
        self.assertNotEqual(sp1.data, sp2.data)

    def test_data(self):
        im = cv2.imread(r"tests/stockpile.png")
        stockpile = Stockpile(im)

        with open("tests/stockpile.json", "r") as json_file:
            data = json.load(json_file)

        self.assertGreater(len(stockpile.data), 0)
        self.assertEqual(stockpile.data, data)