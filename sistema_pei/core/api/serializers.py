from rest_framework import serializers


class SUAPTokenSerializer(serializers.Serializer):
    token = serializers.CharField()
    code = serializers.CharField()
