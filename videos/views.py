from django.http import Http404
from rest_framework import generics, status, parsers
from rest_framework.response import Response
from .serializers import VideoSerializer

# Import the functions for video processing
from .video_processing import run_yolov8, run_yolov8_segment, create_gait_energy_image

class GetVideoResult(generics.CreateAPIView):
    serializer_class = VideoSerializer
    parser_classes = (parsers.MultiPartParser,)

    def post(self, request, *args, **kwargs):
        # Check if a video file was included in the request
        video_file = request.FILES.get('video')
        prediction=''
        if video_file:
            # Save the video file
            video_path = save_video_file(video_file)
            
            # Temporary folders for intermediate outputs
            temp_frame_folder = "temp_frames"
            temp_binary_frame_folder = "temp_binary_frames"

            # Run YOLOv8 on the video to extract frames
            run_yolov8(video_path, temp_frame_folder)

            # Run YOLOv8-segment on the extracted frames to get binary frames
            run_yolov8_segment(temp_frame_folder, temp_binary_frame_folder)

            # Create gait energy image from the binary frames
            gait_energy_image_output = "gait_energy_image.png"
            create_gait_energy_image(temp_binary_frame_folder, gait_energy_image_output)

            # Now you have the gait energy image ready for further processing or model input

            # Optionally, you can delete temporary folders and video file after processing
            # (make sure to handle exceptions if deletion fails)

            # Construct a response message with the gait energy image URL
            message = f'Video processed successfully. Gait Energy Image URL: {gait_energy_image_output}'
            model.load('densenet1-090.h5')
            prediction = model.predict()
            status_code = status.HTTP_200_OK
        else:
            message = 'No video file included in the request.'
            status_code = status.HTTP_400_BAD_REQUEST

        # Return the response
        return Response(
            {
                'result': prediction,
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
    # Return the path to access the saved file
    return file_path