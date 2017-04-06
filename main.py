# http://www.chioka.in/python-live-video-streaming-example/
# http://pythonhosted.org/Flask-Classy/
# http://flask.pocoo.org/docs/0.12/quickstart/

# RESTful!

import cv2
from flask import Flask, Response, render_template
from flask.ext.classy import FlaskView, route

from imutils.video.pivideostream import PiVideoStream


class StreamingAndWebApi(object):
    def __init__(self):
        self.app = Flask(__name__)
        print(__name__)
        self.WebApiView.register(self.app, route_prefix='/api/')
        self.app.run(host='0.0.0.0', port=5000, debug=True)

    class WebApiView(FlaskView):
        def __init__(self):
            super(StreamingAndWebApi.WebApiView, self).__init__()  # this is python 2 so ...
            self.streamingBuffer = StreamingBuffer.getInstance()
            print(self.streamingBuffer)

        @route('/')
        def index(self):
            return render_template('index.html')

        @route('/video_feed')
        def video_feed(self):
            return Response(self.streamingBuffer.gen(),
                            mimetype='multipart/x-mixed-replace; boundary=frame')


class StreamingBuffer:
    _INSTANCE = None
    _RUNNING = True

    @staticmethod
    def getInstance():
        if StreamingBuffer._INSTANCE is None:
            StreamingBuffer._INSTANCE = StreamingBuffer()
        return StreamingBuffer._INSTANCE

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
        video = PiVideoStream(framerate=30)
        video.start()
        while StreamingBuffer._RUNNING:
            # if self.frame_queue.empty():
            #     frame = self.last_frame
            # else:
            #     frame = self.frame_queue.get()
            frame = self.encode(video.read())
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame.tobytes() + b'\r\n\r\n')

            # def putNewFrame(self, cv2Frame):
            #     self.frame_queue.put(cv2Frame)
        video.stop()


if __name__ == '__main__':
    StreamingBuffer.getInstance()
    StreamingAndWebApi()
