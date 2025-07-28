from rest_framework import serializers
from sistema_pei.peis_sync.models import AppVersion

class AppVersionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppVersion
        fields = ['version', 'releaseDate']
