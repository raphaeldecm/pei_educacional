from rest_framework import serializers


class SUAPTokenSerializer(serializers.Serializer):
    suap_token = serializers.CharField()
