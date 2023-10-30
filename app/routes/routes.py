from flask import Blueprint, render_template, Response, redirect, request
from app.configs.stream import streamer
from subprocess import Popen
import json

zr = Blueprint('zeromq_routes', __name__)

with open('app/configs/config.json', 'r') as config_file:
    config = json.load(config_file)

def gen(id):
  camera = list(filter(lambda x: x["id"] == int(id), config["cameras"]))[0]
#   print(camera)
  while True:
      stream = streamer(camera["address"])
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream + b'\r\n\r\n')

@zr.route('/')
def index():
    cameras = {}
    for camera in config["cameras"]:
     if camera["lokasi_kamera"] in cameras:
        cameras[camera["lokasi_kamera"]].append(camera["id"])
     else:
        cameras[camera["lokasi_kamera"]] = [camera["id"]]
    return render_template('index.html', cameras=cameras)

@zr.route('/manage')
def manage():
    return render_template('manage.html', cameras=config["cameras"])

@zr.route('/manage/create', methods=["POST"])
def manageCreate():
    return redirect("/manage")

@zr.route('/manage/edit', methods=["POST"])
def manageEdit():
    return redirect("/manage")

@zr.route('/manage/delete/<key>', methods=["DELETE"])
def manageDelete(key):
    return redirect("/manage")

@zr.route('/lean-detection')
def lean():
    return render_template('lean.html')

@zr.route('/jump-detection')
def jump():
    return render_template('jump.html')

@zr.route('/stream/<id>')
def camera(id):
    return Response(gen(id), mimetype='multipart/x-mixed-replace; boundary=frame')
