# http://www.chioka.in/python-live-video-streaming-example/
# http://pythonhosted.org/Flask-Classy/
# http://flask.pocoo.org/docs/0.12/quickstart/

# RESTful!

from Queue import Queue
from threading import Thread

import cv2
import numpy as np
from flask import Flask, Response
from flask.ext.classy import FlaskView, route

from imutils.video.pivideostream import PiVideoStream


class StreamingAndWebApi:
    def __init__(self):
        self.streamingBuffer = self.StreamingBuffer()

        self.app = Flask(__name__)
        self.WebApiView(self.streamingBuffer).register(self.app, route_base='/', subdomain='api')
        self.app.run(host='0.0.0.0', port=5000, debug=True)

    class WebApiView(FlaskView):
        def __init__(self, streamingBuffer):
            super(StreamingAndWebApi.WebApiView, self).__init__()  # this is python 2 so ...
            self.streamingBuffer = streamingBuffer

        @route('/video_feed')
        def video_feed(self):
            return Response(self.streamingBuffer.gen(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')

    class StreamingBuffer:
        def __init__(self):
            self.video = PiVideoStream(resolution=(854, 480), framerate=30)
            self.video.start()

            # self.pushing = True
            # t = Thread(target=self.push(), args=())
            # t.daemon = True
            # t.start()

            # self.frame_queue = Queue()
            # self.last_frame = self.encode(np.zeros((854, 480, 3), np.uint8))

        def __del__(self):
            self.pushing = False

        @staticmethod
        def encode(frame):
            return cv2.imencode('.jpg', frame)

        # def push(self):
        #     while self.pushing:
        #         if self.frame_queue.qsize() > 128:
        #             self.frame_queue.get_nowait()
        #         frame = self.encode(self.frame_queue.get())
        #         self.frame_queue.put(frame)
        #         self.last_frame = frame

        def gen(self):
            while True:
                # if self.frame_queue.empty():
                #     frame = self.last_frame
                # else:
                #     frame = self.frame_queue.get()
                frame = self.encode(self.video.read())
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')

        # def putNewFrame(self, cv2Frame):
        #     self.frame_queue.put(cv2Frame)
