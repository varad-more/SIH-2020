from rest_framework import viewsets
from dashboard.models import corp_action_data
from .serializers import corpactiondata_serialiser

class corpactiondata_viewset(viewsets.ModelViewSet):
    queryset = corp_action_data.objects.all()
    serializer_class = corpactiondata_serialiser
