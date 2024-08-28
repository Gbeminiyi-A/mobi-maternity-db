from rest_framework import serializers
from accounts.models import Consultation


class AgoraTokenSerializer(serializers.Serializer):
    channel = serializers.CharField()
    uid = serializers.IntegerField()
    health_worker_id = serializers.IntegerField()


class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'
