import cv2
import zmq
import base64
import numpy as np

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.connect('tcp://localhost:5555')

context2 = zmq.Context()
footage_socket2 = context.socket(zmq.SUB)
footage_socket2.connect('tcp://localhost:6666')

footage_socket.setsockopt_string(zmq.SUBSCRIBE, '')

footage_socket2.setsockopt_string(zmq.SUBSCRIBE, '')


def streamer():
    while True:
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        return cv2.imencode('.jpg', source)[1].tobytes()
    
def streamer2():
    while True:
        frame = footage_socket2.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        return cv2.imencode('.jpg', source)[1].tobytes()

        # source.tobytes()

