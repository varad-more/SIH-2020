from rest_framework import viewsets
from . import models
from . import serializers

class corpactiondata_viewset(viewsets.ModelViewSet):
    queryset = models.corp_action_data.objects.all()
    serializer_class = serializers.corpactiondata_serialiser()
