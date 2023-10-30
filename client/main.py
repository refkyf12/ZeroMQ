from AnalyticClient import AnalyticClient
import requests
import json

# urlApi = ""
# params = {'key':'value'}
# r = requests.get(url= urlApi, params= params)
# response = r.json()

dataKameraLean = [
    {
        "ip": "localhost",
        "port": "6660",
        "rtsp": "rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00",
        "status": 1,
        "lokasi_kamera": "Bundaran Senayan",
    },
]

dataKameraPeopleCounting = [
    {
        "ip": "localhost",
        "port": "6661",
        "rtsp": "rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00",
        "status": 1,
        "lokasi_kamera": "Polda",
    },
]

with open('../config/configModel.json', 'r') as config_file:
    config = json.load(config_file)

if __name__ == "__main__":
    listAnalytic = []
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