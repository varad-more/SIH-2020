from rest_framework import serializers
from .models import corp_action_data

class corpactiondata_serialiser(serializers.ModelSerializer):
    class meta:
        model = corp_action_data
        fields = '__all__'