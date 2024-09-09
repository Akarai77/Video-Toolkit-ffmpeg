import subprocess
import os

def stretch_video(input_file, output_file, width, height):
    try:
        command = [
            'ffmpeg',
            '-i', input_file,
            '-vf', f'scale={width}:{height}',  # Stretch to fit the resolution
            '-c:a', 'copy',
            output_file
        ]
        
        subprocess.run(command, check=True)
        print(f"Video stretched to fit screen. Output saved as {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing ffmpeg: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
input_path = os.path.abspath('./GTAV(1)_CLIP1.mp4')
output_path = os.path.abspath('./output2.mp4')
stretch_video(input_path, output_path, 1080, 1920)