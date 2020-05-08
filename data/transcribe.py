import pathlib
from pathlib import Path

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
SKIP_FRAMES = 2


def download_videos():
    video_links = ["https://www.youtube.com/watch?v=_FPUjb63ghk"]
    ydl_opts = {"format": "bestvideo"}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(video_links)


def is_end_of_snippet(text, prev_text):
    return len(text) < len(prev_text)


def frame_to_seconds(frame):
    return frame / FRAMES_PER_SECOND


def process_video(path):
    cap = cv2.VideoCapture(str(path))
    currentFrame = 0
    start_and_stop = None
    prev_text = ""
    im_cache = dict()

    while True:
        currentFrame += 1
        ret, frame = cap.read()
        if currentFrame % SKIP_FRAMES != 0:
            continue

        im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        im_cache[currentFrame] = im

        char = get_character(im)
        if char is not None:
            if start_and_stop is None:
                start_and_stop = [currentFrame - SKIP_FRAMES, None]

            text = get_text(im)

            if is_end_of_snippet(text, prev_text):
                start_and_stop[1] = currentFrame
                log_snippet(char, prev_text, start_and_stop, im_cache)
                start_and_stop = None

            prev_text = text


def log_snippet(char, text, start_and_stop, image_cache):
    print(
        f"{char} {start_and_stop[0] / FRAMES_PER_SECOND} - {start_and_stop[1] / FRAMES_PER_SECOND}: {text}"
    )
    image_cache[start_and_stop[0]].save(str(FRAMES_DIR / f"{start_and_stop[0]}.png"))
    image_cache[start_and_stop[1]].save(str(FRAMES_DIR / f"{start_and_stop[1]}.png"))


def get_character(im):
    name_box = (360, 614, 655, 695)
    text = pytesseract.image_to_string(im.crop(box=name_box))

    for c in characters:
        if c in text:
            return c
    return None


def get_text(im):
    name_box = (380, 720, 1541, 967)
    return pytesseract.image_to_string(im.crop(box=name_box)).strip()


process_video(VIDEOS_DIR / "1.mp4")
