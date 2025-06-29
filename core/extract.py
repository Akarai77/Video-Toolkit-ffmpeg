import os
import ffmpeg
from .menu import menu
from .IOFunctions import getInput, manageOutput
from .colorPrint import *

def extract(ch, input_dir, input_file, output_dir, output_file):
    input_path = [os.path.join(input_dir[i], input_file[i]) for i in range(len(input_file))]
    output_path = os.path.join(output_dir, output_file)
    print(output_path)
    try:
        if ch == 1:  # Extract Audio from Video
            ffmpeg.input(input_path[0]).output(
                output_path,
                vn=None,          # no video
                acodec='copy',
                preset='fast'
            ).run()
        elif ch == 2:  # Extract Video without Audio
            ffmpeg.input(input_path[0]).output(
                output_path,
                an=None,          # no audio
                vcodec='copy',
                preset='fast'
            ).run()
        elif ch == 3:  # Extract Subtitles
            ffmpeg.input(input_path[0]).output(
                output_path,
                scodec='copy',
                vn=None,
                an=None,
                preset='fast'
            ).run()
        else:
            error("Invalid extraction choice!")
            return
        success(f"\t\t{input_file[0]} has been successfully extracted to {output_file}")
    except ffmpeg.Error as e:
        error(f"FFmpeg Error: {str(e)}")
        if e.stderr:
            error(f"ERROR DETAILS: {e.stderr.decode('utf-8')}")
    except Exception as e:
        error(f"Unexpected Error: {str(e)}")

def handleExtract(dir):
    options = {
        'Extract Audio from Video': 'Video',
        'Extract Video without Audio': 'Video',
        'Extract Subtitles from Video': 'Video'
    }

    sub_options = [
        # For 'Extract Audio'
        {
            'Extract to MP3': '.mp3',
            'Extract to AAC': '.aac',
            'Extract to WAV': '.wav',
            'Extract to FLAC': '.flac',
            'Extract to OGG': '.ogg',
            'Extract to WMA': '.wma'
        },
        # For 'Extract Video without Audio'
        {
            'Extract to MP4': '.mp4',
            'Extract to MKV': '.mkv',
            'Extract to AVI': '.avi',
            'Extract to MOV': '.mov',
            'Extract to FLV': '.flv',
            'Extract to WEBM': '.webm'
        },
        # For 'Extract Subtitles'
        {
            'Extract to SRT': '.srt'
        }
    ]

    while True:
        options_list = list(options.keys())
        type_list = list(options.values())
        ch = menu("Extraction Options", options_list)
        if ch == len(options_list) + 1:
            return
        elif ch == -1:
            continue

        input_file_dir, input_file_name, input_file_format = getInput(type_list[ch-1], dir)
        if not input_file_dir or not input_file_name or not input_file_format:
            continue

        sub_options_list = list(sub_options[ch-1].keys())
        file_format_list = list(sub_options[ch-1].values())
        while True:
            ch2 = menu(options_list[ch-1], sub_options_list)
            if ch2 == len(sub_options_list) + 1:
                break
            elif ch2 == -1:
                continue
            output_file_dir, output_file_name = manageOutput(dir)
            if output_file_dir == -1 and output_file_name == -1:
                continue
            output_file_format = file_format_list[ch2-1]

            input_file = [input_file_name[i] + input_file_format[i] for i in range(len(input_file_name))]
            output_file = output_file_name + output_file_format

            extract(ch, input_file_dir, input_file, output_file_dir, output_file)
            return

