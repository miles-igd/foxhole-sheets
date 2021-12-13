import cv2
import json
import numpy as np

def convert_nums():
    with open("Data/nums.json", 'r') as f:
        nums = json.load(f)

    for num, value in nums.items():
        arr = np.array(value)
        cv2.imwrite(f"Data/Numbers/{num}.png", arr)

if __name__ == "__main__":
    convert_nums()