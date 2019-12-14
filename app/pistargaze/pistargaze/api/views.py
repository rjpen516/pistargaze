from django.shortcuts import render
import subprocess
# Create your views here.

import time



from datetime import datetime
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
import time

from .serializers import CommandSerializer, GPSSerializer, MovementSerializer

import gpsd
import json

from django.conf import settings






class CommandTelescope(APIView):
	serializer_class = MovementSerializer

	def get(self,request, format=None):
		try:
			settings.TELESCOPE_LOCK.acquire()
			azimuth, altitude = settings.TELESCOPE.get_azalt()
			settings.TELESCOPE_LOCK.release()


			data = {'azimuth': azimuth, 'altitude': altitude}
			return Response(data)

		except Exception as e:
			print(e)
			settings.TELESCOPE_LOCK.release()
			return Response({'azimuth': 0, 'altitude': 0})

	def post(self, request, format=None):
		serializer =MovementSerializer(data=request.data)

		if serializer.is_valid():
			rate = serializer.data['rate']
			axis = serializer.data['axis']

			settings.TELESCOPE_LOCK.acquire()
			settings.TELESCOPE.slew_fixed(axis,rate)
			#time.sleep(.2)
			settings.TELESCOPE_LOCK.release()

			return Response({'status':"ok"})

class Position(APIView):
	serializer_class = GPSSerializer
	def get(self, request, format=None):
		try:
			gpsd.connect()
			packet = gpsd.get_current()
			loc = packet.position()
			time = packet.get_time()
			satdata = packet.get_sat()
			data = {'satdata': satdata,'longitude':loc[0], 'latitude':loc[1], 'lock_fixed':True, 'datetime': time.strftime("%m/%d/%Y, %H:%M:%S")}
		except Exception:
			data = {'satdata': [],'longitude':0, 'latitude':0, 'lock_fixed':False, 'datetime': ""}



		return Response(data)


class TelescopeStatus(APIView):
	def get(self,request,format=None):
		try:
			settings.TELESCOPE_LOCK.acquire()


			loc = settings.TELESCOPE.get_location()
			time = settings.TELESCOPE.get_time()
			az,alt = settings.TELESCOPE.get_azalt()
				#time.sleep(.2)
			settings.TELESCOPE_LOCK.release()

			python_time = datetime.fromtimestamp(time)


			data = {'az':az,'alt':alt,'latitude': loc[0], 'longitude': loc[1], 'datetime': python_time.strftime("%m/%d/%Y, %H:%M:%S")}
		except Exception as e:
			print(e)
			settings.TELESCOPE_LOCK.release()
			data = {'az':0, 'alt':0,'latitude': 0, 'longitude': 0, 'datetime': ""}

		return Response(data)

class SyncGPS(APIView):
	def post(self, request, format=None):
		try:
			gpsd.connect()
			packet = gpsd.get_current()
			loc = packet.position()
			time = packet.get_time()

			settings.TELESCOPE_LOCK.acquire()

			settings.TELESCOPE.set_location(loc[0],loc[1])
			settings.TELESCOPE.set_time(datetime.timestamp(time))
			settings.TELESCOPE_LOCK.release()

			data = {'error': False, 'message': 'GPS Sync'}


		except Exception:
			settings.TELESCOPE_LOCK.release()
			data = {'error': True, 'message': 'GPS Error'}

		return Response(data)


class UtilsPower(APIView):
	serializer_class = CommandSerializer

	def post(self, request, format=None):

		serializer =CommandSerializer(data=request.data)
		#print(serializer.data)
		if serializer.is_valid():

			command = serializer.data['command']
			param = serializer.data['param']



			if command == "shutdown":
				output = "now"
				if int(param) > 0:
					output = str(param)



				file = open("/shutdown_signal/signal","w+")
				file.write("shutdown")
				file.close()

				return Response('', status=status.HTTP_202_ACCEPTED)

			elif command == "restart":
				output = "now"
				if int(param) > 0:
					output = str(param)



				file = open("/shutdown_signal/signal","w+")
				file.write("restart")
				file.close()

				return Response('', status=status.HTTP_202_ACCEPTED)
		return Response('', status=status.HTTP_400_BAD_REQUEST)