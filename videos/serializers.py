from rest_framework import serializers

class VideoSerializer(serializers.Serializer):
  material = serializers.CharField(max_length=100)
  quantity = serializers.IntegerField()