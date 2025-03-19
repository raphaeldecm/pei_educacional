from rest_framework import serializers

from sistema_pei.academics.models import Enrollment


class EnrollmentUpdateDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Enrollment
        fields = "__all__"
