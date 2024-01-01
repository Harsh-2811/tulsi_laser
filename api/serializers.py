from rest_framework import serializers
from complaints.models import Complain, ComplainOutcome
from customers.models import Machine, Customer
from users.models import Technician
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
    
class UpdateStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complain
        fields = ['status']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class MachineSerializer(serializers.ModelSerializer):
    machine_type = serializers.SlugRelatedField(slug_field='_type', read_only = True)
    purchase_date = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Machine
        fields = '__all__'

    def get_purchase_date(self, instance):
        return (instance.purchase_date if instance.purchase_date else '')

class TechnicianSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only = True)
    class Meta:
        model = Technician
        fields = '__all__'

    def get_name(self, instance):
        return instance.user.first_name


class ComplainSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer()
    machine = MachineSerializer()
    technician = TechnicianSerializer()

    class Meta:
        model = Complain
        fields = '__all__'


class ComplainOutcomeSerializer(serializers.ModelSerializer):
    complain = ComplainSerializer(read_only=True)
    technician = TechnicianSerializer(read_only=True)

    class Meta:
        model = ComplainOutcome
        fields = '__all__'
        # exclude = ['created_at', 'updated_at']


class ComplainOutcomeCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComplainOutcome
        fields = '__all__'
        # exclude = ['created_at', 'updated_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data
    
class FCMSerializer(serializers.Serializer):
    fcm_token = serializers.CharField(required=True)