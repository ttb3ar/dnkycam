from flask import Flask, render_template, Response
from picamera2 import Picamera2
import io
import time
import cv2

app = Flask(__name__)

picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())

def generate_frames():
    while True:
        # Capture an image
        frame = picam2.capture_array()
        if frame is None:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    

@app.route('/')
def index():
    return render_template('index.html')  # Make sure index.html is in the 'templates' folder

@app.route('/videofeed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    picam2.start()
    app.run(host='0.0.0.0', port=5000)
