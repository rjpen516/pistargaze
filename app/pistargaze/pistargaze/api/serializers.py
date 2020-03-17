from rest_framework import serializers
import datetime


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
	note = serializers.CharField()
	location = serializers.CharField()