# Animalese To Text

This project is an attempt to train a speech to text model using Animalese.

The dataset in `/data` contains 855 unique audio samples spoken by Blathers.
These samples were collected from this Youtube playlist: [Animal Crossing: New Horizons (no commentary)](https://www.youtube.com/playlist?list=PLhv3KSMy-FY4SSA_QfRhfw9sdBif09cOk)
The samples were gathered and transribed using the scripts in `/data_collection`.

## Data Format

Metadata is provided in metadata.csv. This file consists of one record per line, delimited by the pipe character. The fields are:

1. ID: this is the name of the corresponding .wav file
2. Transcription: words spoken by Blathers
3. Normalized Transcription: transcription with numbers, ordinals, and monetary units expanded into full words.
Each audio file is a single-channel 16-bit PCM WAV with a sample rate of 16000 Hz.

## Training

The training code was taken from a speech to text tutorial: [Building an end-to-end Speech Recognition model in PyTorch](https://www.assemblyai.com/blog/end-to-end-speech-recognition-pytorch).

To train locally first unzip the file `data/BlathersSpeech-1.2.zip`. Next, generate a [comet API key](https://www.comet.ml/) and run the following:

```
pip install -r requirements.txt
COMET_API_KEY=XXXXXXXXX python -m train.main
```
