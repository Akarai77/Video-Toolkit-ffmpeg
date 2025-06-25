import os
import ffmpeg
from .IOFunctions import getInput
from .menu import menu
from .colorPrint import *

def getCodecs(dir, options=['Get Codecs of a Video File', 'Get Codecs of an Audio File']):
    while True:
        ch = menu('Select an option', options)
        if ch == len(options) + 1:
            return -1, -1
        elif ch == -1:
            continue
        
        media_type = 'Video' if ch == 1 else 'Audio'
        input_dir, input_file_name, input_file_format = getInput(media_type, dir)

        if not input_dir or not input_file_name or not input_file_format:
            continue
        
        file_path = os.path.join(input_dir[0], input_file_name[0] + input_file_format[0])
        try:
            codecs = []
            probe = ffmpeg.probe(file_path)
            if ch == 1:
                video_codec = next(
                    (stream['codec_name'] for stream in probe['streams'] if stream['codec_type'] == 'video'),
                    None
                )
                codecs.append(video_codec)
            audio_codec = next(
                (stream['codec_name'] for stream in probe['streams'] if stream['codec_type'] == 'audio'),
                None
            )
            codecs.append(audio_codec)
            return file_path, codecs

        except ffmpeg.Error as e:
            error(f"FFmpeg Error: {str(e)}")
            error(f"ERROR DETAILS: {e.stderr.decode('utf-8') if e.stderr else 'No additional details available.'}")
            return -1, -1

        except Exception as e:
            error(f"Unexpected Error: {str(e)}")
            return -1, -1

