from django.shortcuts import render
import cv2
import threading
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

class VideoStream(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.cap = cv2.VideoCapture(0)  # Use 0 or -1 to select the default camera
        self.lock = threading.Lock()

    def run(self):
        while True:
            ret, frame = self.cap.read()
            with self.lock:
                self.frame = frame

    def get_frame(self):
        with self.lock:
            return self.frame

video_stream = VideoStream()
video_stream.start()

@gzip.gzip_page
def camera_stream(request):
    def generate():
        while True:
            frame = video_stream.get_frame()
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')

