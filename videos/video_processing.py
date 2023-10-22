# Import necessary libraries
import subprocess

# function to run YOLOv8 on the video
def run_yolov8(video_path, frame_output_folder):
    # Replace 'yolov8_code.py' with the actual filename of your YOLOv8 code
    subprocess.run(['python', 'videos/utils/yolotrackcrop90test.py', video_path, frame_output_folder])

# YOLOv8-segmentfunction on the extracted frames
def run_yolov8_segment(frame_folder, binary_frame_output_folder):
    # Replace 'yolov8_segment_code.py' with the actual filename of your YOLOv8-segment code
    subprocess.run(['python', 'videos/utils/pd_90_silhouettes.py', frame_folder, binary_frame_output_folder])

# function to create gait energy image from binary frames
def create_gait_energy_image(binary_frame_folder, gait_energy_image_output):
    # Replace 'gait_energy_code.py' with the actual filename of your gait energy image code
    subprocess.run(['python', 'videos/utils/gei.py', binary_frame_folder, gait_energy_image_output])

# Main pipeline function
def video_to_gait_energy(video_path, gait_energy_image_output):
    # Temporary folders for intermediate outputs
    temp_frame_folder = "temp_frames"
    temp_binary_frame_folder = "temp_binary_frames"

    # Run YOLOv8 on the video to extract frames
    run_yolov8(video_path, temp_frame_folder)

    # Run YOLOv8-segment on the extracted frames to get binary frames
    run_yolov8_segment(temp_frame_folder, temp_binary_frame_folder)

    # Create gait energy image from the binary frames
    create_gait_energy_image(temp_binary_frame_folder, gait_energy_image_output)