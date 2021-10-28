import cv2
import json
import unittest

from sheets.core import ocr

class TestOCR(unittest.TestCase):

    def test_ocr_238(self):
        with open("nums.json", "r") as f:
            identities = json.load(f)
        im = cv2.imread("tests/238.png")
        val = ocr(im, identities)

        self.assertEqual(val, "238")

    def test_ocr_771(self):
        with open("nums.json", "r") as f:
            identities = json.load(f)
        im = cv2.imread("tests/771.png")
        val = ocr(im, identities)

        self.assertEqual(val, "771")

    def test_chars(self):
        with open("nums.json", "r") as f:
            identities = json.load(f)

        self.assertEqual(len(identities), 12)
        self.assertIn("0", identities)
        self.assertIn("1", identities)
        self.assertIn("2", identities)
        self.assertIn("3", identities)
        self.assertIn("4", identities)
        self.assertIn("5", identities)
        self.assertIn("6", identities)
        self.assertIn("7", identities)
        self.assertIn("8", identities)
        self.assertIn("9", identities)
        self.assertIn("k", identities)
        self.assertIn("+", identities)
        