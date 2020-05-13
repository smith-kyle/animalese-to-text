from pathlib import Path
from pydub import AudioSegment
import os
import sys

from data.transcribe import process_video

WORK_DIR = Path(__file__).parent


VIDEO_DEST = WORK_DIR / "video.mp4"
AUDIO_DEST = WORK_DIR / "audio.mp3"
OUTPUT_DIR = WORK_DIR / "result"

def download_from_storage(src, dest):
    cmd = f"gsutil cp {src} {dest}"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise ValueError(error)

def upload_to_storage(src, dest):
    cmd = f"gsutil cp -r {src} {dest}"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise ValueError(error)


if __name__ == "__main__":
    os.mkdir(OUTPUT_DIR)
    video_src = sys.argv[1]
    audio_src = sys.argv[2]
    output_url = sys.argv[3]

    download_from_storage(video_src, VIDEO_DEST)
    download_from_storage(audio_src, AUDIO_DEST)
    audio = AudioSegment.from_mp3(AUDIO_DEST)

    video_num = video_src.split("/")[-1].split(".mp4")[0]

    snippet_num = 0
    for s in process_video(VIDEO_DEST):
        snippet_num += 1
        prefix = f"{video_num}.{snippet_num}"
        with open(OUTPUT_DIR / f"{prefix}.txt") as f:
            f.write(f"{s.char}\n{s.text}")
        
        start_ms = int(s.start_frame / s.fps) * 1000
        end_ms = int(s.end_frame / s.fps) * 1000
        audio[start_ms:end_ms].export(OUTPUT_DIR / f"{prefix}.mp3", format="mp3")
    
    upload_to_storage(OUTPUT_DIR, output_url)


        

        
