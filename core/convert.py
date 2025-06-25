import os
import ffmpeg
from .menu import menu
from .IOFunctions import getInput, manageOutput
from .colorPrint import *

def convert(input_dirs, input_files, output_dir, output_file):
    input_paths = [os.path.join(input_dirs[i], input_files[i]) for i in range(len(input_files))]
    output_path = os.path.join(output_dir, output_file)
    try:
        if len(input_paths) > 1:
            input_streams = [ffmpeg.input(f) for f in input_paths]
            concat_stream = ffmpeg.concat(*input_streams, v=1, a=1).node
            video = concat_stream[0]
            audio = concat_stream[1]
            stream = ffmpeg.output(video, audio, output_path, preset='ultrafast')
        else:
            stream = ffmpeg.input(input_paths[0]).output(output_path, preset='ultrafast')

        stream.run()
        success(f"\t\t{input_files[0]} has been successfully converted to {output_file}")
    except ffmpeg.Error as e:
        error(f"FFmpeg Error: {str(e)}")
        if e.stderr:
            error(f"ERROR DETAILS: {e.stderr.decode('utf-8')}")
    except Exception as e:
        error(f"Unexpected Error: {str(e)}")

def handleConvert(dir):
    options = {
        'Convert Video':'Video',
        'Convert Audio':'Audio',
        'Convert Audio to Video with single image': 'Audio+Image',
        'Convert Audio to Video with sequence of images': 'Audio+ImageSeq',
        'Convert Video to GIF':'Video'
    }
    
    sub_options = [
        # Convert Video
        {'Convert to MP4': '.mp4', 'Convert to MKV': '.mkv', 'Convert to AVI': '.avi', 'Convert to MOV': '.mov', 'Convert to FLV': '.flv'},
        # Convert Audio
        {'Convert to MP3': '.mp3', 'Convert to AAC': '.aac', 'Convert to WAV': '.wav', 'Convert to FLAC': '.flac', 'Convert to WMA': '.wma'},
        # Convert Audio to Video with single image
        {'Convert to MP4': '.mp4', 'Convert to MKV': '.mkv', 'Convert to AVI': '.avi', 'Convert to MOV': '.mov', 'Convert to FLV': '.flv'},
        # Convert Audio to Video with sequence of images
        {'Convert to MP4': '.mp4', 'Convert to MKV': '.mkv', 'Convert to AVI': '.avi', 'Convert to MOV': '.mov', 'Convert to GIF': '.gif'},
        # Convert Video to GIF
        {'Convert to GIF': '.gif'}
    ]

    while True:
        options_list = list(options.keys())
        types_list = list(options.values())
        ch = menu("Convert Options", options_list)
        if ch == len(options_list) + 1:
            return
        elif ch == -1:
            continue
        
        selected_type = types_list[ch - 1]

        # Special handling for sequence of images option:
        if selected_type == 'Audio+ImageSeq':
            try:
                n = int(input("Enter the number of images in the sequence: "))
                if n <= 0:
                    error("Number of images must be positive.")
                    continue
            except ValueError:
                error("Invalid number entered.")
                continue

            # Get image files from user
            input_file_dir, input_file_name, input_file_format = [], [], []
            for i in range(n):
                print(f"Select image {i+1} in the sequence:")
                dirs, names, formats = getInput('Image', dir)
                if not dirs or not names or not formats:
                    break
                input_file_dir.append(dirs[0])
                input_file_name.append(names[0])
                input_file_format.append(formats[0])
            
            # Get audio file
            audio_dir, audio_name, audio_format = getInput('Audio', dir)
            if not audio_dir or not audio_name or not audio_format:
                continue
            
            # Append audio to inputs
            input_file_dir.append(audio_dir[0])
            input_file_name.append(audio_name[0])
            input_file_format.append(audio_format[0])

        else:
            input_file_dir, input_file_name, input_file_format = getInput(selected_type, dir)
            if not input_file_dir or not input_file_name or not input_file_format:
                continue
        
        sub_opts = list(sub_options[ch - 1].keys())
        file_formats = list(sub_options[ch - 1].values())
        
        while True:
            ch2 = menu(options_list[ch - 1], sub_opts)
            if ch2 == len(sub_opts) + 1:
                break
            elif ch2 == -1:
                continue
            output_dir, output_name = manageOutput(dir)
            if output_dir == -1 and output_name == -1:
                continue
            output_format = file_formats[ch2 - 1]

            input_files = [input_file_name[i] + input_file_format[i] for i in range(len(input_file_name))]
            output_file = output_name + output_format
            convert(input_file_dir, input_files, output_dir, output_file)
            return

