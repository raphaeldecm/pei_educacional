from django.urls import path

from sistema_pei.peis_sync.views import PeisSyncView

app_name = "peis_sync"
urlpatterns = [
    path("app/", PeisSyncView.as_view(), name="app"),
]
