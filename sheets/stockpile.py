import cv2
import logging
import os

from sheets.core import (
    find_numbers, find_icons, prepare_icon, load_numbers, load_icons, match_item, 
    ocr, guess_resolution
    )

DEBUG = False

class Stockpile():
    RESOLUTIONS = {
        "1920x1080": (42,32),
        "2560x1440": (56,43),
        "2560x1440x2": (56,42)
    }

    @classmethod
    def bool_size(cls, rectangle, resolution):
        try:
            size = cls.RESOLUTIONS[resolution]
        except KeyError:
            raise NotImplementedError(f"{resolution} not available in class Stockpile")

        _,_,w,h = cv2.boundingRect(rectangle)
        return (w,h) == size

    @classmethod
    def get_resolution(cls, image):
        return guess_resolution(image)

    def __init__(self, image, 
                 resolution=None, 
                 min_err=0.03, 
                 number_identities=None,
                 icon_identities=None,
                 numbers=None,
                 icons=None,
                 parse=True):
        if resolution:
            self.resolution = resolution
        else:
            self.resolution = guess_resolution(image)
        assert self.resolution in Stockpile.RESOLUTIONS

        self.min_err = min_err

        self.image = image

        self.data = dict()

        self.unidentified = []

        if number_identities:
            self.number_identities = number_identities
        else:
            self.number_identities = load_numbers(resolution=self.resolution)
        if icon_identities:
            self.icon_identities = icon_identities
        else:
            self.icon_identities = load_icons(resolution=self.resolution)

        self.numbers=find_numbers(self.image)
        self.icons=find_icons(self.numbers, resolution=self.resolution)

        self.names = list(self.icon_identities.keys())
        self.icon_arrays = list(self.icon_identities.values())

        if parse: self.parse()

        for k, v in self.data.items():
            self.data[k] = v.replace("k+", "000")

    def parse(self):
        for number, icon in zip(self.numbers, self.icons):
            x,y,w,h = cv2.boundingRect(number)
            number_image = self.image[y:y+h,x:x+w]

            x,y,w,h = cv2.boundingRect(icon)
            icon_image = self.image[y:y+h,x:x+w]

            icon_image = prepare_icon(icon_image)
            err, item_index = match_item(icon_image, self.icon_arrays)

            if err >= self.min_err:
                logging.info(f"Could not identify {(x,y,w,h)}, with err:{err}")
                self.unidentified.append(self.image[y:y+h,x:x+w].copy())
                continue

            name = os.path.basename(self.names[item_index])
            name, ext = os.path.splitext(name)
            val = ocr(number_image, self.number_identities)
            self.data[name] = val 
