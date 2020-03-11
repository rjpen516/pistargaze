from django.db import models

# Create your models here.


class Stars(models.Model):
	name = models.CharField(max_length=128)

class Session(models.Model):
	name = models.CharField(max_length=128)
	stars = models.ManyToManyField(Stars)






class Photo(models.Model):
	session = models.ManyToManyField(Session)
	token = models.TextField()
	file = models.TextField()
	loc_long = models.DecimalField(decimal_places=5, max_digits=10)
	loc_lat = models.DecimalField(decimal_places=5, max_digits=10)
	time = models.DateTimeField(auto_now_add=True)
