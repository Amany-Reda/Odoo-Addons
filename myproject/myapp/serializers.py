from rest_framework import serializers

class MySerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)