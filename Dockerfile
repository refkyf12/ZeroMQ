FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg libsm6 libxext6

COPY . .

CMD ["python3", "main.py"]