from rest_framework.response import Response
from rest_framework.views import APIView
from .ai_response import ai_response
from rest_framework.permissions import IsAuthenticated
from .serializers import PromptSerializer

# Create your views here.


class AiResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PromptSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']
            user = request.user
            health_info = user.health_info.health_conditions
            if health_info is None:
                health_info = "None"
            response = ai_response(prompt, health_info)
            return Response({'response': response})
        else:
            return Response(serializer.errors, status=400)
