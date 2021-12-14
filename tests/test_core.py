import cv2
import unittest

from sheets.core import (
    find_numbers, find_holes, find_reasonable_opening,
    guess_resolution
    )

class TestCore(unittest.TestCase):

    def test_finding_numbers(self):
        im = cv2.imread(r"tests/stockpile.png")
        rects = find_numbers(im)

        self.assertGreater(len(rects), 0)
        self.assertEqual(len(rects), 54)

    def test_finding_numbers_1440(self):
        im = cv2.imread(r"tests/sp_1440.png")
        rects = find_numbers(im)

        self.assertGreater(len(rects), 0)
        self.assertEqual(len(rects), 10)

    def test_finding_numbers_noisy(self):
        im = cv2.imread(r"tests/sp_noise.png")
        rects = find_numbers(im)

        self.assertGreater(len(rects), 0)
        self.assertEqual(len(rects), 85)

    def test_find_opening(self):
        im = cv2.imread(r"tests/sp_noise.png")
        holes, opening = find_holes(im, 50, 105)

        x,y = find_reasonable_opening(holes)

        self.assertEqual(holes[x,y], 0)

    def test_guess_resolution_1080(self):
        im = cv2.imread(r"tests/sp_noise.png")
        resolution = guess_resolution(im)

        self.assertEqual(resolution, "1920x1080")

    def test_guess_resolution_1440(self):
        im = cv2.imread(r"tests/sp_1440.png")
        resolution = guess_resolution(im)

        self.assertEqual(resolution, "2560x1440")