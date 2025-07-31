from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from sistema_pei.peis_sync.models import AppVersion
from .serializers import AppVersionSerializer
from packaging import version

class LatestAppVersionView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        all_versions = AppVersion.objects.all()
        if not all_versions.exists():
            return Response({"detail": "Nenhuma versão disponível."}, status=404)

        latest = max(all_versions, key=lambda v: version.parse(v.version))
        serializer = AppVersionSerializer(latest)
        return Response(serializer.data)
