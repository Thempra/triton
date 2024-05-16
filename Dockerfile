FROM python:3.13.0b1-slim

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN apt update && apt -y install ffmpeg

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./triton.py"]
