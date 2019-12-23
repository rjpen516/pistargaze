import os




class CaptureBridge(obj):
	def __init__(self):
		self.path = '/var/run/videostream/signal'
		self.video_state = "not_capturing"



		self.approved_iso = [100,200,400,800,1200,1800,]

	def startVideoStream(self):

		if self.video_state == "not_capturing":
			self.video_state = "capturing"
			signal = file.open(self.path,"w+")
			signal.write("stream")
			signal.close()
		return "ok"

	def stopVideoStream(self):
		if self.video_state == "capturing":
			signal = file.open(self.path,"w+")
			signal.write("stopstream")
			signal.close()
		return "ok"

	def setISO(self, iso_value):

		if iso_value in self.approved_iso:
			signal = file.open(self.path,'w+')
			signal.write("iso\n{0}".format(iso_value))
			signal.close()
			return "ok"
		else:
			return "error"


	def setShutterSpeed(self, shutterspeed):
		signal = file.open(self.path,'w+')
		signal.write("shutterspeed\n{0}".format(shutterspeed))
		signal.close()

		return "ok"

	def setImageFormat(self, imageformat):
		signal = file.open(self.path, 'w+')
		signal.write("imageformat\n{0}".format(imageformat))
		signal.close()

		return "ok"

	def capture(self, bulb_expose=0):
		signal = file.open(self.path, 'w+')
		signal.write("imageformat\n{0}".format(bulb_expose))
		signal.close()

	
