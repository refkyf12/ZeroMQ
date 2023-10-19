FROM python:3.8

WORKDIR /app

COPY requirements.txt .

RUN pip3 install blinker

RUN pip3 install click

RUN pip3 install docopt

RUN pip3 install Flask

RUN pip3 install imutils

RUN pip3 install itsdangerous

RUN pip3 install Jinja2

RUN pip3 install MarkupSafe

RUN pip3 install mqtt-client

RUN pip3 install numpy==1.24.0

RUN pip3 install opencv-python

RUN pip3 install paho-mqtt

RUN pip3 install pytz

RUN pip3 install pyzmq

RUN pip3 install terminaltables

RUN pip3 install Werkzeug

RUN pip3 install zmq

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

COPY . .

CMD ["python3", "main.py"]