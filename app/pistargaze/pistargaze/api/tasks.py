
# Create your tasks here
from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .models import Photo, Session

from pistargaze.utils.CaptureBridge import CaptureBridge

import hashlib
from datetime import datetime




@shared_task
def add(x, y):
	return x + y



@shared_task
def run_simple_expose(number, delay):

	capture = CaptureBridge()


	for iteration in range(0,number):

		now = datetime.now()
		m = hashlib.sha256()
		m.update("{0}".format(now.strftime("%m/%d/%Y, %H:%M:%S")).encode())

		filename_hex = m.hexdigest()

		photoFile = capture.capture("{0}.cr2".format(filename_hex))

		time.sleep(delay)



