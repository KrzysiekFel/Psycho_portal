from rest_framework.viewsets import generics
from rest_framework.permissions import IsAuthenticated
from .serializers import PsychoTestSerializer


class CreatePsychoTest(generics.CreateAPIView):
    serializer_class = PsychoTestSerializer
    permission_classes = [IsAuthenticated]
