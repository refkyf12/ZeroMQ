import AnalyticClient

dataKamera = [
    {
        "ip": "localhost",
        "port": "6660",
        "rtsp": "rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00",
    },
    {
        "ip": "localhost",
        "port": "6661",
        "rtsp": "rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00",
    },
    {
        "ip": "localhost",
        "port": "6662",
        "rtsp": "rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00",
    },
    {
        "ip": "localhost",
        "port": "6663",
        "rtsp": "rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00",
    },
    {
        "ip": "localhost",
        "port": "6664",
        "rtsp": "rtsp://admin:rastek123@10.50.0.13/cam/realmonitor?channel=1&subtype=00",
    },
]

if __name__ == "__main__":
    listAnalytic = []
    for kamera in dataKamera:
        tempAnalytic = AnalyticClient()
        tempAnalytic.setIp(kamera["ip"])
        tempAnalytic.setPort(kamera["port"])
        tempAnalytic.setRtsp(kamera["rtsp"])
        tempAnalytic.run()
        listAnalytic.append(tempAnalytic)