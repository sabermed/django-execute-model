from django.http import Http404
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import VideoSerializer

class GetVideoResult(generics.CreateAPIView):
    serializer_class = VideoSerializer

    def post(self, request, *args, **kwargs):
      serializer = self.serializer_class(data=request.data)
      serializer.is_valid(raise_exception=True)
      material = serializer.validated_data['material']
      quantity = serializer.validated_data['quantity']
      # Perform multiplication
      result = [material] * quantity

      return Response(
        {
        'result': result,
        'message': 'success',
        'status': True,
        }, status=status.HTTP_200_OK)
