import pathlib
from pathlib import Path
from typing import Optional

import cv2
from PIL import Image
import pytesseract
from matplotlib import cm
import numpy as np
import youtube_dl

from characters import characters


PROJECT_DIR = Path(__file__).parent.parent
FRAMES_DIR = PROJECT_DIR / "data" / "frames"
VIDEOS_DIR = PROJECT_DIR / "data" / "videos"

FRAMES_PER_SECOND = 30
SKIP_FRAMES = 3


def download_videos():
    video_links = ["https://www.youtube.com/watch?v=_FPUjb63ghk"]
    ydl_opts = {"format": "bestvideo"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_links)


class OCR:
    def __init__(self):
        pass

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
        self.num_frames_char_missing = 0

    
    def process_frame(self, im: Image, frame_num: int):
        frame_text = OCR.get_text(im)
        char = OCR.get_character(im)

        if char != self.char:
            self.num_frames_char_missing += 1
        else:
            self.num_frames_char_missing = 0

        if len(frame_text) > len(self.text):
            print(self.text)
            self.last_text_append = frame_num
            self.last_text_append_im = im
            self.text = frame_text
        elif self.is_end(im, frame_text):
            self.dump()
            self.is_done = True


    def dump(self) -> None:
        if self.last_text_append is None or self.last_text_append_im is None:
            raise ValueError("Trying to log without capturing text")

        start_timestamp = self.start_frame / FRAMES_PER_SECOND
        end_timestamp = self.last_text_append / FRAMES_PER_SECOND
        print(f"{self.char} {start_timestamp} - {end_timestamp}: {self.text}")


    def is_end(self, frame_im: Image, frame_text: str):
        if self.num_frames_char_missing > 5:
            return True

        is_next_dialog = len(frame_text) == 0 and len(self.text) > 0 
        return is_next_dialog


    @staticmethod
    def is_start(im: Image) -> bool:
        """
        Checks whether the image is the start of some dialog
        """
        if OCR.get_character(im) is not None:
            return OCR.get_text(im) == ""
        return False


def process_video(path):
    cap = cv2.VideoCapture(str(path))
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


process_video(VIDEOS_DIR / "1.mp4")
