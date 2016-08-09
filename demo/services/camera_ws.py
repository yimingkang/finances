import argparse
import base64
import hashlib
import os
import time
import threading
import webbrowser
import datetime

try:
    import cStringIO as io
except ImportError:
    import io

import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback


class WebSocket(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
	return True

    def on_message(self, message):
        """Evaluates the function pointed to by json-rpc."""

        # Start an infinite loop when this is called
        if message == "read_camera":
            self.camera_loop = PeriodicCallback(self.loop, 10)
	    print "Starting camera!"
            self.camera_loop.start()

        # Extensibility for other methods
        else:
            print("Unsupported function: " + message)

    def on_close(self):
	print "Stopping camera!"
	self.camera_loop.stop()

    def loop(self):
        """Sends camera images in an infinite loop."""
        sio = io.StringIO()

    	camera.capture(sio, "jpeg", use_video_port=True)

        try:
            self.write_message(base64.b64encode(sio.getvalue()))
        except tornado.websocket.WebSocketClosedError:
            self.camera_loop.stop()

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description="Starts a webserver that "
					 "connects to a webcam.")
	parser.add_argument("--port", type=int, default=8000, help="The "
			    "port on which to serve the website.")
	parser.add_argument("--resolution", type=str, default="low", help="The "
			    "video resolution. Can be high, medium, or low.")
	args = parser.parse_args()

	import picamera
	camera = picamera.PiCamera()
	#camera.start_preview()

	resolutions = {"high": (1280, 720), "medium": (640, 480), "low": (320, 240)}
	if args.resolution in resolutions:
		camera.resolution = resolutions[args.resolution]
	else:
	    raise Exception("%s not in resolution options." % args.resolution)

	handlers = [(r"/websocket", WebSocket)]
	application = tornado.web.Application(handlers)
	application.listen(args.port)

	webbrowser.open("http://localhost:%d/" % args.port, new=2)

	tornado.ioloop.IOLoop.instance().start()
