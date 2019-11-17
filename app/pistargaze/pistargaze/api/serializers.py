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
	