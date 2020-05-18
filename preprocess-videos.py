from pathlib import Path
import os
import sys
import subprocess
import shutil
import fileinput

WORK_DIR = Path(__file__).parent.resolve()

JOB_TEMPLATE = WORK_DIR / "data" / "k8s_templates" / "prepare-videos-template.yaml"
JOB_PATH = WORK_DIR / "data" / "k8s_templates" / "prepare-videos.yaml"

VIDEO_URLS = [
 "https://www.youtube.com/watch?v=N9rkYYIIsXM"
]


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
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, universal_newlines=True)
    output, error = process.communicate()
    if error:
        raise ValueError(error)
    else:
        print(output)


if __name__ == "__main__":
    dest = sys.argv[1]

    for i, url in enumerate(VIDEO_URLS):
        shutil.copyfile(JOB_TEMPLATE, JOB_PATH)
        print(url)
        job_name = f"prepare-video-job-{i}"
        names_and_values = [("JOB_NAME", job_name), ("VIDEO_URL", f"\"{url}\""), ("SEGMENT_LENGTH", "\"60\""), ("DEST", f"\"{dest}/{i}\"")]
        replace(JOB_PATH, names_and_values)
        k8s_apply(JOB_PATH)
