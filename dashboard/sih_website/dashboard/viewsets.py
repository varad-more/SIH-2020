from rest_framework import viewsets
# from dashboard.models import corp_action_data, file_download
from dashboard.models import *
# from .serializers import corpactiondata_serialiser,filedownload_serialiser
from .serializers import *

class corpactiondata_viewset(viewsets.ModelViewSet):
    queryset = corp_action_data.objects.all()
    serializer_class = corpactiondata_serialiser

class filedownload_viewset(viewsets.ModelViewSet):
    queryset = file_download.objects.all()
    serializer_class = filedownload_serialiser

class articles_viewset(viewsets.ModelViewSet):
    queryset = articles.objects.all()
    serializer_class = articles_serialiser

class dashboard_viewset(viewsets.ModelViewSet):
    queryset = dashboard.objects.all()
    serializer_class = dashboard_serialiser

class securities_viewset(viewsets.ModelViewSet):
    queryset = securities.objects.all()
    serializer_class = securities_serialsier


