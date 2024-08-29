from rest_framework.response import Response
from rest_framework.views import APIView
from .ai_response import ai_response, googleai_response
from rest_framework.permissions import IsAuthenticated
from .serializers import PromptSerializer

# Create your views here.


class AiResponseView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PromptSerializer(data=request.data)
        if serializer.is_valid():
            prompt = serializer.validated_data['prompt']
            response = googleai_response(prompt)
            return Response({'response': response})
        else:
            return Response(serializer.errors, status=400)
