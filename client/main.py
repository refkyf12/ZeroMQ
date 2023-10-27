from AnalyticClient import AnalyticClient
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
    },
    {
        "ip": "localhost",
        "port": "6661",
        "rtsp": "rtsp://admin:rastek123@10.50.0.15/cam/realmonitor?channel=1&subtype=00",
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
        tempAnalytic.run()
        listAnalytic.append(tempAnalytic)