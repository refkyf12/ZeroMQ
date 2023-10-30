from analyticclient import AnalyticClient
import requests

# urlApi = ""
# params = {'key':'value'}
# r = requests.get(url= urlApi, params= params)
# response = r.json()

dataKamera = [
    {
        "ip": "localhost",
        "port": "6660",
        "rtsp": "rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00",
        "deployment": "../analytics/models/Deployment-JPO People detection",
        "tmp": "../static/tmp/people_counting/",
        "det_duration": 5,
        "status": 1,
        "lokasi_kamera": "Bundaran Senayan",
    },
]

if __name__ == "__main__":
    listAnalytic = []
    for kamera in dataKamera:
        print(kamera["ip"])
        tempAnalytic = AnalyticClient()
        tempAnalytic.setIp(kamera["ip"])
        tempAnalytic.setPort(kamera["port"])
        tempAnalytic.setRtsp(kamera["rtsp"])
        tempAnalytic.setDeployment(kamera["deployment"])
        tempAnalytic.setTmp(kamera["tmp"])
        tempAnalytic.setDetDuration(kamera["det_duration"])
        tempAnalytic.setStatus(kamera["status"])
        tempAnalytic.setLokasiKamera(kamera["lokasi_kamera"])
        tempAnalytic.start()
        listAnalytic.append(tempAnalytic)