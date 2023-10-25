# Docker Usage Guide

If you want to create a Docker volume and mount it into a container, you can follow these steps:

## Step 1: Creating a Docker Volume

You can use the `docker volume create` command to create a Docker volume. For example, if you want to create a volume named "zeromq_volume," run the following command:

```sh
docker volume create zeromq_volume
```

## Step 2: Building a Docker Image

Once you have successfully created the Docker volume, you can build a Docker image as previously described. Make sure you are in the directory containing the Dockerfile and application code, then run the following command:

```sh
docker build -t zeromq .
```

Replace "zeromq" with the name you want for your Docker image.

## Step 3: Running a Container with the Created Volume

Now, run a container and mount the Docker volume you created into the container with the following command:

```sh
docker run -d -p 5000:5000 -v zeromq_volume:/app/volume_kontainer zeromq
```

- `-d` runs the container in the background.
- `-p 5000:5000` forwards port 5000 from the container to port 5000 on the host machine.
- `-v zeromq_volume:/app/volume_kontainer` mounts the Docker volume "zeromq_volume" into the "/app/volume_kontainer" directory within the container. The volume will be automatically created in the container with the data from the Docker volume you created earlier.

---

# how to run the app manually ?

### Install requirements.txt
```python
pip install requirements.txt

```
### Run Server
```python
python main.py
```
```python
python client.py
```
### Now Browse
- [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

#### Use Built-in Webcam of Laptop
##### Put Zero (O) in cv2.VideoCapture(0)
```python
cv2.VideoCapture(0)
 
```
#### Use Ip Camera/CCTV/RTSP Link
```python
cv2.VideoCapture('rtsp://username:password@camera_ip_address:554/user=username_password='password'_channel=channel_number_stream=0.sdp')  

 ```
####  Example RTSP Link
```python
cv2.VideoCapture('rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=0_stream=0.sdp')

```
#### Change Channel Number to Change the Camera
```python
cv2.VideoCapture('rtsp://mamun:123456@101.134.16.117:554/user=mamun_password=123456_channel=1_stream=0.sdp')

```
#### Display the resulting frame in browser
```python
cv2.imencode('.jpg', frame)[1].tobytes()

```   
