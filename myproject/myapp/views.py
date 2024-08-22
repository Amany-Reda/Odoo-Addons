from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import MySerializer

class MyView(APIView):
    def get(self, request):
        # Your API logic here
        return Response({'message': 'Hello, World!'})