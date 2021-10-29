import cv2
import io
import numpy as np
import os
import json

from sheets.ident import ident_item, ident_num

DEBUG = False

def find_items(im):
    assert type(im) == np.ndarray
    LOW_THRESH = 50
    HIGH_THRESH = 105

    im_Gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(im_Gray, LOW_THRESH, HIGH_THRESH)

    kernel = np.ones((4,4),np.uint8)
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    holes = opening.copy()
    cv2.floodFill(holes, None, (32, 0), 255)

    opening[np.where(holes==0)] = 255
    result = cv2.bitwise_and(im, im, mask = opening)

    if DEBUG:
        cv2.imshow("im", im)
        cv2.imshow("im_Gray", im_Gray)
        cv2.imshow("mask", mask)
        cv2.imshow("opening", opening)
        cv2.imshow("holes", holes)
        cv2.imshow("result", result)
        cv2.waitKey()
        
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    icons = [contour-np.array([49,0]) for contour in contours]
    rects = [cv2.convexHull(contour) for contour in contours]

    return icons, rects

def ident_items(icons, im):
    for icon in icons:
        x,y,w,h = cv2.boundingRect(icon)
        ident_icon = prepare_item(im[y:y+h,x:x+w].copy())
        ident_item(ident_icon, output="Icons\\")

def prepare_item(ident_icon):
    ident_icon = cv2.cvtColor(ident_icon, cv2.COLOR_BGR2GRAY)
    _, ident_icon = cv2.threshold(ident_icon, 144, 255, cv2.THRESH_BINARY)

    return ident_icon

def match_item(icon_image, arrs, metric=lambda x, y: ((x-y)**2).mean(), order=min, **kwargs):
    if len(arrs) == 0:
        return None, None

    distances = [metric(icon_image, icon_array, **kwargs) for icon_array in arrs]
    min_err = order(distances)
    return min_err, distances.index(min_err)

def load_icons(folder_path = "Icons\\"):
    files = os.listdir(folder_path) 
    icons = {os.path.basename(f): cv2.imread(folder_path + f, cv2.IMREAD_GRAYSCALE) for f in files}
    
    return icons

def ocr(im, identities):
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

def ident_nums(rects, im, output="nums.json", save=True):
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

        with open("nums.json", "w") as f:
            json.dump(num_identities, f)

def load_nums(file_path = "nums.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            dictionary = json.load(f)
        for k, v in dictionary.items():
            dictionary[k] = np.array(v).astype(np.uint8)
        return dictionary
    else:
        return dict()

def process(im, identify=False, min_err=.03):
    identities = load_nums()
    icon_arrays = load_icons()
    names = list(icon_arrays.keys())
    arrs = list(icon_arrays.values())
    data = dict()

    icons, rects = find_items(im)

    for icon, rect in zip(icons, rects):
        xi,yi,wi,hi = cv2.boundingRect(icon)
        icon_image = im[yi:yi+hi,xi:xi+wi]
        xr,yr,wr,hr = cv2.boundingRect(rect)
        rect_image = im[yr:yr+hr,xr:xr+wr]

        try:
            icon_image = prepare_item(icon_image)
        except cv2.error as e:
            print(str(e))
            continue

        try:
            err, index = match_item(icon_image, arrs)#, structural_similarity, max)
        except ValueError as e:
            print(str(e))
            continue

        if err >= min_err:
            print("Could not identify.", err)
            if identify:
                ident_item(icon_image, output="Icons\\")
            else:
                cv2.rectangle(im, (xi, yi), (xi+wi, yi+hi), (0, 0, 255), 3)
            continue
        name = names[index]
        name = os.path.basename(name)
        name, ext = os.path.splitext(name)
        val = ocr(rect_image, identities)
        data[name] = val 

    return data, im

if __name__ == "__main__":
    im = cv2.imread("unknown.png")
    data, out = process(im, identify=True)