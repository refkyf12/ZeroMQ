import requests
import json
import threading

from analyticclient import AnalyticClient

# urlApi = ""
# params = {'key':'value'}
# r = requests.get(url= urlApi, params= params)
# response = r.json()

dataKameraLean = [
    {
        "ip": "localhost",
        "port": "6660",
        "rtsp": "/home/refky/websocket/live-stream-zeromq/testVideo/1.avi",
        "status": 1,
        "lokasi_kamera": "Bundaran Senayan",
    },
]

dataKameraPeopleCounting = [
    {
        "ip": "localhost",
        "port": "6661",
        "rtsp": "/home/refky/websocket/live-stream-zeromq/testVideo/1.avi",
        "status": 1,
        "lokasi_kamera": "Polda",
    },
]

with open('../config/configModel.json', 'r') as config_file:
    config = json.load(config_file)


def run_dataKameraLean():
    for kamera in dataKameraLean:
        detection = "lean"
        model = list(filter(lambda x: x["detection"] == detection, config["model"]))[0]
        deployment = model["deployment"]
        tmp = model["tmp"]
        det_duration = model["det_duration"]
        print(kamera["ip"])
        tempAnalytic = AnalyticClient()
        tempAnalytic.setIp(kamera["ip"])
        tempAnalytic.setPort(kamera["port"])
        tempAnalytic.setRtsp(kamera["rtsp"])
        tempAnalytic.setDeployment(deployment)
        tempAnalytic.setTmp(tmp)
        tempAnalytic.setDetDuration(det_duration)
        tempAnalytic.setStatus(kamera["status"])
        tempAnalytic.setLokasiKamera(kamera["lokasi_kamera"])
        tempAnalytic.start()
        listAnalytic.append(tempAnalytic)

def run_dataKameraPeopleCounting():
    for kameraPeople in dataKameraPeopleCounting:
        detection = "people_counting"
        model = list(filter(lambda x: x["detection"] == detection, config["model"]))[0]
        deployment = model["deployment"]
        tmp = model["tmp"]
        det_duration = model["det_duration"]
        print(kameraPeople["port"])
        peopleCounting = AnalyticClient()
        peopleCounting.setIp(kameraPeople["ip"])
        peopleCounting.setPort(kameraPeople["port"])
        peopleCounting.setRtsp(kameraPeople["rtsp"])
        peopleCounting.setDeployment(deployment)
        peopleCounting.setTmp(tmp)
        peopleCounting.setDetDuration(det_duration)
        peopleCounting.setStatus(kameraPeople["status"])
        peopleCounting.setLokasiKamera(kameraPeople["lokasi_kamera"])
        peopleCounting.start()
        listAnalytic.append(peopleCounting)
        


if __name__ == "__main__":
    listAnalytic = []
    
    thread_dataKameraLean = threading.Thread(target=run_dataKameraLean)
    thread_dataKameraPeopleCounting = threading.Thread(target=run_dataKameraPeopleCounting)

    thread_dataKameraLean.start()
    thread_dataKameraPeopleCounting.start()

    thread_dataKameraLean.join()
    thread_dataKameraPeopleCounting.join()