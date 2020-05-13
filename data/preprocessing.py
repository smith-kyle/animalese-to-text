from pathlib import Path
import os
import math
import sys
import subprocess

import cv2
from pydub import AudioSegment

VIDEOS_DIR = Path(__file__).parent / "videos"


bashCommand = "cwm --rdf test.rdf --ntriples > test.nt"

def ms_to_hmsms(ms):
    seconds=int((ms / 1000) % 60)
    minutes=int((ms/(1000 * 60)) % 60)
    hours=int((ms/(1000*60*60))%24)

    leftover_ms = ms - ((hours * 60 * 60 * 1000) + (minutes * 60 * 1000) + (seconds * 1000))


    return (str(hours).zfill(2), str(minutes).zfill(2), str(seconds).zfill(2), leftover_ms)

def ms_to_timestamp(ms):
    start_hour, start_min, start_sec, start_ms = ms_to_hmsms(ms)
    if start_ms:
        return f"{start_hour}:{start_min}:{start_sec}.{start_ms}"
    else:
        return f"{start_hour}:{start_min}:{start_sec}"


def split_video(input_path, output_path, start_ms, duration_ms):
    cmd = f"ffmpeg -ss {ms_to_timestamp(start_ms)} -t {ms_to_timestamp(duration_ms)} -i {input_path} -acodec copy -vcodec copy {output_path}"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise ValueError(error)


def split_video_and_audio(video_num: str, chunk_len: int):
    video_path = VIDEOS_DIR / f"{video_num}.mp4"
    audio_path = VIDEOS_DIR / f"{video_num}.mp3"
    output_dir = VIDEOS_DIR / f"split-{video_num}"

    os.mkdir(output_dir)
    audio = AudioSegment.from_mp3(audio_path)

    chunk_len_ms = chunk_len * 1000

    total_ms = len(audio)
    num_chunks = math.ceil(total_ms / chunk_len_ms)
    for chunk in range(num_chunks):
        audio_output_path = output_dir / f"{chunk}.mp3"
        video_output_path = output_dir / f"{chunk}.mp4"
        start_ms = chunk * chunk_len_ms
        end_ms = min(total_ms, (chunk + 1) * chunk_len_ms)
        audio[start_ms:end_ms].export(audio_output_path, format="mp3")
        split_video(video_path, video_output_path, start_ms, chunk_len_ms)



if __name__ == "__main__":
    video_num = sys.argv[1]
    segment_length = sys.argv[2]
    split_video_and_audio(video_num, int(segment_length))
