from rest_framework import serializers
import datetime


class CommandSerializer(serializers.Serializer):
	command = serializers.CharField(max_length=150)
	param = serializers.IntegerField()