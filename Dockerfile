FROM python:3.7.7-slim

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y curl apt-transport-https ca-certificates gnupg
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -

RUN apt-get update

RUN apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    google-cloud-sdk \
    ffmpeg \
    tesseract-ocr \
    libxrender1

COPY main.py main.py
COPY data/transcribe.py data/transcribe.py
COPY data/characters.py data/characters.py
COPY data/preprocessing.py data/preprocessing.py

CMD python /main.py