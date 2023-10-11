from rest_framework import serializers
from complaints.models import Complain

class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'
