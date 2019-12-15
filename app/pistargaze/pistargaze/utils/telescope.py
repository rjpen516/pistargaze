from datetime import datetime

import point




class TelescopeRunner(object):
	def __init__(self,LOCAL_NON_PI, tty='/dev/ttyUSB1'):

		if LOCAL_NON_PI:
			print("In Simulation Mode")
		else:
			print("Using telescope")

		self.az = 0
		self.alt = 0
		self.rate = 0
		self.axis = "az"
		self.longs = 0
		self.lat = 0
		self.time = datetime.now()
		self.LOCAL_NON_PI = LOCAL_NON_PI
		self.last_api_call_time = datetime.now()
		try:
			self.telescope_serial = point.nexstar.NexStar(tty)
		except Exception:
			print("Error setting up the serial data")

	def get_azalt(self):

		if self.LOCAL_NON_PI:
			#add logic to use the time now to simulate rate
			return (self.az,self.alt)
		else:
			return self.telescope_serial.get_azalt()

	def slew_fixed(self,axis,rate):

		if self.LOCAL_NON_PI:
			print("moving telescope on axis: {0} and rate {1}".format(axis,rate))
			last_api_call_time = datetime.now()
			self.rate = rate
			self.axis = axis

			if axis == "az":
				self.az = (self.az + rate) %360

			else:
				alt = rate + self.alt 

				if alt > 180:
					self.alt = 180
				elif alt < -180:
					self.alt = -180
				else:
					self.alt = alt

		else:
			return self.telescope_serial.slew_fixed(axis,rate)


	def get_location(self):

		if self.LOCAL_NON_PI:
			print("getting location {0}{1}".format(self.longs,self.lat))
			#we need to use logoic to get the position of telescope
			return [self.longs, self.lat]
		else:
			return self.telescope_serial.get_location()


	def set_location(self,longs, lat):
		if self.LOCAL_NON_PI:
			self.longs = longs
			self.lat = lat

		else:
			self.telescope_serial.set_location(longs,lat)

	def set_time(self,time):
		if self.LOCAL_NON_PI:
			self.time = time
		else:
			self.telescope_serial.set_time(time)


	def get_time(self):
		if self.LOCAL_NON_PI:
			return datetime.timestamp(self.time)
		else:
			self.telescope_serial.get_time()