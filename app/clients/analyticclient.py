import sys
import logging
import imutils
import dlib
import json
import os
import time
import cv2
import zmq
import base64
import configs.helper as helper

sys.path.append('/home/rastekid/Projects/GETI/Code')
sys.path.insert(0, '../')
from analytics.trackers.centroidtracker import CentroidTracker
from analytics.trackers.trackableobject import TrackableObject
from imutils.video import FPS
from geti_sdk.deployment import Deployment

logging.basicConfig(level = logging.INFO, format = "[INFO] %(message)s")
logger = logging.getLogger(__name__)

class AnalyticClient:
    port = "6000"
    ip = "127.0.0.1"
    rtsp = 0
    deployment = "../Analytic/Deployment-JPO People detection"
    tmp ="../tmp/people_counting/"
    det_duration = 5
    status = 1
    lokasi_kamera = "Bundaran Senayan"

    def __init__(self):
        self.vs = cv2.VideoCapture(self.rtsp)
    def setPort(self, port):
        self.port = port
    def setIp(self, ip):
        self.ip = ip
    def setRtsp(self, rtsp):
        self.rtsp = rtsp
        self.vs = cv2.VideoCapture(rtsp)
    def setDeployment(self, deployment):
        self.deployment = deployment
    def setTmp(self, tmp):
        self.contmpfig = tmp
    def setDetDuration(self, det_duration):
        self.det_duration = det_duration
    def setStatus(self, status):
        self.status = status
    def setLokasiKamera(self, lokasi_kamera):
        self.lokasi_kamera = lokasi_kamera
    

    def people_counter(self, video_path, offline_deployment):
    
        logger.info("Starting the video..")
        vs = cv2.VideoCapture(video_path)
        
        W = H = None

        ct = CentroidTracker(maxDisappeared=40, maxDistance=50)
        
        trackers = []
        trackableObjects = {}
        totalFrames = 0
        
        fps = FPS().start()
        
        start_time = time.time()
        count = 0
        _alert_ = False
        
        object_id = []
        object_id_tmp = []

        context = zmq.Context()
        footage_socket = context.socket(zmq.PUB)
        footage_socket.bind(f"tcp://*:{self.port}")
        
        while True:
            
            time.sleep(.05)
            
            frame = vs.read()
            frame = frame[1]
            if frame is None:
                break
                
            frame = imutils.resize(frame, width = 2000)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            if W is None or H is None:
                (H, W) = frame.shape[:2]

            rects = []

            if totalFrames % 10 == 0:
                trackers = []
                
                start_time_process = time.time()
                numpy_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                detections = offline_deployment.infer(numpy_rgb)
                end_time_process = time.time()
                
                time_process = end_time_process - start_time_process
                infer_process = "{:.2f}".format(time_process)
                
                # print('INFER PROCCESS : ', infer_process)
                
                for annot in detections.annotations:
                    for lab in annot.labels:
                        scores = lab.probability
                        classId = lab.name
                        
                        confidence = scores
                        if confidence > 0.5 and (classId != 'No Object'):
                            _alert_ = True
                            center_x = int(annot.shape.x * W)
                            center_y = int(annot.shape.y * H)
                            width = int(annot.shape.width * W)
                            height = int(annot.shape.height * H)
                            left = int(center_x - width / 2)
                            top = int(center_y - height / 2)
                            cv2.rectangle(frame, (left, top), (left + width, top + height), (0, 255, 0), 2)
                            
                            tracker = dlib.correlation_tracker()
                            rect = dlib.rectangle(int(annot.shape.x), int(annot.shape.y), int(annot.shape.x+annot.shape.width) , int(annot.shape.y+annot.shape.height))
                            tracker.start_track(numpy_rgb, rect)
                            trackers.append(tracker)

            else:
                for tracker in trackers:
                    
                    tracker.update(rgb)
                    pos = tracker.get_position()
                    startX = int(pos.left())
                    startY = int(pos.top())
                    endX = int(pos.right())
                    endY = int(pos.bottom())
                    rects.append((startX, startY, endX, endY))
                    
            objects = ct.update(rects)

            object_id = []
            for (objectID, centroid) in objects.items():
                to = trackableObjects.get(objectID, None)

                if to is None:
                    to = TrackableObject(objectID, centroid)
                else:
                    to.centroids.append(centroid)

                trackableObjects[objectID] = to
                object_id.append(objectID)
                text = "ID {}".format(objectID)
                cv2.putText(frame, classId, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                cv2.rectangle(frame, (centroid[0] - 10, centroid[1] - 10), (centroid[0] + 10, centroid[1] + 10), (0, 255, 0), 2)

            # print(_alert_)
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            unique_id = set(object_id)
            unique_id_ = list(unique_id)

            diff_unique_id = [item for item in unique_id_ if item not in object_id_tmp]
                

            if _alert_ :
                if elapsed_time >= 1.0:
                    count += 1
                    start_time = current_time
                    
            if count >= self.det_duration :
                
                print(len(objects))
                print('obj sebelumnya : ', object_id_tmp, '| jumlah : ' + str(len(object_id_tmp)))
                print('obj sekarang : ', unique_id_, '| jumlah : ' + str(len(unique_id_)))
                print('diff array : ', diff_unique_id)
                
                object_id_tmp = unique_id_
                
                ts = helper.timestamp("%Y%m%d%H%M%S")
                
                img_name = ts + '.jpg'
                img_path = self.tmp
                obj_count = len(diff_unique_id)
                
                
                ## KIRIM DATA ##
                if obj_count > 0 :
                    cv2.imwrite(img_path + img_name, frame)
                    print(obj_count)
                    
                    # helper.send_mqtt(img_path, img_name, obj_count)
                
                object_id = []
                _alert_ = False
                count = 0

            cv2.putText(frame, str(len(diff_unique_id)), (60, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 5)
            # cv2.imshow("Real-Time Monitoring/Analysis Window", frame)
            
            frame = cv2.resize(frame,(720, 420))
            encoded, buffer = cv2.imencode('.jpg', frame)
            jpg_as_text = base64.b64encode(buffer)
            footage_socket.send(jpg_as_text)
            
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord("q"):
                break
            
            totalFrames += 1
            fps.update()

        fps.stop()
        logger.info("Elapsed time: {:.2f}".format(fps.elapsed()))
        logger.info("Approx. FPS: {:.2f}".format(fps.fps()))

        cv2.destroyAllWindows()
    
    def start(self):
        print("[INFO] loading deployment...")
        
        offline_deployment = Deployment.from_folder(self.deployment)
        offline_deployment.load_inference_models(device="CPU")
        
        self.people_counter(self.rtsp, offline_deployment)