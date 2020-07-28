"""
Starts a k8s job per each VIDEO_URL to: 
  1. Download the video 
  2. Split the video into 60 second chunks
  3. Save the audio and video separately to a destination URL
"""

from pathlib import Path
import os
import sys
import subprocess
import shutil
import fileinput

DATA_COLLECTION_DIR = Path(__file__).parent.resolve()

JOB_TEMPLATE = DATA_COLLECTION_DIR / "k8s_templates" / "prepare-videos-template.yaml"
JOB_PATH = DATA_COLLECTION_DIR / "k8s_templates" / "prepare-videos.yaml"

VIDEO_URLS = [
    # "https://youtu.be/nyRHbBWoQ7w",
    # "https://youtu.be/_FPUjb63ghk",
    # "https://youtu.be/B5-1TMx9bAY",
    # "https://youtu.be/k0Esc0p1Rrk",
    # "https://youtu.be/KC2nv4X_KdM",
    # "https://youtu.be/aQh_mceb_7k",
    # "https://youtu.be/icQIhSLJWv4",
    # "https://youtu.be/yQk0n28S5Yc",
    # "https://youtu.be/eZsuUDPwqBU",
    # "https://youtu.be/mUA-qSxqRpo",
    # "https://youtu.be/Q0E0w_gh5W4",
    # "https://youtu.be/A5hdqE6Ei88",
    # "https://youtu.be/X9e0AOswWbQ",
    # "https://youtu.be/dqBn72EnGCc",
    # "https://youtu.be/dlWGrYTDvYg",
    # "https://youtu.be/0ff5HCYItt4",
    # "https://youtu.be/usExSitGL3o",
    # "https://youtu.be/XHj7LWmye0I",
    # "https://youtu.be/tsctXGtf4dw",
    # "https://youtu.be/IcN4G4lVTAc",
    # "https://youtu.be/x41BY62hhnE",
    # "https://youtu.be/AHFRlGPkfEg",
    # "https://youtu.be/ORedilpSGWw",
    # "https://youtu.be/NgVjNuv4CgU",
    # "https://youtu.be/F1rNEdIre9M",
    # "https://youtu.be/6Ap65TcM2vY",
    # "https://youtu.be/AhBpzti3tNQ",
    # "https://youtu.be/nQfE6_qRKng",
    # "https://youtu.be/UfgzvuvPBUU",
    # "https://youtu.be/vbp7VgyXoIQ",
    # "https://youtu.be/XplQ03MDtXg",
    # "https://youtu.be/N9rkYYIIsXM",
    # "https://youtu.be/Ds3s4JjpN1A",
    # "https://youtu.be/CSAnldwVx3o",
    # "https://youtu.be/pYCsjTB33m4",
    # "https://youtu.be/kUJfAU7V2Mg",
    # "https://youtu.be/p1Gs2nK920Q",
    # "https://youtu.be/A9RoLUEA52k",
    # "https://youtu.be/4MweNH0V0SU",
    # "https://youtu.be/frL-Benek0c",
    # "https://youtu.be/YObVsKDhXLM",
    # "https://youtu.be/ESy3ORf9dtc",
    # "https://youtu.be/KNcbbtj90s4",
    # "https://youtu.be/59rHUiyyKP0",
    # "https://youtu.be/swLEZMoB7h8",
    # "https://youtu.be/_d25JzMq8r0",
    # "https://youtu.be/K4X5NEgZ2KE",
    # "https://youtu.be/hEFqogc_irI",
    # "https://youtu.be/P8PtVyEsCFw",
    # "https://youtu.be/zbHPZGW4iYg",
    # "https://youtu.be/OZ75vVDUI-4",
    # "https://youtu.be/KtEECoVR-Ag",
    # "https://youtu.be/PSp_n61aKTk",
    # "https://youtu.be/wOAXluPmC_w",
    "https://youtu.be/im3_MIMHn9A",
    "https://youtu.be/QvST7UzHV54",
    "https://youtu.be/VjNpipeoTyA",
    "https://youtu.be/9i3Blns2MT4",
    "https://youtu.be/o9U9nXgsjLo",
    "https://youtu.be/k_zoMmXr7sc",
    "https://youtu.be/nzXgF7LHzEg",
    "https://youtu.be/TuANAHqvrVw",
    "https://youtu.be/TjM0BttPC3c",
    "https://youtu.be/J3jFiGPeq0s",
    "https://youtu.be/AROsgz74ky0",
    "https://youtu.be/L-jPta9qV1Y",
    "https://youtu.be/EJyblVrkhXI",
    "https://youtu.be/szavRsTbseY",
    "https://youtu.be/NcItAIZWYto",
    "https://youtu.be/HK-TZd3j0zo",
    "https://youtu.be/AJ8XxSBfmGE",
    "https://youtu.be/8YkdR-UVDwQ",
    "https://youtu.be/OqwoqMGE1qE",
    "https://youtu.be/XDHT7MpDxFQ",
    "https://youtu.be/H8-ZG75aHNk",
    "https://youtu.be/aBncYaejbS8",
    "https://youtu.be/Qr22eY63nWM",
    "https://youtu.be/-8l23xsAbDs",
    "https://youtu.be/kBHVPsOb5DM",
    "https://youtu.be/eNBJTRlgpMg",
    "https://youtu.be/jE4BrIEnysQ",
    "https://youtu.be/7yJiuywDnwk",
    "https://youtu.be/IhL0_Eew7PY",
    "https://youtu.be/RezBR3XYwNU",
    "https://youtu.be/xLNUfahwZWQ",
    "https://youtu.be/8e-oJCv4tGA",
    "https://youtu.be/W_6mwhYfNsI",
    "https://youtu.be/EXWuEF8Jeeg",
    "https://youtu.be/2fym9hUk5S8",
    "https://youtu.be/RwQjpNrpGPo",
    "https://youtu.be/axHR1-udcZc",
    "https://youtu.be/fW12uR98x6A",
    "https://youtu.be/VaIUjZreemo",
    "https://youtu.be/m0ahsWo841U",
    "https://youtu.be/Ov12qYyat9k",
    "https://youtu.be/ov7R6504jqU",
    "https://youtu.be/Isjrz1VVajQ",
    "https://youtu.be/Ds5hM_K7QMI",
    "https://youtu.be/eQHS4B8gtJo",
    "https://youtu.be/jZieEeK-LCc",
    "https://youtu.be/Iq844ldKEhQ",
    "https://youtu.be/VgPV8JHJA9I",
    "https://youtu.be/iEb6Jh3M9Wk",
    "https://youtu.be/zLqLPq6udbQ",
    "https://youtu.be/PphgwAlUKGY",
    "https://youtu.be/WsWM8BLpJ_o",
    "https://youtu.be/xINr1DbKegg",
    "https://youtu.be/tu2nnrknFxQ",
    "https://youtu.be/15fZ4YHCgr8",
    "https://youtu.be/ViKPofz11GA",
    "https://youtu.be/O-75XJqEzcI",
    "https://youtu.be/qDbczpCErO4",
    "https://youtu.be/0V8niTK1K0s",
    "https://youtu.be/rnsYYhxmsTU",
    "https://youtu.be/KWfSXfDBbTA",
    "https://youtu.be/aEx0dwzRaUs",
    "https://youtu.be/tldUzWUW2JQ",
    "https://youtu.be/awDs7E9rj00",
    "https://youtu.be/ODGih-Aje3I",
    "https://youtu.be/oBk7fIU4gUk",
    "https://youtu.be/ll6qAGftWDc",
    "https://youtu.be/uwiENGJhjns",
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

NUM_VIDEOS_PREVIOUSLY_PREPROCESSED = 53
if __name__ == "__main__":
    # GCP storage destination URL (e.g. gs://animalese-to-text/videos/switch-playthroughs-playlist)
    dest = sys.argv[1]

    for i, url in enumerate(VIDEO_URLS):
        shutil.copyfile(JOB_TEMPLATE, JOB_PATH)
        video_id = NUM_VIDEOS_PREVIOUSLY_PREPROCESSED + i
        print(url)
        job_name = f"prepare-video-job-{video_id}"
        names_and_values = [("JOB_NAME", job_name), ("VIDEO_URL", f"\"{url}\""), ("SEGMENT_LENGTH", "\"60\""), ("DEST", f"\"{dest}/{video_id}\"")]
        replace(JOB_PATH, names_and_values)
        k8s_apply(JOB_PATH)
