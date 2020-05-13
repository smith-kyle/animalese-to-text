FROM python:3.7.7-slim

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y curl
RUN curl -sSL https://sdk.cloud.google.com | bash
RUN apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    gsutil \
    ffmpeg \
    tesseract-ocr \
    libxrender1

COPY main.py main.py
COPY data/transcribe.py data/transcribe.py
COPY data/characters.py data/characters.py

CMD python /main.py