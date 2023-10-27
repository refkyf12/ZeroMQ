import base64
import cv2
import zmq
import numpy as np
import time
import threading
import cv2
import time
import json
import os

from imutils.video import VideoStream, FileVideoStream
from multiprocessing import Process
from multiprocessing import Queue
from multiprocessing import Manager
from utils.helper import getOutputsNames, draw_pred

class AnalyticClient:
    port = "6000"
    ip = "127.0.0.1"
    rtsp = 0
    weight = "../models/yolov3-tiny.weights"
    config = "../models/yolov3-tiny.cfg"
    kelas = "../models/coco.names"
    cap = None
    manager = Manager()
    var_manager = manager.dict({'image' : None, 'time_process': 0,})
    inputQueue = Queue(maxsize=10)
    outputQueue = Queue(maxsize=10)
    frameQueue = Queue(maxsize=10)
    net = cv2.dnn.readNet(weight, config)
    detections = None
    p_detect = None
    p_classify_frame = None
    p_output = None

    def __init__(self):
        self.cap = cv2.VideoCapture(self.rtsp)
    
    def setPort(self, port):
        self.port = port
    def setIp(self, ip):
        self.ip = ip
    def setRtsp(self, rtsp):
        self.rtsp = rtsp
        self.cap = cv2.VideoCapture(rtsp)
    def setWeight(self, weight):
        self.weight = weight
    def setConfig(self, config):
        self.config = config
    def setKelas(self, kelas):
        self.kelas = kelas
    
    def classify_frame(self):
        while True:
            # time.sleep(delay)
            if not self.inputQueue.empty():
            
                start_time_process = time.time()
                
                image = self.inputQueue.get()
                blob = cv2.dnn.blobFromImage(image, 0.00392, (412, 412), (0, 0, 0), True, crop=False)
                self.net.setInput(blob)
                self.detections = self.net.forward(getOutputsNames(self.net))
            
                end_time_process = time.time()
                
                time_process = end_time_process - start_time_process
                self.var_manager['time_process'] = "{:.2f}".format(time_process)
                
                self.outputQueue.put(self.detections)
    
    def detect(self):
        # with open('config/config.json', 'r') as config_file:
        #     config = json.load(config_file)

        # kamera_id = "camera_1"
        # rtsp_url = config["cameras"][kamera_id]["rtsp_url"]
        # print("ZMQ Address:", zmq_address)
        
        # cap = FileVideoStream(config['cam']).start() # Load Video
        # cap = VideoStream(config['cam']).start()

        with open(self.kelas, "r") as f:
            classes = f.read().strip().split('\n')\

        colors = np.random.uniform(0, 255, size=(len(classes), 3))
        
        while True:
            # time.sleep(delay)
            
            hasFrame, image = self.cap.read() # opencv
            print(self.cap.read())
            # image = cap.read() # imutils
            
            if image is None:
                image = np.zeros((1020,480,3), dtype=np.uint8)
                continue
            
            Width = image.shape[1]
            Height = image.shape[0]

            if self.inputQueue.full():
                continue
            else:
                self.inputQueue.put(image)

            if not self.outputQueue.empty():
                self.detections = self.outputQueue.get()
            
            # Showing informations on the screen
            class_ids = []
            confidences = []
            boxes = []

            if self.detections is not None:
                
                for out in self.detections:	
                    for detection in out:
                        scores = detection[5:]
                        class_id = np.argmax(scores)
                        confidence = scores[class_id]
                        
                        if confidence > 0.6:
                            
                            center_x = int(detection[0] * Width)
                            center_y = int(detection[1] * Height)
                            w = int(detection[2] * Width)
                            h = int(detection[3] * Height)
                            x = center_x - w / 2
                            y = center_y - h / 2
                            class_ids.append(class_id)
                            confidences.append(float(confidence))
                            boxes.append([x,y,w,h])
                        

                indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
                
                for i in range(len(boxes)):
                    for i in indices:
                        box = boxes[i]
                        x = box[0]
                        y = box[1]
                        w = box[2]
                        h = box[3]	
                        draw_pred(classes, colors, image, class_ids[i], confidences[i], round(x), round(y), round(x+w), round(y+h))              
                
                self.frameQueue.put(image)
    
    def output(self):
        prevTime = 0
        context = zmq.Context()
        footage_socket = context.socket(zmq.PUB)
        footage_socket.bind(f"tcp://*:{self.port}")
        
        while True:
            # time.sleep(delay)
            if self.frameQueue.empty() !=True:
                image = self.frameQueue.get()
                currTime = time.time()
                fps = 1 / (currTime - prevTime)
                prevTime = currTime
                cv2.putText(image, str(round(fps,2)), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1) #FPS Value
                    
                self.var_manager['image'] = image
                
                print('')
                print("PROCESS DETEKSI : ", self.var_manager['time_process'])
                print("QUEUE Input ", self.inputQueue.qsize())
                # print("QUEUE Frame ", frameQueue.qsize())
                print("FPS:", fps)
                
                image = cv2.resize(image,(720, 420))
                encoded, buffer = cv2.imencode('.jpg', image)
                jpg_as_text = base64.b64encode(buffer)
                footage_socket.send(jpg_as_text)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
    def run(self):
        print("[INFO] starting process...")
        self.p_detect = Process(target=self.detect)
        self.p_classify_frame = Process(target=self.classify_frame)
        self.p_output = Process(target=self.output)
        
        self.p_classify_frame.start()
        self.p_detect.start()
        self.p_output.start()
        
        self.p_detect.join()
        self.p_classify_frame.join()
        self.p_output.join()
    
    def close(self):
        self.p_classify_frame.terminate()
        self.p_output.terminate()
        self.p_detect.terminate()

