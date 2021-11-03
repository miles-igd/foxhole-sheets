import cv2
import logging
import os

from sheets.core import find_numbers, find_icons, prepare_icon, load_numbers, load_icons, match_item, ocr



class Stockpile():
    RESOLUTIONS = {
        "1920x1080": (42,32)
    }

    @classmethod
    def bool_size(cls, rectangle, resolution):
        try:
            size = cls.RESOLUTIONS[resolution]
        except KeyError:
            raise NotImplementedError(f"{resolution} not available in Stockpile()")

        _,_,w,h = cv2.boundingRect(rectangle)
        return (w,h) == size

    def __init__(self, image, 
                 resolution="1920x1080", 
                 min_err=0.03, 
                 number_identities=load_numbers(r"Data/nums.json"),
                 icon_identities=load_icons(r"Data/Icons/"),
                 numbers=None,
                 icons=None,
                 parse=True):
        self.resolution = resolution
        self.min_err = min_err

        self.image = image
        self.data = dict()

        self.unidentified = []

        self.number_identities = number_identities
        self.icon_identities = icon_identities

        self.numbers=[rect for rect in find_numbers(self.image) if Stockpile.bool_size(rect, self.resolution)]
        self.icons=find_icons(self.numbers)

        self.names = list(icon_identities.keys())
        self.icon_arrays = list(icon_identities.values())

        if parse: self.parse()

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