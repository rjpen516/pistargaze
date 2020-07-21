
# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task, task
from .models import Photo, Session

from pistargaze.utils.CaptureBridge import CaptureBridge

import hashlib
from datetime import datetime


import time

import gpsd

import traceback
import sys

import rawpy
import imageio

from PIL import Image
import PIL




@shared_task
def add(x, y):
	return x + y



@task(soft_time_limit=45*60, time_limit=50*60)
def run_simple_expose(number, delay):

	capture = CaptureBridge()

	current_session = Session.objects.get(current=True)


	for iteration in range(0,number):

		now = datetime.now()
		m = hashlib.sha256()
		m.update("{0}".format(now.strftime("%m/%d/%Y, %H:%M:%S")).encode())

		filename_hex = m.hexdigest()

		processing = True

		while processing:
			try:
				photoFile = capture.capture("{0}.cr2".format(filename_hex))
				processing = False


				with rawpy.imread(photoFile) as raw:
					thumb = raw.extract_thumb()
					if thumb.format == rawpy.ThumbFormat.JPEG:
						Image.frombuffer()
						# thumb.data is already in JPEG format, save as-is
						with open('/data/capture/current_large.jpg', 'wb') as f:
							f.write(thumb.data)
					elif thumb.format == rawpy.ThumbFormat.BITMAP:
						# thumb.data is an RGB numpy array, convert with imageio
						imageio.imsave('/data/capture/current_large.jpg', thumb.data)

				basewidth = 300
				img = Image.open('/data/capture/current_large.jpg')

				wpercent = (basewidth / float(img.size[0]))
				hsize = int((float(img.size[1]) * float(wpercent)))
				img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
				img.save('/data/capture/current.jpg')


			except Exception as err:
				print(traceback.format_exc())
				time.sleep(delay)
				pass


		photo_data = Photo()

		photo_data.token = filename_hex
		photo_data.file = '{0}'.format(photoFile)
		loc = None
		try:
			gpsd.connect()
			packet = gpsd.get_current()
			loc = packet.position()
			time_gps = packet.get_time()
		except Exception:
			loc = [0,0]
			time_gps = "00000000"


		photo_data.loc_long = loc[0]
		photo_data.loc_lat = loc[1]
		photo_data.time = time_gps

		photo_data.save()

		photo_data.session.add(current_session.id)

		time.sleep(delay)



