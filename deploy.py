from pathlib import Path
from pydub import AudioSegment
import os
import sys
import subprocess
import shutil
import fileinput

from data.transcribe import process_video

WORK_DIR = Path(__file__).parent.resolve()

JOB_TEMPLATE = WORK_DIR / "data" / "k8s_templates" / "transcribe-job-template.yaml"
JOB_PATH = WORK_DIR / "data" / "k8s_templates" / "transcribe-job.yaml"


def gsutil_ls(src):
    cmd = f"gsutil ls {src}"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    if error:
        raise ValueError(error)
    else:
        lines = str(output).splitlines()
        return [str(x) for x in lines if "mp4" in x]


def replace(file_path, name_and_values):
    with open(file_path, "r") as sources:
        lines = sources.readlines()
    with open(file_path, "w") as sources:
        for line in lines:
            for n, v in name_and_values:
                line = line.replace(n, v)
            sources.write(line)

    
def k8s_apply(path):
    cmd = f"kubectl apply -f {path}"
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise ValueError(error)
    else:
        print(output)


if __name__ == "__main__":
    video_source = sys.argv[1]
    dest = sys.argv[2]

    paths = gsutil_ls(video_source)
    for i, video_path in enumerate(paths):
        shutil.copyfile(JOB_TEMPLATE, JOB_PATH)
        job_name = f"transcribe-job-{i}"
        audio_path = f"{video_path.split('.mp4')[0]}.mp3"
        names_and_values = [("JOB_NAME", job_name), ("AUDIO_PATH", audio_path), ("VIDEO_PATH", video_path), ("DEST", dest)]
        replace(JOB_PATH, names_and_values)
        if i > 25:
            k8s_apply(JOB_PATH)
        if i == 50:
            break
