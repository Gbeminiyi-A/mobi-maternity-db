from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from accounts.models import UserRegistration, HealthInfo, HealthWorkerInfo
from api.serializers import UserRegistrationSerializer, HealthInfoSerializer, LoginSerializer, \
    HealthWorkerInfoSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.contrib.auth import authenticate
from django.contrib.auth import login, logout
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationViewSet(viewsets.ModelViewSet):
    queryset = UserRegistration.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    http_method_names = ['post']

    def create(self, request, *args, **kwargs):
        print("Request data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserDetailViewSet(viewsets.ModelViewSet):
    queryset = User.objects.none()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        return UserRegistration.objects.filter(user=user)


class HealthInfoRegistrationViewSet(viewsets.ModelViewSet):
    queryset = HealthInfo.objects.none()
    serializer_class = HealthInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def get_queryset(self):
        user = self.request.user
        return HealthInfo.objects.filter(user=user)

    def put(self, request):
        user = request.user
        if user.userregistration.role != 'P':
            raise PermissionDenied("You are not authorized to perform this action.")
        try:
            health_info, created = HealthInfo.objects.get_or_create(user=user)
            health_info.pregnancy_status = request.data.get('pregnancy_status', health_info.pregnancy_status)
            health_info.due_date = request.data.get('due_date', health_info.due_date)
            health_info.health_conditions = request.data.get('health_conditions', health_info.health_conditions)
            health_info.save()
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if created:
            message = 'Health information created successfully'
        else:
            message = 'Health information updated successfully'
        return Response({'message': message})


class HealthDetailViewSet(viewsets.ModelViewSet):
    queryset = HealthInfo.objects.none()
    serializer_class = HealthInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        if user.userregistration.role != 'P':
            raise PermissionDenied("You are not authorized to perform this action.")
        return HealthInfo.objects.filter(user=user)


class HealthWorkerInfoRegistrationViewSet(viewsets.ModelViewSet):
    queryset = HealthWorkerInfo.objects.none()
    serializer_class = HealthWorkerInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['put']

    def get_queryset(self):
        user = self.request.user
        return HealthWorkerInfo.objects.filter(user=user)

    def put(self, request):
        user = self.request.user
        if user.userregistration.role != 'H':
            raise PermissionDenied("You are not authorized to perform this action.")
        try:
            health_worker_info, created = HealthInfo.objects.get_or_create(user=user)
            health_worker_info.medical_license_number = request.data.get('medical_license_number',
                                                                         health_worker_info.medical_license_number)
            health_worker_info.specialty = request.data.get('specialty', health_worker_info.specialty)
            health_worker_info.clinic_location = request.data.get('clinic_location', health_worker_info.clinic_location)
            health_worker_info.hospital_name = request.data.get('clinic_name', health_worker_info.hospital_name)
            health_worker_info.save()
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        if created:
            message = 'Health Records created successfully'
        else:
            message = 'Health Records updated successfully'
        return Response({'message': message})


class HealthWorkerDetailViewSet(viewsets.ModelViewSet):
    queryset = HealthWorkerInfo.objects.none()
    serializer_class = HealthWorkerInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        user = self.request.user
        if user.userregistration.role != 'H':
            raise PermissionDenied("You are not authorized to perform this action.")
        return HealthWorkerInfo.objects.filter(user=user)


class HealthWorkerListViewSet(viewsets.ModelViewSet):
    queryset = HealthWorkerInfo.objects.none()
    serializer_class = HealthWorkerInfoSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        return HealthWorkerInfo.objects.filter(user__userregistration__role='H')


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        # Debug: print credentials
        print(f"Username: {username}, Password: {password}")

        user = authenticate(request, username=username, password=password)

        # Debug: check if user was authenticated
        if user is None:
            print("User authentication failed")
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        login(request, user)
        try:
            user_registration = UserRegistration.objects.get(user=user)
            serializer = UserRegistrationSerializer(user_registration)
            print({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful', 'data': serializer.data, })
            if user.userregistration.role == 'H':
                user.healthworker_info.is_available = True
                user.healthworker_info.save()
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'Login successful', 'data': serializer.data,
            }, status=status.HTTP_200_OK)
        except UserRegistration.DoesNotExist:
            return Response({'message': 'Login successful, but user registration not found'}, status=status.HTTP_200_OK)


class BlacklistRefreshView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Clear the session data for the authenticated user
            if request.user.userregistration.role == 'H':
                request.user.healthworker_info.is_available = False
                request.user.healthworker_info.save()
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
