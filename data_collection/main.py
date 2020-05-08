from pathlib import Path
from pydub import AudioSegment
import os
import sys
import subprocess

from data.transcribe import process_video

WORK_DIR = Path(__file__).parent


VIDEO_DEST = WORK_DIR / "video.mp4"
AUDIO_DEST = WORK_DIR / "audio.mp3"
OUTPUT_DIR = WORK_DIR / "result"


def gsutil_cp(src, dest):
    cmd = f"gsutil cp {src} {dest}"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise ValueError(error)
    else:
        print(output)


if __name__ == "__main__":
    if not OUTPUT_DIR.is_dir():
        os.mkdir(OUTPUT_DIR)
    video_src = sys.argv[1]
    audio_src = sys.argv[2]
    output_url = sys.argv[3]

    gsutil_cp(video_src, VIDEO_DEST)
    gsutil_cp(audio_src, AUDIO_DEST)
    audio = AudioSegment.from_mp3(AUDIO_DEST)

    big_video = video_src.split("/")[-2]
    small_video = video_src.split("/")[-1].split(".mp4")[0]

    snippet_num = 0
    for s in process_video(VIDEO_DEST):
        snippet_num += 1
        prefix = f"{big_video}.{small_video}.{snippet_num}"
        text_snippet_path = OUTPUT_DIR / f"{prefix}.txt"
        with open(text_snippet_path, "w") as f:
            f.write(f"{s.char}\n{s.text}")
        
        fps = 30
        start_ms = int((s.start_frame / fps) * 1000)
        end_ms = int((s.end_frame / fps) * 1000)

        audio_snippet_path = OUTPUT_DIR / f"{prefix}.mp3"
        audio[start_ms:end_ms].export(audio_snippet_path, format="mp3")
        gsutil_cp(audio_snippet_path, output_url)
        gsutil_cp(text_snippet_path, output_url)

    print("Finished transcribing!")


        

        
