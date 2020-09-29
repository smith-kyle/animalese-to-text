import os
from os import listdir
from os.path import isfile, isdir, join
from collections.abc import MutableMapping
from pathlib import Path
from typing import Callable, Dict, List, Optional, Tuple

import cv2
import numpy as np
from PIL import Image as PILImage, ImageChops
import imagehash
import pytesseract

from .characters import characters

FILE_DIR = Path(__file__).parent.absolute()

class Image:
    @staticmethod
    def to_bw(im: PILImage.Image, thresh: int) -> PILImage.Image:
        fn = lambda x : 255 if x > thresh else 0
        return im.convert('L').point(fn, mode='1')

    
    @staticmethod
    def combine_images(images: List[PILImage.Image]) -> PILImage.Image:
        widths, heights = zip(*(i.size for i in images))

        max_width = max(widths)
        total_height = sum(heights)

        new_im = PILImage.new('RGB', (max_width, total_height))

        y_offset = 0
        for im in images:
            new_im.paste(im, (0, y_offset))
            y_offset += im.size[1]

        return new_im

    @staticmethod
    def preprocess(im):
        """
        Crops the image to where the character name would appear
        makes it black and white
        """
        name_boxes = [
            (360, 614, 655, 695), 
            (395, 635, 585, 686),
        ]

        images = []
        for name_box in name_boxes:
            for thresh in [100, 200]:
                images.append(Image.to_bw(im.crop(box=name_box), thresh).rotate(-8))

        return Image.combine_images(images)

    @staticmethod
    def get_character(im) -> Optional[str]:
        image = Image.preprocess(im)
        # from uuid import uuid4
        # image.save(f"/Users/kylesmith/git-projects/animalese-to-text/{uuid4()}.png")
        text = pytesseract.image_to_string(image).strip()
        print(text)
        for char in characters:
            if char in text:
                return char

        return None


class VideoProcessor:
    def __init__(self, video_src: str, callback: Callable[[PILImage.Image, int], None], skip_frames: int = 0):
        self.video_src = video_src
        self.skip_frames = skip_frames
        self.callback = callback
        self.stop = False
    
    def start(self):
        cap = cv2.VideoCapture(self.video_src)
        current_frame = 0
        while True:
            current_frame += 1
            _ret, frame = cap.read()
            if frame is None or self.stop:
                break

            if current_frame % self.skip_frames != 0:
                continue

            im = PILImage.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            self.stop = self.callback(im, current_frame)


class CharactersDict(MutableMapping):
    """
    A fuzzy lookup where given an image it is mapped to
    a character, given some ground truth labels
    """
    def __init__(self, data_dir: str):
        """
        data_dir is a directory containing labeled samples of
        characters talking
        """
        self._dict: Dict[imagehash.Image, str] = {}

        chars = [d for d in listdir(data_dir) if isdir(join(data_dir, d))]
        for char in chars:
            for image_path in listdir(join(data_dir, char)):
                image_path = join(data_dir, char, image_path)
                if isfile(image_path):
                    self[PILImage.open(image_path)] = char

    def __setitem__(self, key: PILImage.Image, value: str):
        """
        Adds a sample image
        """
        self._dict[CharactersDict._hash_im(key)] = value

    def __getitem__(self, key: PILImage.Image):
        """
        Finds the character with the closest sample image
        """
        return self._dict[CharactersDict._hash_im(key)]
    
    @staticmethod
    def _hash_im(im):
        name_box = (380, 645, 550, 680)
        return str(imagehash.average_hash(im.crop(box=name_box)))


    def __delitem__(self, key):
        raise NotImplemented

    def __iter__(self):
        raise NotImplemented

    def __len__(self):
        return len(self._dict)

    def __str__(self):
        pass

    def __repr__(self):
        pass

    @staticmethod
    def populate_dict_seed(input_dir: str, output_dir: str):
        """
        `input_dir` is a flat directory containing videos
        `output_dir` is where the seed data for the characters dict will be stored
        """
        def callback(im: PILImage.Image, current_frame: int):
            """
            For a given video, identify whether a character is talking in the frame.
            If so save the frame at "${output_dir}/${character_name}"
            """
            maybe_char = Image.get_character(im)
            if maybe_char:
                im_dir = f"{output_dir}/{maybe_char.lower()}"
                if not isdir(im_dir):
                    os.mkdir(im_dir)
                im.save(f"{im_dir}/{current_frame}.png")

        # Go through every video in the input_dir and pass it through the callback
        for f in listdir(input_dir):
            f = join(input_dir, f)
            if isfile(f):
                vp = VideoProcessor(f, callback, 15)
                vp.start()
