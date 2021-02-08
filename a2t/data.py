
import subprocess
import json
import numpy as np
import tempfile
from torchvision import datasets, transforms
from torchvision.transforms import functional as F
import torch
from torch.utils import data
from PIL import Image
import os
from contextlib import contextmanager
from typing import Iterator, List, Tuple
from math import ceil
from pathlib import Path

from .model import model, transform


def get_video_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-print_format", "json", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)


@contextmanager
def temporaryframes(video_src, seconds) -> Iterator[Tuple[torch.utils.data.DataLoader, List[str]]]:
    with tempfile.TemporaryDirectory() as d:
        # Hack to allow use of datasets.ImageFolder
        os.mkdir(f"{d}/1")
        os.putenv('OUTPUT_DIR', f"{d}/1")
        os.putenv('VIDEO_SRC', video_src)
        n = 200
        for secs in [seconds[n * i:n * (i+1)] for i in range(ceil(len(seconds) / n))]:
            os.putenv('FRAMES', ' '.join(str(s) for s in secs))
            subprocess.run(["./get-frames.sh"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        frame_paths = [f"{d}/1/tmp_{s}.bmp" for s in seconds]
        dataset = datasets.ImageFolder(root=d, transform=transform)
        yield (torch.utils.data.DataLoader(dataset,batch_size=50, shuffle=False), frame_paths)


def create_dataset(video_src, output_dir, seconds) -> None:
    if not Path(output_dir).is_dir():
        os.mkdir(f"{output_dir}")
        os.mkdir(f"{output_dir}/dialogue")
        os.mkdir(f"{output_dir}/not-dialogue")
        
    with temporaryframes(video_src, seconds) as temp_frames:
        data_loader, frame_paths = temp_frames
        output = []
        for data, _ in data_loader:
            output.append(model(data))
        res = torch.cat(output).min(1).indices
        for i, (frame_path, is_dialogue) in enumerate(zip(frame_paths, res)):
            if is_dialogue:
                os.rename(frame_path, f"{output_dir}/dialogue/{seconds[i]}.bmp")
            else:
                os.rename(frame_path, f"{output_dir}/not-dialogue/{seconds[i]}.bmp")