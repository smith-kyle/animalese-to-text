import math
import pathlib
from pathlib import Path
from typing import Optional

import cv2
from PIL import Image
import pytesseract
from matplotlib import cm
import numpy as np
import youtube_dl

from .characters import characters


PROJECT_DIR = Path(__file__).parent.parent
FRAMES_DIR = PROJECT_DIR / "data" / "frames"
VIDEOS_DIR = PROJECT_DIR / "data" / "videos"

FRAMES_PER_SECOND = 30
SKIP_FRAMES = 1 
SECONDS_OF_AUDIO_AFTER_ARROW_APPEARS = 0.5


def download_videos():
    video_links = ["https://www.youtube.com/watch?v=_FPUjb63ghk"]
    ydl_opts = {"format": "bestvideo"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_links)


class OCR:
    def __init__(self):
        pass

    @staticmethod
    def has_yellow_arrow(im) -> bool:
        samples_pos = [(962, 997), (962, 990)]
        YELLOW_THRESHOLD = 80
        def distance(c1):
            (r1,g1,b1) = c1
            (r2, g2, b2) = (184, 138, 10)
            return math.sqrt((r1 - r2)**2 + (g1 - g2) ** 2 + (b1 - b2) **2)

        rgbs = [im.convert('RGB').getpixel(pos) for pos in samples_pos]
        ds = [distance(rgb) for rgb in rgbs]
        return any(d < YELLOW_THRESHOLD for d in ds)

    @staticmethod
    def get_character(im) -> Optional[str]:
        """
        Crops the image to where the character name would appear
        and checks whether the characters match any character names
        """
        name_box = (360, 614, 655, 695)
        text = pytesseract.image_to_string(im.crop(box=name_box))

        for c in characters:
            if c in text:
                return c
        return None
    
    @staticmethod
    def get_text(im) -> str:
        """
        Crops an image to where the dialog appears and converts to string
        """
        name_box = (380, 720, 1541, 967)
        return pytesseract.image_to_string(im.crop(box=name_box)).strip()


class Snippet:
    def __init__(self, start_frame: int, start_im: Image):
        print(f"Started snippet at {start_frame}")
        self.start_frame = start_frame
        self.start_im = start_im
        self.is_done = False
        self.last_text_append: Optional[int] = None
        self.last_text_append_im: Optional[Image] = None
        self.text = ""
        self.char = OCR.get_character(start_im)

    
    def process_frame(self, im: Image, frame_num: int):
        frame_text = OCR.get_text(im)

        if len(frame_text) > len(self.text):
            print(self.text)
            self.last_text_append = frame_num
            self.last_text_append_im = im
            self.text = frame_text

        if self.is_end(im, frame_text):
            print(OCR.has_yellow_arrow(im))
            im.save('./wau.png')
            self.dump(frame_num)
            self.is_done = True


    def dump(self, frame_num: int) -> None:
        if self.last_text_append is None or self.last_text_append_im is None:
            print(repr(self.text))
            raise ValueError("Trying to log without capturing text")

        start_timestamp = self.start_frame / FRAMES_PER_SECOND
        end_timestamp = (frame_num / FRAMES_PER_SECOND) + SECONDS_OF_AUDIO_AFTER_ARROW_APPEARS
        print(f"{self.char} {start_timestamp} - {end_timestamp}: {self.text}")


    def is_end(self, frame_im: Image, frame_text: str):
        if OCR.has_yellow_arrow(frame_im) and len(frame_text) > 0:
            return True
        
        if len(self.text) > 0 and len(frame_text) == 0:
            return True
        
        return False


    @staticmethod
    def is_start(im: Image) -> bool:
        """
        Checks whether the image is the start of some dialog
        """
        maybe_char = OCR.get_character(im)
        if maybe_char is not None:
            text = OCR.get_text(im)
            return text == ""
        return False


def process_video(path, n = 0):
    cap = cv2.VideoCapture(str(path))
    total_frames = cap.get(7)
    cap.set(1, n)
    current_frame = 0

    while True:
        current_frame += 1
        ret, frame = cap.read()
        if current_frame % SKIP_FRAMES != 0:
            continue

        im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        print(current_frame)
        if Snippet.is_start(im):
            s = Snippet(current_frame, im)
            while not s.is_done:
                current_frame += 1
                ret, frame = cap.read()
                print(current_frame)
                im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                s.process_frame(im, current_frame)


def get_nth_frame(path, n):
    cap = cv2.VideoCapture(str(path))
    total_frames = cap.get(7)
    cap.set(1, n)
    ret, frame = cap.read()
    return Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))


# process_video(VIDEOS_DIR / "1.mp4")
