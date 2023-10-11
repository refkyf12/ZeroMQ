from flask import Flask, render_template, Response
from stream import streamer

app = Flask(__name__)
CAMERAS = [
   (1, "tcp://localhost:5555"),
   (2, "tcp://localhost:6666")
]

def gen(id):
  print([item[1] for item in CAMERAS if item[0] == int(id)])
  while True:
      stream = streamer([item[1] for item in CAMERAS if item[0] == int(id)][0])
      yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + stream + b'\r\n\r\n')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/stream/<id>')
def camera(id):
  return Response(gen(id), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)