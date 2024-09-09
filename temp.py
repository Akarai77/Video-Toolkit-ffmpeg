import subprocess
import os

def scale_and_crop_video(input_file, output_file, width, height):
    try:
        # Check if ffmpeg is installed
        subprocess.run(['ffmpeg', '-version'], check=True)
        
        # Create the ffmpeg scaling and cropping command
        command = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f'scale={width}:{height}:force_original_aspect_ratio=increase,crop={width}:{height}',
            '-c:a', 'copy',  # Keep the original audio
            output_file
        ]
        
        # Execute the command
        subprocess.run(command, check=True)
        print(f"Video scaled and cropped successfully. Output saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ffmpeg: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_path = os.path.abspath('./GTAV(1)_CLIP1.mp4')
output_path = os.path.abspath('./output.mp4')
scale_and_crop_video(input_path, output_path, 1080, 1920)
