FROM python:3.9.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y ffmpeg

CMD ["python3", "bdbot.py"]