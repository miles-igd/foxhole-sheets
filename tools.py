import cv2
import json
import numpy as np

from sheets.core import find_numbers, ident_nums, guess_resolution

def convert_nums():
    with open("Data/nums.json", 'r') as f:
        nums = json.load(f)

    for num, value in nums.items():
        arr = np.array(value)
        cv2.imwrite(f"Data/Numbers/{num}.png", arr)

def save_nums():
    im = cv2.imread("screens/high2.png")
    cv2.imshow("tools", im)
    cv2.waitKey()

    resolution = guess_resolution(im)
    rects = find_numbers(im)

    ident_nums(rects, im, resolution=resolution)


if __name__ == "__main__":
    save_nums()