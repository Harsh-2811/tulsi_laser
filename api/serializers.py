from rest_framework import serializers
from complaints.models import Complain, ComplainOutcome
from django_filters import rest_framework as filters
from customers.models import Machine, Customer
from users.models import Technician


class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = ['status']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'


class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = Technician
        fields = '__all__'


class ComplainSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    machine = MachineSerializer()
    technician = TechnicianSerializer()

    class Meta:
        model = Complain
        fields = '__all__'


class ComplainOutcomeSerializer(serializers.ModelSerializer):
    complain = ComplainSerializer(source='complain', read_only=True)
    technician = TechnicianSerializer(source='technician', read_only=True)

    class Meta:
        model = ComplainOutcome
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']


class ComplainOutcomeCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ComplainOutcome
        # fields = '__all__'
        exclude = ['created_at', 'updated_at']