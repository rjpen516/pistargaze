from django.shortcuts import render
import subprocess
# Create your views here.



import datetime
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics

from .serializers import CommandSerializer, GPSSerializer

import gpsd
import json


class Position(APIView):
	serializer_class = GPSSerializer
	def get(self, request, format=None):
		gpsd.connect()
		packet = gpsd.get_current()
		loc = packet.position()
		time = packet.get_time()
		data = {'longitude':loc[0], 'latitude':loc[1], 'lock_fixed':True, 'datetime': time.strftime("%m/%d/%Y, %H:%M:%S")}

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