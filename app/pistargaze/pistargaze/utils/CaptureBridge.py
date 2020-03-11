import os
import time

import os.path




class CaptureBridge(object):
	def __init__(self):
		self.path = '/var/run/videostream/signal'
		self.video_state = "not_capturing"



		self.approved_iso = [100,200,400,800,1200,1800,]

	def startVideoStream(self):

		if self.video_state == "not_capturing":
			self.video_state = "capturing"
			signal = open(self.path,"w+")
			signal.write("stream")
			signal.close()
		return "ok"

	def stopVideoStream(self):
		if self.video_state == "capturing":
			signal = open(self.path,"w+")
			self.video_state = "not_capturing"
			signal.write("stopstream")
			signal.close()
		return "ok"

	def setISO(self, iso_value):

		if iso_value in self.approved_iso:
			signal = open(self.path,'w+')
			signal.write("iso\n{0}".format(iso_value))
			signal.close()
			return "ok"
		else:
			return "error"


	def setShutterSpeed(self, shutterspeed):
		signal = open(self.path,'w+')
		signal.write("shutterspeed\n{0}".format(shutterspeed))
		signal.close()

		return "ok"

	def setImageFormat(self, imageformat):
		signal = open(self.path, 'w+')
		signal.write("imageformat\n{0}".format(imageformat))
		signal.close()

		return "ok"

	def capture(self, filename=""):
		signal = open(self.path, 'w+')
		signal.write("capture\n{0}".format(filename))
		signal.close()

		while True:
			if os.path.isfile('/data/capture/new/{0}'.format(filename)):
				break
			else:
				time.sleep(.1)

		time.sleep(.1) #there is a timming condition where the file might not be fully written to disk before we return. 

		return '/data/capture/new/{0}'.format(filename)

	def status(self):
		signal = open(self.path, 'w+')
		signal.write("status")
		signal.close()
		time.sleep(.1)
		pid = open(self.path,'r+').read().strip()

		return pid


