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
    "https://youtu.be/nyRHbBWoQ7w",
    "https://youtu.be/_FPUjb63ghk",
    "https://youtu.be/B5-1TMx9bAY",
    "https://youtu.be/k0Esc0p1Rrk",
    "https://youtu.be/KC2nv4X_KdM",
    "https://youtu.be/aQh_mceb_7k",
    "https://youtu.be/icQIhSLJWv4",
    "https://youtu.be/yQk0n28S5Yc",
    "https://youtu.be/eZsuUDPwqBU",
    "https://youtu.be/mUA-qSxqRpo",
    "https://youtu.be/Q0E0w_gh5W4",
    "https://youtu.be/A5hdqE6Ei88",
    "https://youtu.be/X9e0AOswWbQ",
    "https://youtu.be/dqBn72EnGCc",
    "https://youtu.be/dlWGrYTDvYg",
    "https://youtu.be/0ff5HCYItt4",
    "https://youtu.be/usExSitGL3o",
    "https://youtu.be/XHj7LWmye0I",
    "https://youtu.be/tsctXGtf4dw",
    "https://youtu.be/IcN4G4lVTAc",
    "https://youtu.be/x41BY62hhnE",
    "https://youtu.be/AHFRlGPkfEg",
    "https://youtu.be/ORedilpSGWw",
    "https://youtu.be/NgVjNuv4CgU",
    "https://youtu.be/F1rNEdIre9M",
    "https://youtu.be/6Ap65TcM2vY",
    "https://youtu.be/AhBpzti3tNQ",
    "https://youtu.be/nQfE6_qRKng",
    "https://youtu.be/UfgzvuvPBUU",
    "https://youtu.be/vbp7VgyXoIQ",
    "https://youtu.be/XplQ03MDtXg",
    "https://youtu.be/N9rkYYIIsXM",
    "https://youtu.be/Ds3s4JjpN1A",
    "https://youtu.be/CSAnldwVx3o",
    "https://youtu.be/pYCsjTB33m4",
    "https://youtu.be/kUJfAU7V2Mg",
    "https://youtu.be/p1Gs2nK920Q",
    "https://youtu.be/A9RoLUEA52k",
    "https://youtu.be/4MweNH0V0SU",
    "https://youtu.be/frL-Benek0c",
    "https://youtu.be/YObVsKDhXLM",
    "https://youtu.be/ESy3ORf9dtc",
    "https://youtu.be/KNcbbtj90s4",
    "https://youtu.be/59rHUiyyKP0",
    "https://youtu.be/swLEZMoB7h8",
    "https://youtu.be/_d25JzMq8r0",
    "https://youtu.be/K4X5NEgZ2KE",
    "https://youtu.be/hEFqogc_irI",
    "https://youtu.be/P8PtVyEsCFw",
    "https://youtu.be/zbHPZGW4iYg",
    "https://youtu.be/OZ75vVDUI-4",
    "https://youtu.be/KtEECoVR-Ag",
    "https://youtu.be/PSp_n61aKTk",
    "https://youtu.be/wOAXluPmC_w",
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
