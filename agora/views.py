import time
from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from agora_token_builder import RtcTokenBuilder
from .serializers import AgoraTokenSerializer
from accounts.models import UserRegistration
from accounts.models import Consultation


# Create your views here.
class AgoraTokenView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = AgoraTokenSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.validated_data)
            health_worker_id = serializer.validated_data['health_worker_id']
            try:
                health_worker_id = int(health_worker_id)  # Convert to integer
                health_worker = UserRegistration.objects.get(id=health_worker_id)
                print(health_worker)
                print(health_worker.user.healthworker_info)
                print(health_worker.user.healthworker_info.is_available)
            except ValueError:
                return Response({'error': 'Invalid health worker ID'}, status=400)
            if health_worker.user.healthworker_info is None:
                return Response({'error': 'Health worker info not found'}, status=404)

            if not health_worker.user.healthworker_info.is_available:  # Check if health worker is available:
                return Response({'error': 'Health worker is not available'}, status=400)
            channel = serializer.validated_data['channel']
            print(channel)
            uid = serializer.validated_data['uid']
            print(uid)
            app_id = settings.AGORA_APP_ID
            app_certificate = settings.AGORA_APP_CERTIFICATE
            channel_name = channel
            uid = uid
            role = 1
            expiration_time_in_seconds = 3600
            current_time = int(time.time())
            privilege_expired_ts = current_time + expiration_time_in_seconds

            token = RtcTokenBuilder.buildTokenWithUid(
                app_id, app_certificate, channel_name, uid, role, privilege_expired_ts)
            print(token)
            print(app_id)

            consultation = Consultation.objects.create(
                health_worker=health_worker.user,
                patient=request.user,
                channel_name=channel,
                uid=uid,
                token=token,
                app_id=app_id
            )

            return Response(
                {'consultation_id': consultation.id, 'channel_name': channel, 'uid': uid, 'token': token,
                 'app_id': app_id})
        else:
            return Response(serializer.errors, status=400)


class GetConsultationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            consultation = Consultation.objects.filter(health_worker=request.user).latest('created_at')

            if consultation.health_worker != request.user:
                return Response({'error': 'You are not authorized to view this consultation'}, status=403)
            return Response({'channel': consultation.channel_name, 'uid': consultation.uid,
                             'patient_name': consultation.patient.userregistration.first_name,
                             'token': consultation.token, 'app_id': consultation.app_id})
        except Consultation.DoesNotExist:
            return Response({'error': 'Consultation not found'}, status=404)
