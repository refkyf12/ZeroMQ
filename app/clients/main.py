import requests
import json
import threading
import sys
from analyticclient import AnalyticClient

sys.path.append("../../")
import app.configs.config as conf

with open('../configs/configModel.json', 'r') as config_file:
    config = json.load(config_file)

dataKamera = conf.getDataKamera()
dataKameraLean = conf.getDataKameraPeopleLean()
dataKameraPeopleCount = conf.getDataKameraPeopleCount()
dataKameraJump = conf.getDataKameraPeopleJump()

# print("data semua kamera",dataKamera)
# print("data semua kamera jump",dataKameraJump)
# print("data semua kamera lean",dataKameraLean)
# print("data semua kamera people count",dataKameraPeopleCount)

def run_dataKameraLean():
    port = 666
    for kamera in dataKameraLean:
        for i in range(len(kamera)):
            detection = "lean"
            model = list(filter(lambda x: x["detection"] == detection, config["model"]))[0]
            deployment = model["deployment"]
            tmp = model["tmp"]
            det_duration = model["det_duration"]
            tempAnalytic = AnalyticClient()
            tempAnalytic.setIp("127.0.0.1")
            tempAnalytic.setPort(int(str(port) + str(i)))
            tempAnalytic.setRtsp(kamera["url"])
            tempAnalytic.setDeployment(deployment)
            tempAnalytic.setTmp(tmp)
            tempAnalytic.setDetDuration(det_duration)
            tempAnalytic.setLokasiKamera(kamera["location"])
            tempAnalytic.start()
            listAnalytic.append(tempAnalytic)

def run_dataKameraJump():
    port = 888
    for kameraJump in dataKameraJump:
        for i in range(len(kameraJump)):
            detection = "jump"
            model = list(filter(lambda x: x["detection"] == detection, config["model"]))[0]
            deployment = model["deployment"]
            tmp = model["tmp"]
            det_duration = model["det_duration"]
            tempAnalytic = AnalyticClient()
            tempAnalytic.setIp("127.0.0.1")
            tempAnalytic.setPort(int(str(port) + str(i)))
            tempAnalytic.setRtsp(kameraJump["url"])
            tempAnalytic.setDeployment(deployment)
            tempAnalytic.setTmp(tmp)
            tempAnalytic.setDetDuration(det_duration)
            tempAnalytic.setLokasiKamera(kameraJump["location"])
            tempAnalytic.start()
            listAnalytic.append(tempAnalytic)

def run_dataKameraPeopleCounting():
    port = 777
    for kameraPeople in dataKameraPeopleCount:
        for i in range(len(kameraPeople)):
            detection = "people_counting"
            model = list(filter(lambda x: x["detection"] == detection, config["model"]))[0]
            deployment = model["deployment"]
            tmp = model["tmp"]
            det_duration = model["det_duration"]
            peopleCounting = AnalyticClient()
            peopleCounting.setIp("127.0.0.1")
            peopleCounting.setPort(int(str(port) + str(i)))
            peopleCounting.setRtsp(kameraPeople["url"])
            peopleCounting.setDeployment(deployment)
            peopleCounting.setTmp(tmp)
            peopleCounting.setDetDuration(det_duration)
            peopleCounting.setLokasiKamera(kameraPeople["location"])
            peopleCounting.start()
            listAnalytic.append(peopleCounting)  


if __name__ == "__main__":
    listAnalytic = []
    
    thread_dataKameraLean = threading.Thread(target=run_dataKameraLean)
    thread_dataKameraPeopleCounting = threading.Thread(target=run_dataKameraPeopleCounting)
    thread_dataKameraJump = threading.Thread(target=run_dataKameraJump)

    thread_dataKameraLean.start()
    thread_dataKameraPeopleCounting.start()
    thread_dataKameraJump.start()

    thread_dataKameraLean.join()
    thread_dataKameraPeopleCounting.join()
    thread_dataKameraJump.join()