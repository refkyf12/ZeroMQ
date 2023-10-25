import json
from flask import Flask, render_template, Response, redirect, request
from stream import streamer
from subprocess import Popen

with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)

app = Flask(__name__, static_folder='../static/')
app.static_folder = 'static'
runProcess = []

# CAMERAS = [
#    (1, "tcp://10.200.0.161:5555"),
#    (2, "tcp://localhost:6666"),
#    (3, "tcp://localhost:7777"),
#    (4, "tcp://localhost:8888"),
#    (5, "tcp://10.200.0.219:9999"),
#    (6, "tcp://10.200.0.219:9991"),
#    (7, "tcp://10.200.0.219:9992"),
#    (8, "tcp://localhost:9993"),
#    (9, "tcp://localhost:9994"),
#    (10, "tcp://localhost:9995"),
#    (11, "tcp://localhost:9996"),
#    (12, "tcp://localhost:9997")
# ]

def gen(id):
  print([config["cameras"][key]["address"] for key in config["cameras"].keys() if config["cameras"][key]["id"] == int(id)])
  while True:
      stream = streamer([config["cameras"][key]["address"] for key in config["cameras"].keys() if config["cameras"][key]["id"] == int(id)][0])
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream + b'\r\n\r\n')

@app.route('/')
def index():
  global runProcess
  if len(runProcess) > 0:
    for process in runProcess:
      process.kill()

  runProcess = [Popen([config["python_env"], f"client/{config['cameras'][key]['client']}"]) for key in config["cameras"].keys() if config["cameras"][key]["status"] == 1]
  
  cameras = {}
  for key in config["cameras"].keys():
    if config["cameras"][key]["lokasi_kamera"] in cameras:
      cameras[config["cameras"][key]["lokasi_kamera"]].append(config["cameras"][key]["id"])
    else:
      cameras[config["cameras"][key]["lokasi_kamera"]] = [config["cameras"][key]["id"]]
  return render_template('/index.html', cameras=cameras)

@app.route('/manage')
def manage():
  global runProcess
  if len(runProcess) > 0:
    for process in runProcess:
      process.kill()
      
  return render_template('/manage.html', cameras=config["cameras"])

@app.route('/manage/create', methods=["POST"])
def manageCreate():
  newId = len(config["cameras"].keys())+1
  newKey = "camera_" + str(newId)
  config["cameras"][newKey] = {
    'id': newId,
    'rtsp_url': request.form.get('rtsp'),
    'zmq_address': request.form.get('zmq'),
    'address': request.form.get('address'),
    'status': int(request.form.get('status')),
    'lokasi_kamera': request.form.get('lokasi_kamera'),
    'client': request.form.get('client_kamera')
  }

  with open('config/config.json', 'w') as f:
    json.dump(config, f)

  return redirect("/manage")

@app.route('/manage/edit', methods=["POST"])
def manageEdit():
  key = request.form.get('key')
  config["cameras"][key] = {
    'id': config["cameras"][key]['id'],
    'rtsp_url': request.form.get('rtsp'),
    'zmq_address': request.form.get('zmq'),
    'address': request.form.get('address'),
    'status': int(request.form.get('status')),
    'lokasi_kamera': request.form.get('lokasi_kamera'),
    'client': request.form.get('client_kamera')
  }

  with open('config/config.json', 'w') as f:
    json.dump(config, f)

  return redirect("/manage")

@app.route('/manage/delete/<key>', methods=["DELETE"])
def manageDelete(key):
  del config['cameras'][key]

  with open('config/config.json', 'w') as f:
    json.dump(config, f)

  return redirect("/manage")

@app.route('/lean-detection')
def lean():
  return render_template('/lean.html')

@app.route('/jump-detection')
def jump():
  return render_template('/jump.html')

@app.route('/stream/<id>')
def camera(id):
  return Response(gen(id), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
  # runProcess = [Popen([config["python_env"],f"{config["client"]["client_folder"]}{client}"]) for client in config["client"]["clients"]]

  app.run(debug=True, host="0.0.0.0")