from django.contrib.auth import get_user_model
from rest_framework import serializers
from accounts.models import UserRegistration, HealthInfo, HealthWorkerInfo
from django.contrib.auth.hashers import make_password

User = get_user_model()


class HealthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthInfo
        fields = ('pregnancy_status', 'due_date', 'health_conditions')


class UserRegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    health_info = HealthInfoSerializer(source='user.health_info', read_only=True)
    role = serializers.CharField()

    class Meta:
        model = UserRegistration
        fields = (
            'id', 'username', 'password', 'first_name', 'last_name', 'phone_number', 'role', 'gender',
            'date_of_birth', 'health_info',
        )

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            password=make_password(validated_data['password'])
        )

        user_registration = UserRegistration.objects.create(
            user=user,
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
            phone_number=validated_data.get('phone_number'),
            role=validated_data.get('role'),
            gender=validated_data.get('gender'),
            date_of_birth=validated_data.get('date_of_birth')
        )

        return user_registration


class HealthWorkerInfoSerializer(serializers.ModelSerializer):
    user_registration = serializers.SerializerMethodField()

    class Meta:
        model = HealthWorkerInfo
        fields = ['user_registration', 'medical_license_number', 'specialty', 'hospital_name', 'clinic_location',
                  'is_verified', 'is_available']

    def get_user_registration(self, obj):
        user_registration = UserRegistration.objects.get(user=obj.user)
        return UserRegistrationSerializer(user_registration).data


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
