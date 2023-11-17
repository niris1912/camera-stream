from django.conf import settings
import threading
import json
import time
import logging
import os
import cv2

from django.http import StreamingHttpResponse
from django.views.decorators import gzip
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

class CameraStream(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.frame = None
        self.cap = cv2.VideoCapture(0)  # Use 0 or -1 to select the default camera
        self.lock = threading.Lock()
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.capturing = False
        self.out = None

    def run(self):
        while True:
            ret, frame = self.cap.read()
            with self.lock:
                self.frame = frame

    def get_frame(self):
        with self.lock:
            return self.frame
        
    def start_capture(self):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        fname = settings.MEDIA_ROOT + "/" + now + ".mp4"
        logger.debug('output: ' + fname)
        fps = self.cap.get(cv2.CAP_PROP_FPS)
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.out = cv2.VideoWriter(fname, self.fourcc, fps, (width, height))
        thread = threading.Thread(target=write_frame_to_file)
        thread.daemon = False  # Set the thread as a daemon (will stop when the main thread stops)
        thread.start()

    def stop_capture(self):
        self.out.release()

    def set_capturing(self, _capturing):
        self.capturing = _capturing

def write_frame_to_file():
    logger.debug("Capturing: %s", cStream.capturing)
    while cStream.capturing:
        success, frame = cStream.cap.read()
        logger.debug("success: %s", success)
        if success:
            cStream.out.write(frame)

cStream = CameraStream()
cStream.start()
logger = logging.getLogger('my_custom_logger')

@gzip.gzip_page
def camera_stream(request):
    def generate():
        while True:
            frame = cStream.get_frame()
            _, jpeg = cv2.imencode('.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')

    return StreamingHttpResponse(generate(), content_type='multipart/x-mixed-replace; boundary=frame')


def video_stream(request):
    def stream():
        # Open the video file in binary read mode
        video_path = settings.MEDIA_ROOT + '/testing_video.mp4'
        if os.path.exists(video_path):
            logger.debug('Video file exists')
        else:
            logger.debug('Video file doesn\'t exist')
        
        with open(video_path, 'rb') as file:
            while True:
                chunk = file.read(1024)  # Read a chunk of the video file
                if not chunk:
                    break
                yield chunk  # Yield the chunk of data as a generator

    response = StreamingHttpResponse(stream(), content_type='video/mp4')
    response['Content-Disposition'] = 'inline; filename="video.mp4"'
    return response

@csrf_exempt
def capture_stream(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body.decode('utf-8'))
            action = json_data.get('action')
           
            if action == 'start':
                if cStream.capturing:
                    return JsonResponse({'status': False,  'message': 'Capturing has already been started.'})
                else:
                    cStream.capturing = True
                    cStream.start_capture()
                    return JsonResponse({'status': True})
            
            elif action == 'stop':
                if not cStream.capturing:
                    return JsonResponse({'status': False,  'message': 'Capturing has not been started.'})
                else:
                    cStream.capturing = False
                    cStream.stop_capture()
                    return JsonResponse({'status': True})
                
            elif action == 'restart':
                if cStream.capturing:
                    cStream.capturing = False
                    cStream.stop_capture()

                time.sleep(0.05)
                cStream.capturing = True
                cStream.start_capture()
                return JsonResponse({'status': True})

            return JsonResponse({'status': False, 'message': 'Your request is not correct.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)
    else:
        return JsonResponse({'error': 'Only POST requests allowed'}, status=405)