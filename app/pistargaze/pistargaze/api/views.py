from django.shortcuts import render
import subprocess
# Create your views here.

import time

import os



from datetime import datetime
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import generics
import time

from .serializers import CommandSerializer, GPSSerializer, MovementSerializer, CaptureSerializer, CaptureCalibrate, CameraCaptureApi

import gpsd
import json


from django.shortcuts import HttpResponse
from django.conf import settings

from requests_toolbelt.multipart.encoder import MultipartEncoder
import requests


from astropy.coordinates import EarthLocation,SkyCoord
from astropy.time import Time
from astropy import units as u
from astropy.coordinates import AltAz
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
from pprint import pprint

import rawpy
import imageio



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



class CaptureLatest(APIView):
	def get(self, request, format=None):


		#this fucntion will always return the latest image that we have, else it will return the error photo


		image_data = open(os.path.join(settings.ROOT_DIR,"pistargaze/static/images/error_message.png"), "rb").read()
		return HttpResponse(image_data,content_type="image/png")


class CaptureAnalysis(APIView):
	def get(self, request, format=None):


		#in this method we will run our sky finder, and return out a job session id that we can query until the result is done. It will use the latest image in the capture queue 

		image_data = open(os.path.join(settings.ROOT_DIR,"pistargaze/static/images/img1.jpg"), "rb")


		#we gotta auth to our local version of nova 
		request_json = {"publicly_visible": "y", "allow_modifications": "y", "allow_commercial_use": "y"}

		multipart_data = MultipartEncoder( 
 	    fields={ 
	     'request-json': json.dumps(request_json), 
	     'file': ('image.jpg', image_data, 'application/octet-stream') 
	    })   

		response = requests.post("http://nova:8000/api/upload", data=multipart_data, headers={'Content-Type': multipart_data.content_type}) 
		try:
			return_object = json.loads(response.text)
		except Exception:
			return Response({'result':'pending'})

		if 'subid' in return_object.keys():
			return Response({'result':'processing', 'subid': return_object['subid']})
		else:
			return Response(return_object,content_type="application/json")


class CaptureData(APIView):

	def get(self, request, format=None):

		if request.query_params.get('subid') is not None:
			try:
				subid = request.query_params.get('subid')
				result = requests.get("http://nova:8000/api/jobs/{0}".format(subid))
			except Exception:
				return Response({'success': False, 'message': 'pending backend API', 'backend': result.text }) 

			if result.status_code == 404:
				return Response({'success': False, 'message': 'pending'})

			status = json.loads(result.text)

				

			if status['status'] == 'success':
				objects_in_field = json.loads(requests.get("http://nova:8000/api/jobs/{0}/info".format(subid)).text)
				annotations =  json.loads(requests.get("http://nova:8000/api/jobs/{0}/annotations".format(subid)).text)


				images = {'annotated_image': 'http://localhost:8001/annotated_display/{0}'.format(subid), 
						  }


				output = {'success': True,
						'objects_in_field': objects_in_field, 
						'annotations': annotations, 
						 'images': images}

				return Response(output)
			return Response({'success': False, 'message': 'solving'})
		return Response({'success': False, 'message': "invalid subid"}, content_type="application/json")


class CaptureCalabration(APIView):

	serializer_class = CaptureCalibrate


	def post(self,request,format=None):


		serializer = CaptureCalibrate(data=request.data)


		if serializer.is_valid():

			#print(serializer['subid'])

			info =  json.loads(requests.get("http://nova:8000/api/jobs/{0}/info".format(serializer['subid'].value)).text)


			observing_location = EarthLocation(lat=serializer['latitude'].value*u.deg, lon=serializer['longitude'].value*u.deg, height=serializer['altitude'].value*u.m)  
			observing_time = serializer['datetime'].value
			aa = AltAz(location=observing_location, obstime=observing_time)

			coord = SkyCoord(ra=info['calibration']['ra']*u.degree, dec=info['calibration']['dec']*u.degree)
			altaz =coord.transform_to(aa)

			#print("Telescope's Altitude = {0.alt:.2}\n Telescope's Az = {0.az:.2}\n".format(altaz))
			settings.TELESCOPE_LOCK.acquire()
			self.TELESCOPE.sync(info['calibration']['ra'], info['calibration']['dec'])
			settings.TELESCOPE_LOCK.release()




			return Response({'alt': altaz.alt.value, 'az':altaz.az.value})




class CameraStream(APIView):

	def get(self, request, format=None):
		pid = settings.CAMERA_CONTROL.status()
		return Response({'success': True, 'pid': pid})


	def post(self, request, format=None):
		settings.CAMERA_CONTROL.startVideoStream()


		return Response({'success': True})

	def delete(self, request, format=None):

		settings.CAMERA_CONTROL.stopVideoStream()

		return Response({'success': True})




class CameraCapture(APIView):


	serializer_class = CameraCaptureApi


	def post(self, request, fortmat=None):

		serializer = CameraCaptureApi(data=request.data)

		if serializer.is_valid():

			#first we need to see if we are streaming, if so, lets stop that crap
			pid = settings.CAMERA_CONTROL.status()

			if pid == "status":
				return Response({'status': False, 'message': 'Stack still booting up'})

			elif pid != "" and int(pid) > 0:
				settings.CAMERA_CONTROL.stopVideoStream()


			#now that we are in an expected state, lets go make a capture

			photoFile = settings.CAMERA_CONTROL.capture("filename.cr2")

			with rawpy.imread(photoFile) as raw:
				thumb = raw.extract_thumb()
			if thumb.format == rawpy.ThumbFormat.JPEG:
    			# thumb.data is already in JPEG format, save as-is
    			with open('/data/capture/current.jpg', 'wb') as f:
        			f.write(thumb.data)
			elif thumb.format == rawpy.ThumbFormat.BITMAP:
   				# thumb.data is an RGB numpy array, convert with imageio
    			imageio.imsave('/data/capture/current.jpg', thumb.data)



			return Response({'status': True, 'photoFile': photoFile})

		return Response({'status': False, 'message': 'invalid input'})
