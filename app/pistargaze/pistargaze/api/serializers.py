from rest_framework import serializers
import datetime

from .models import Session


class CommandSerializer(serializers.Serializer):
	command = serializers.RegexField("(shutdown)|(restart)", max_length=150,help_text="Command such as shutdown or restart")
	param = serializers.IntegerField(help_text="How long should we wait, in seconds")


class GPSSerializer(serializers.Serializer):
	longitude = serializers.FloatField()
	latitude = serializers.FloatField()
	lock_fixed = serializers.BooleanField()
	datetime = serializers.DateTimeField()

class MovementSerializer(serializers.Serializer):
	axis = serializers.RegexField("(az)|(alt)")
	rate = serializers.IntegerField(max_value=9, min_value=-9)



class CaptureSerializer(serializers.Serializer):
	subid = serializers.IntegerField(min_value=0)



class CaptureCalibrate(serializers.Serializer):
	subid = serializers.IntegerField(min_value=0)
	latitude = serializers.FloatField()
	longitude = serializers.FloatField()
	altitude = serializers.FloatField()
	datetime = serializers.DateTimeField()


class CameraCaptureApi(serializers.Serializer):
	expose = serializers.IntegerField(min_value=0, max_value=1000)



class SessionNew(serializers.Serializer):
	name = serializers.CharField()
	loc_long = serializers.FloatField()
	loc_lat = serializers.FloatField()
	date = serializers.DateTimeField(required=False, read_only=True)
	current = serializers.BooleanField(required=False, read_only=True)
	pk = serializers.CharField(required=False, read_only=True)
	#stars = serializers.IntegerField()

	def create(self, validated_data):
		data = Session()
		data.name = validated_data['name']
		data.loc_long = validated_data['loc_long']
		data.loc_lat = validated_data['loc_lat']
		current = True
		data.save()
		return data


class SessionQuery(serializers.Serializer):
	pk = serializers.CharField()


