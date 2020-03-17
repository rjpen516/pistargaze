from django.db import models
import uuid

# Create your models here.


class Stars(models.Model):
	name = models.CharField(max_length=128)

class Session(models.Model):
	name = models.CharField(max_length=128)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	stars = models.ManyToManyField(Stars)
	note = models.TextField()
	date = models.DateTimeField(auto_now_add=True)
	location = models.TextField()


class KVStore(models.Model):
	key = models.CharField(max_length=128)
	value = models.TextField()



class Photo(models.Model):
	session = models.ManyToManyField(Session)
	token = models.TextField()
	file = models.TextField()
	loc_long = models.DecimalField(decimal_places=5, max_digits=10)
	loc_lat = models.DecimalField(decimal_places=5, max_digits=10)
	time = models.DateTimeField(auto_now_add=True)
