import base64
import cv2
import zmq
import numpy as np
import time

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.bind('tcp://*:6666')

net = cv2.dnn.readNet("yolov3-tiny.weights", "yolov3-tiny.cfg")
classes = []

with open("coco.names") as f:
    classes = f.read().strip().split('\n')\

# camera = cv2.VideoCapture("/home/refky/websocket/live-stream-zeromq/jpo.avi")
camera = cv2.VideoCapture("rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00")
width = int(camera.get(3))
height = int(camera.get(4)) # init the camera

while True:
    grabbed, frame = camera.read()
    if frame is None:
        frame = np.zeros((1020,480,3), dtype=np.uint8)
        camera.release()
        camera = cv2.VideoCapture(camera)  # grab the current frame
    # frame = cv2.resize(frame, (640, 480)) 
    if grabbed:
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outputLayers = net.getUnconnectedOutLayersNames()
        outs = net.forward(outputLayers)

        boxes = []
        class_ids = []
        confidences = []

        for out in outs:
                for detection in out:
                    scores = detection[5:]
                    classId = np.argmax(scores)
                    confidence = scores[classId]
                    if confidence > 0.5:
                        centerX = int(detection[0] * width)
                        centerY = int(detection[1] * height)
                        w = int(detection[2] * width)
                        h = int(detection[3] * height)

                        x = int(centerX - w / 2)
                        y = int(centerY - h / 2)

                        boxes.append([x, y, w, h])
                        class_ids.append(classId)
                        confidences.append(float(confidence))
            
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

        for i in indices:
            x, y, w, h = boxes[i]
            classId = class_ids[i]
            label = classes[classId]
            confidence = confidences[i]

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)
    else:
        break
     # resize the frame
    
    