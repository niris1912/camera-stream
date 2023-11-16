from django.shortcuts import render
from django.conf import settings
import threading
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import logging
import os
import cv2

class CameraStream(threading.Thread):
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

cstream = CameraStream()
cstream.start()
logger = logging.getLogger(__name__)

@gzip.gzip_page
def camera_stream(request):
    def generate():
        while True:
            frame = cstream.get_frame()
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')


def video_stream(request):
    def stream():
        # Open the video file in binary read mode
        index = 0
        video_path = settings.MEDIA_ROOT + '/testing_video.mp4'
        if os.path.exists(video_path):
            logger.debug('Video file exists')
        else:
            logger.debug('Video file doesn\'t exist')
        
        with open(video_path, 'rb') as file:
            logger.debug(f'Frame Index: {index}')
            while True:
                chunk = file.read(1024)  # Read a chunk of the video file
                if not chunk:
                    break
                yield chunk  # Yield the chunk of data as a generator

    response = StreamingHttpResponse(stream(), content_type='video/mp4')
    response['Content-Disposition'] = 'inline; filename="video.mp4"'
    return response

