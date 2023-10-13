from flask import Flask, render_template, Response
from stream import streamer


app = Flask(__name__, static_folder='../static/')
app.static_folder = 'static'

CAMERAS = [
   (1, "tcp://10.200.0.161:5555"),
   (2, "tcp://localhost:6666"),
   (3, "tcp://localhost:7777"),
   (4, "tcp://localhost:8888"),
   (5, "tcp://10.200.0.219:9999"),
   (6, "tcp://10.200.0.219:9991"),
   (7, "tcp://10.200.0.219:9992"),
   (8, "tcp://localhost:9993"),
   (9, "tcp://localhost:9994"),
   (10, "tcp://localhost:9995"),
   (11, "tcp://localhost:9996"),
   (12, "tcp://localhost:9997")
]

def gen(id):
  print([item[1] for item in CAMERAS if item[0] == int(id)])
  while True:
      stream = streamer([item[1] for item in CAMERAS if item[0] == int(id)][0])
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream + b'\r\n\r\n')

@app.route('/')
def index():
  return render_template('/index.html')

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
    app.run(debug=True, host="0.0.0.0")