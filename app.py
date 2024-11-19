from flask import Flask, render_template, Response
from picamera2 import Picamera2
import cv2

app = Flask(__name__)

# Initialize and configure the Picamera2
picam2 = Picamera2()
picam2.configure(picam2.create_video_configuration())

# Function to generate frames for the video feed
def generate_frames():
    while True:
        frame = picam2.capture_array()
        if frame is None:
            continue  # Skip if no frame is captured
        else:
            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                continue
            frame = buffer.tobytes()
            # Yield the frame to the browser
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Route for the homepage
@app.route('/')
def index():
    return render_template('index.html')  # Ensure 'index.html' is in the 'templates' folder

# Route for the video feed
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Route for the gallery page
@app.route('/gallery')
def gallery():
    return render_template('gallery.html')  # Ensure 'gallery.html' is in the 'templates' folder

# Run the application
if __name__
