import cv2
import io
import json
import numpy as np
import os
import random
import logging

from collections import Counter
from sheets.ident import ident_item, ident_num

DEBUG = False

RESOLUTIONS = {
    "1920x1080": (42,32),
    "2560x1440": (56,43),
    "2560x1440x2": (56,42)
}

RESOLUTIONS_INV = {
    (42, 32): "1920x1080",
    (56, 43): "2560x1440",
    (56, 42): "2560x1440"
}

ICON_TRANSLATION = {
    "1920x1080": np.array([49,0]),
    "2560x1440": np.array([65,0])
}

def find_numbers(im, low_threshold=50, high_threshold=105):
    '''
    Finds rectangles on a cv2 np.ndarray given the expected values of the grey boxes in a Foxhole stockpile.
    '''
    assert type(im) == np.ndarray

    holes, opening = find_holes(im, low_threshold, high_threshold)
    starting = find_reasonable_opening(holes)

    cv2.floodFill(holes, None, starting, 255)

    opening[np.where(holes==0)] = 255
    result = cv2.bitwise_and(im, im, mask = opening)

    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = [cv2.convexHull(contour) for contour in contours]
    rects = reduce_to_resolutions(rects)

    return rects

def find_holes(im, low_threshold, high_threshold):
    im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(im_gray, low_threshold, high_threshold)

    kernel = np.ones((4,4),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    holes = opening.copy()

    return holes, opening

def reduce_to_resolutions(rects):
    candidates = []

    for rect in rects:
        x,y,w,h = cv2.boundingRect(rect)
        if (w,h) in RESOLUTIONS.values():
            if (w,h) == (56, 43):
                p1 = [x+w-1,y]
                p2 = [x+w-1,y+h-2]
                p3 = [x,y+h-2]
                p4 = [x,y]
                
                rect = np.array([[p1],[p2],[p3],[p4]]) 
            candidates.append(rect)

    return candidates

def guess_resolution(im):
    rects = find_numbers(im)
    sizes = [cv2.boundingRect(rect)[2:] for rect in rects]
    size = Counter(sizes).most_common(1)[0][0]

    return RESOLUTIONS_INV[size]

def find_reasonable_opening(holes, window=11, limit=9):
    '''
    introduces randomness into algorithm, consider reconsidering
    if a test fails sometimes, check here
    '''
    w,h=holes.shape
    for i in range(limit):
        x=random.randint(1,w-1)
        y=random.randint(1,h-1)
        logging.info(f"Trying to flood fill at ({y},{x})")

        if np.sum(holes[x:x+window,y:y+window]) == 0:
            return (y,x)
        else:
            logging.info("Failed")

    return (22,22)

def find_icons(num_rects, resolution="1920x1080"):
    translation = ICON_TRANSLATION[resolution]
    return [rect-translation for rect in num_rects]

def ident_items(im):
    '''
    Prompts the user to identify icons, given a stockpile image.
    It will save the icon into the folder {resolution}/Icons/
    '''
    resolution = guess_resolution(im)
    rects = find_numbers(im)
    icons = find_icons(rects, resolution=resolution)

    for icon in icons:
        x,y,w,h = cv2.boundingRect(icon)
        ident_icon = prepare_icon(im[y:y+h,x:x+w].copy())
        ident_item(ident_icon, output=f"Data/{resolution}/Icons/")

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

def load_icons(folder_path = "./Data/{res}/Icons/", resolution = "1920x1080"):
    '''
    loads the icons from folder_path or Icons\\ into memory as cv2 np.ndarrays
    '''
    folder_path = folder_path.format(res=resolution)
    files = os.listdir(folder_path) 
    icons = {os.path.basename(f): cv2.imread(folder_path + f, cv2.IMREAD_GRAYSCALE) for f in files}
    
    return icons

NUM_SIZES = {
    "1920x1080": (32,32),
    "2560x1440": (48,48)
}

def ocr(im, identities, resolution="1920x1080"):
    '''
    Brute-force matching of numbers to its identity, which is determined beforehand.
    '''
    rects, thresh, original = prepare_nums(im)
    digits = []
    nums = dict()

    for x,y,w,h in rects:
        num = original[y:y+h,x:x+w].copy()
        num = cv2.resize(num, NUM_SIZES[resolution], interpolation = cv2.INTER_NEAREST)
        
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

def ident_nums(rects, im, resolution="1920x1080", save=True):
    '''
    Prompts the user to identify a number,
    It will save the numbers into nums.json file.
    '''
    num_identities = load_numbers(resolution=resolution)

    for rect in rects:                                           
        x,y,w,h = cv2.boundingRect(rect)
        rect_im = im[y:y+h,x:x+w].copy()

        num_rects, _, num_im = prepare_nums(rect_im)
        for x,y,w,h in num_rects:
            num = num_im[y:y+h,x:x+w].copy()
            num = cv2.resize(num, NUM_SIZES[resolution], interpolation = cv2.INTER_NEAREST)
            i = ident_num(num)

            if i and i in num_identities:
                num_identities[i] = (num_identities[i] + num)/2
            else:
                num_identities[i] = num

    if save:
        for k, v in num_identities.items():
            num_identities[k] = v[np.where(v != 0)] = 255
            
            cv2.imwrite(f"Data/{resolution}/Numbers/{k}.png", v)

def load_numbers(folder_path = "./Data/{res}/Numbers/", resolution = "1920x1080"):
    '''
    loads the numbers from numbers folder into memory as cv2 np.ndarrays
    '''
    folder_path = folder_path.format(res=resolution)
    files = os.listdir(folder_path)  
    nums = dict()

    for filepath in files:
        name = os.path.basename(filepath)
        name, ext = os.path.splitext(name)
        nums[name] = cv2.imread(folder_path + filepath, cv2.IMREAD_GRAYSCALE)

    return nums