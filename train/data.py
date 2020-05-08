from pathlib import Path
import re

import torchaudio


def remove_non_alphanumeric(text):
    return re.sub(r'[\W_]+', '', text)


def load_data(path_str: str):
    """
    Yields waveform and text from a given transcription folder
    """
    path = Path(path_str)
    with open(path / "metadata.csv") as f:
        lines = f.read().splitlines()
    
    for line in lines:
        record_id, _text, normalized_text = line.split("|")
        audio_path = Path(path) / "wavs" / f"{record_id}.wav"
        waveform, _sample_rate = torchaudio.load(audio_path)
        yield waveform, remove_non_alphanumeric(normalized_text)

    