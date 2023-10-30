import json
from flask import Flask, render_template, Response, redirect, request
from app.configs.stream import streamer
from subprocess import Popen

app = Flask(__name__, static_folder='app/static/', template_folder='app/templates')
app.static_folder = 'app/static'
with open('app/configs/config.json', 'r') as config_file:
    config = json.load(config_file)

if __name__ == '__main__':
    from app.routes.routes import zr 
    # runProcess = [Popen([config["python_env"], f"client/{config['cameras'][key]['client']}"]) for key in config["cameras"].keys() if config["cameras"][key]["status"] == 1]
    app.register_blueprint(zr)
    app.run(debug=True, host="0.0.0.0")