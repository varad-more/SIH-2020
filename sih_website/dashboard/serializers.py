from rest_framework import serializers
from dashboard.models import corp_action_data

class corpactiondata_serialiser(serializers.ModelSerializer):
    class Meta:
        model = corp_action_data
        fields = ('__all__')  