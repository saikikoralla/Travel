from rest_framework import serializers
from .models import User_Packages

class UserPackageSerializer(serializers.ModelSerializer):

    class Meta:
        model = User_Packages
        fields = ['deal_id', 'no_of_persons', 'total_cost', 'date']
        read_only_fields = ['total_cost','user','date','package'] 