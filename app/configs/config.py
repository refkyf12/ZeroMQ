import requests


# configure data cameras from backend

urlApiSensor = 'http://202.180.16.237:28080/master/api/sensor'
urlApiCamera = 'http://202.180.16.237:28080/master/api/camera'
dataKameraPeopleCounting = []
dataKameraLean = []
dataKameraJump = []
dataKamera =[]

def getDataKameraPeopleCount():
    #Get Data People Count Cam
    params = {'analyticId':'PPLCNT'}
    r = requests.get(url= urlApiSensor, params= params)
    response = r.json()

    response_data = response['data']
    cam_ids = [item['camId'] for item in response_data]

    for cam_id in cam_ids:
        params = {'id': cam_id}
        r = requests.get(url=urlApiCamera, params=params)
        response_people_count = r.json()

        for item in response_people_count['data']:
            dataKameraPeopleCounting.append(item)
    return dataKameraPeopleCounting

def getDataKameraPeopleLean():
    #Get Data Lean Cam
    params = {'analyticId':'PPLLEN'}
    r = requests.get(url= urlApiSensor, params= params)
    response = r.json()

    response_data = response['data']
    cam_ids = [item['camId'] for item in response_data]

    for cam_id in cam_ids:
        params = {'id': cam_id}
        r = requests.get(url=urlApiCamera, params=params)
        response_lean = r.json()

        for item in response_lean['data']:
            dataKameraLean.append(item)
    return dataKameraLean

def getDataKameraPeopleJump():
    #Get Data Jump Cam
    params = {'analyticId':'PPLJMP'}
    r = requests.get(url= urlApiSensor, params= params)
    response = r.json()

    response_data = response['data']
    cam_ids = [item['camId'] for item in response_data]

    for cam_id in cam_ids:
        params = {'id': cam_id}
        r = requests.get(url=urlApiCamera, params=params)
        response_lean = r.json()

        for item in response_lean['data']:
            dataKameraJump.append(item)
    return dataKameraJump

def getDataKamera():
    #GetAllDataCamera
    r = requests.get(url= urlApiCamera)
    response_allcam = r.json()
    for item in response_allcam['data']:
        dataKamera.append(item)

    return dataKamera


