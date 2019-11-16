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


class UtilsPower(APIView):
	serializer_class = CommandSerializer

	def post(self, request, format=None):

		serializer =CommandSerializer(data=request.data)

		if serializer.is_valid():

			command = serializer.data['command']
			param = serializer.data['param']



			if command == "shutdown":
				output = "now"
				if int(param) > 0:
					output = str(param)



				subprocess.run(["shutdown", "-h", output])

