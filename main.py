from flask import Flask, render_template, Response
from stream import streamer, streamer2

app = Flask(__name__)

def gen():
  while True:
      stream = streamer()
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream + b'\r\n\r\n')

def gen2():
   while True:
      stream = streamer2()
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream + b'\r\n\r\n')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/camera')
def camera():
  return Response(gen(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera2')
def camera2():
  return Response(gen2(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)