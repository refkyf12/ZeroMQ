import configs

def send_mqtt(img_path, img_name, count):
    import paho.mqtt.client as mqtt
    import json
    
    print("MQTT Start")
    
    _image_ = imgToBase64(img_path + img_name)
    _camera_id_ = configs.CAM_ID
    _count_ = count
    _timestamp_ = timestamp("%Y-%m-%d %H:%M:%S")
    
    broker_address = configs.MQTT_HOST
    port = configs.MQTT_PORT
    username = configs.MQTT_USERNAME
    password = configs.MQTT_PASSWORD
    topic_pub = configs.MQTT_TOPIC
    
    client = mqtt.Client()
    client.username_pw_set(username, password)
    code = client.connect(broker_address, port, 30)

    msg = {
            "camera_id": _camera_id_,
            "analytic_id" : configs.DETECTION_ID,
            "count": _count_,
            "image": _image_,
            "timestamp": _timestamp_
    }
    
    if code == 0:
        print("MQTT Connected successfully ")
        
        client.loop_start()
        while True:
            client.publish(topic_pub, json.dumps(msg), qos=0, retain=False)
            print("MQTT message sent")
            client.disconnect()
            
            break
    else:
        print("MQTT Bad connection. Code: ", code)
        client.disconnect()

    client.disconnect()
    clearFolder(img_path)
    print("MQTT Disconnected")

def timestamp(format):
    from datetime import datetime

    timestamp = datetime.now()
    formatted_timestamp = timestamp.strftime(format)

    return str(formatted_timestamp)

# def writeLog(msg):
#     with open(configs.LOG_FILE, 'a') as file:
#         file.write(str(msg) + "\n")
        
def imgToBase64(path):
    import base64

    with open(path, 'rb') as image_file:
        image_binary = image_file.read()

    base64_image = base64.b64encode(image_binary).decode('utf-8')

    return base64_image

def clearFolder(path):
    import os
    import shutil
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
            os.mkdir(path)
        else:
            print(f"The folder '{path}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")
       