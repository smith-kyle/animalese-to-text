from pathlib import Path
import os
import math
import sys
import subprocess
import tempfile

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


def timestamp_to_ms(timestamp: str) -> int:
    hour, minute, second = timestamp.strip().split(":")
    return (int(hour) * 60 * 60 * 1000) + (int(minute) * 60 * 1000) + (math.floor(float(second) * 1000))


def split_file(input_path, output_path, start_ms, duration_ms):
    cmd = f"ffmpeg -ss {ms_to_timestamp(start_ms)} -t {ms_to_timestamp(duration_ms)} -i {input_path} -acodec copy -vcodec copy {output_path}"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise ValueError(error)


def split_video_and_audio(video_path: Path, audio_path: Path, output_dir: Path, chunk_len: int):
    chunk_len_ms = chunk_len * 1000

    total_ms = 1000 * get_video_length(video_path)
    num_chunks = math.ceil(total_ms / chunk_len_ms)
    for chunk in range(num_chunks):
        audio_output_path = output_dir / f"{chunk}.mp3"
        video_output_path = output_dir / f"{chunk}.mp4"
        start_ms = chunk * chunk_len_ms
        end_ms = min(total_ms, (chunk + 1) * chunk_len_ms)
        split_file(video_path, video_output_path, start_ms, chunk_len_ms)
        split_file(audio_path, audio_output_path, start_ms, chunk_len_ms)



def get_video_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

def run_cmd(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, shell=True, universal_newlines=True)
    output, error = process.communicate()
    if error:
        raise ValueError(error)
    else:
        print(output)
        return output


def download_video(url, output_path):
    run_cmd(f"youtube-dl -f best -o {output_path} {url}")


def strip_audio(video_path, audio_path):
    run_cmd(f"ffmpeg -i {video_path} -q:a 0 -map a {audio_path}")


if __name__ == "__main__":
    video_url = sys.argv[1]
    segment_length = sys.argv[2]
    dest = sys.argv[3]
    work_dir = Path(tempfile.mkdtemp())
    video_path = work_dir / "video.mp4"
    audio_path = work_dir / "audio.mp3"

    output_dir = work_dir / "output"
    os.mkdir(output_dir)

    download_video(video_url, video_path)
    strip_audio(video_path, audio_path)

    split_video_and_audio(video_path, audio_path, output_dir, int(segment_length))
    run_cmd(f"gsutil cp -r {output_dir} {dest}")
