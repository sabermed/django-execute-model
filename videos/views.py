from django.http import Http404
from rest_framework import generics, status, parsers
from rest_framework.response import Response
from .serializers import VideoSerializer

class GetVideoResult(generics.CreateAPIView):
    serializer_class = VideoSerializer
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        material = serializer.validated_data['material']
        quantity = serializer.validated_data['quantity']

        # Check if a video file was included in the request
        video_file = request.FILES.get('video')

        if video_file:
            # Perform video upload logic here (save the file, process it, etc.)
            # For example, you can save the file to the media directory
            # and include the file URL in the response
            video_url = save_video_file(video_file)
            message = f'Video uploaded successfully. URL: {video_url}'
            status_code = status.HTTP_200_OK
        else:
            message = 'No video file included in the request.'
            status_code = status.HTTP_400_BAD_REQUEST

        # Perform multiplication
        result = [material] * quantity

        return Response(
            {
                'result': result,
                'message': message,
                'status': status_code == status.HTTP_200_OK,
            }, status=status_code)

def save_video_file(video_file):
    # Logic to save the video file, for example, using default storage or a custom function
    # For simplicity, let's assume saving in the media directory
    import os
    from django.conf import settings
    media_path = os.path.join(settings.MEDIA_ROOT, 'videos')
    os.makedirs(media_path, exist_ok=True)
    file_path = os.path.join(media_path, video_file.name)
    with open(file_path, 'wb+') as destination:
        for chunk in video_file.chunks():
            destination.write(chunk)
    # Return the URL to access the saved file
    return os.path.join(settings.MEDIA_URL, 'videos', video_file.name)
