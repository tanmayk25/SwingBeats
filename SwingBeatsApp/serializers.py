#Setting up the DRF Serializers for Rest API
from rest_framework import serializers
from .models import Monitored_Detail

#The serializers will convert the Monitored_data model into JSON that will be used by the API to return the data to the user.
class MonitoredSerializer(serializers.ModelSerializer):
   class Meta:
       model = Monitored_Detail
       fields = ('device_id', 'heart_rate', 'steps', 'calories', 'dance_duration')
