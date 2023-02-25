from flask import Flask, Response
import cv2

app = Flask(__name__)

# Create a VideoCapture object to read from the camera
cap = cv2.VideoCapture(0)

# Define a route for the video stream
@app.route('/video_feed')
def video_feed():
    def generate():
        while True:
            # Read a frame from the camera
            ret, frame = cap.read()

            # Check if the frame was successfully read
            if not ret:
                break

            # Convert the frame to JPEG format
            ret, jpeg = cv2.imencode('.jpg', frame)

            # Yield the JPEG-encoded frame
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    # Return a response containing the video stream
    return Response(generate(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)