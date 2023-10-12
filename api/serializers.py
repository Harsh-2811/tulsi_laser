from rest_framework import serializers
from complaints.models import Complain, ComplainOutcome
from django_filters import rest_framework as filters


class ComplainFilter(filters.FilterSet):
    class Meta:
        model = Complain
        fields = {
            'status': ['exact'],
        }


class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = ['status']


class ComplainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = '__all__'


class ComplainOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplainOutcome
        fields = '__all__'
