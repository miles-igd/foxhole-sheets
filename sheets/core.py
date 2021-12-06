import cv2
import io
import json
import numpy as np
import os
import random
import logging


from sheets.ident import ident_item, ident_num

DEBUG = False

def find_numbers(im, low_threshold=50, high_threshold=105):
    '''
    Finds rectangles on a cv2 np.ndarray given the expected values of the grey boxes in a Foxhole stockpile.
    '''
    assert type(im) == np.ndarray

    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(im_gray, low_threshold, high_threshold)

    kernel = np.ones((4,4),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    holes = opening.copy()
    starting = find_reasonable_opening(holes)

    cv2.floodFill(holes, None, starting, 255)

    opening[np.where(holes==0)] = 255
    result = cv2.bitwise_and(im, im, mask = opening)

    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.convexHull(contour) for contour in contours]

    return rects

def find_reasonable_opening(holes, window=11, limit=9):
    '''
    introduces randomness into algorithm, consider reconsidering
    if a test fails sometimes, check here
    '''
    w,h=holes.shape
    for i in range(limit):
        x=random.randint(0,w)
        y=random.randint(0,h)
        logging.info(f"Trying to flood fill at ({y},{x})")

        if np.sum(holes[x:x+window,y:y+window]) == 0:
            return (y,x)
        else:
            logging.info("Failed")

    return (22,22)

def find_icons(num_rects):
    return [rect-np.array([49,0]) for rect in num_rects]

def ident_items(icons, im):
    '''
    Prompts the user to identify an icon, given a stockpile image and a list of np.ndarray (rectangles).
    It will save the icon into the folder Icons\\
    '''
    for icon in icons:
        x,y,w,h = cv2.boundingRect(icon)
        ident_icon = prepare_item(im[y:y+h,x:x+w].copy())
        ident_item(ident_icon, output="Data\\Icons\\")

def prepare_icon(ident_icon):
    '''
    Returns a thresholded version of a cv2 np.ndarray ident_icon.
    This mitigates noise and artifacts on the image.
    '''
    ident_icon = cv2.cvtColor(ident_icon, cv2.COLOR_BGR2GRAY)
    _, ident_icon = cv2.threshold(ident_icon, 144, 255, cv2.THRESH_BINARY)

    return ident_icon

def match_item(icon_image, icon_identities, metric=lambda x, y: ((x-y)**2).mean(), order=min, **kwargs):
    '''
    Brute-force matching of an icon with all the icons in arrs.
    metric arg expects an image similarity metric, default is mean-squared error.
    order arg expects min or max, depending on how the metric is calculated.
    kwargs expects any kwarg used in metric.
    '''
    if len(icon_identities) == 0:
        return None, None

    distances = [metric(icon_image, icon_array, **kwargs) for icon_array in icon_identities]
    min_err = order(distances)
    return min_err, distances.index(min_err)

def load_icons(folder_path = "Data\\Icons\\"):
    '''
    loads the icons from folder_path or Icons\\ into memory as cv2 np.ndarrays
    '''
    files = os.listdir(folder_path) 
    icons = {os.path.basename(f): cv2.imread(folder_path + f, cv2.IMREAD_GRAYSCALE) for f in files}
    
    return icons

def ocr(im, identities):
    '''
    Brute-force matching of numbers to its identity, which is determined beforehand.
    '''
    rects, thresh, original = prepare_nums(im)
    digits = []
    nums = dict()

    for x,y,w,h in rects:
        num = original[y:y+h,x:x+w].copy()
        num = cv2.resize(num, (32, 32), interpolation = cv2.INTER_NEAREST)
        
        for i, identity in identities.items():
            nums[i] = ((identity - num)**2).mean()

        match = min(nums, key=nums.get)
        digits.append(match)
    
    return "".join(digits)

def prepare_nums(im):
    '''
    Takes an input of a cv2 np.ndarray and returns a list of rectangles
    locating where the digits are on the image.
    '''
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    ret, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    width = int(thresh.shape[1] * 3)
    height = int(thresh.shape[0] * 3)
    dim = (width, height)

    thresh = cv2.resize(thresh, dim, interpolation = cv2.INTER_NEAREST)
    holes = thresh.copy()
    cv2.floodFill(holes, None, (0, 0), 255)

    original = thresh.copy()
    thresh[np.where(holes==0)] = 255
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.boundingRect(contour) for contour in contours]

    return sorted(rects, key = lambda x: x[0]), thresh, original

def ident_nums(rects, im, output="Data\\nums.json", save=True):
    '''
    Prompts the user to identify a number,
    It will save the numbers into nums.json file.
    '''
    num_identities = load_nums()

    for rect in rects:                                           
        x,y,w,h = cv2.boundingRect(rect)
        rect_im = im[y:y+h,x:x+w].copy()

        num_rects, _, num_im = prepare_nums(rect_im)
        for x,y,w,h in num_rects:
            num = num_im[y:y+h,x:x+w].copy()
            num = cv2.resize(num, (32, 32), interpolation = cv2.INTER_NEAREST)
            i = ident_num(num)

            if i and i in num_identities:
                num_identities[i] = (num_identities[i] + num)/2
            else:
                num_identities[i] = num

    if save:
        for k, v in num_identities.items():
            num_identities[k] = v[np.where(v != 0)] = 255
            num_identities[k] = v.tolist()

        with open("Data\\nums.json", "w") as f:
            json.dump(num_identities, f)

def load_numbers(file_path = "Data\\nums.json"):
    '''
    loads the numbers from nums.json into memory as cv2 np.ndarrays
    '''
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            dictionary = json.load(f)
        for k, v in dictionary.items():
            dictionary[k] = np.array(v).astype(np.uint8)
        return dictionary
    else:
        return dict()