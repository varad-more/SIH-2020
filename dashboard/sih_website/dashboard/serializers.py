from rest_framework import serializers
# from dashboard.models import articles,corp_action_data,file_download
from dashboard.models import *
class corpactiondata_serialiser(serializers.ModelSerializer):
    class Meta:
        model = corp_action_data
        fields = ('__all__')  

class filedownload_serialiser(serializers.ModelSerializer):
    class Meta:
        model = file_download
        fields = ('__all__')

class articles_serialiser(serializers.ModelSerializer):
    class Meta:
        model = articles
        fields = ('__all__')

class dashboard_serialiser(serializers.ModelSerializer):
    class Meta:
        model = dashboard
        fields = ('__all__')

class securities_serialsier(serializers.ModelSerializer):
    class Meta:
        model = securities_master
        fields = ('__all__')
         



