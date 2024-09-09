import os
import ffmpeg
from menu import menu
from IOFunctions import getInput
from IOFunctions import manageOutput
from colorPrint import *

def convert(input_dir,input_file,output_dir,output_file):
    input_path = [os.path.join(input_dir[i],input_file[i]) for i in range(len(input_file))]
    output_path = os.path.join(output_dir, output_file)
    print(output_path)
    try:
        if len(input_path) > 1:
            input_streams = [ffmpeg.input(f) for f in input_path]
            stream = ffmpeg.concat(*input_streams)
            stream = stream.output(output_path,preset='fast', video_bitrate='1M')
        else:
            stream = ffmpeg.input(input_path[0]).output(output_path,preset='fast', video_bitrate='1M')

        stream.run()
        success(f"\t\t{input_file[0]} has been successfully converted to {output_file}")
        return
    except ffmpeg.Error as e:
        error(f"FFmpeg Error: {str(e)}")
        if e.stderr:
            error(f"ERROR DETAILS: {e.stderr.decode('utf-8')}")
        return
    except Exception as e:
        error(f"Unexpected Error: {str(e)}\n")
        return

def handleConvert():
    options = {
        'Convert Video':'Video',
        'Convert Audio':'Audio',
        'COnvert Audio to Video with single image': 'Audio+Image',
        'Convert Audio to VIdeo with sequence of images': 'Audio',
        'Convert Video to GIF':'Video'
    }
    
    sub_options = [
        # For 'Convert Video'
        {
            'Convert to MP4': '.mp4',
            'Convert to MKV': '.mkv',
            'Convert to AVI': '.avi',
            'Convert to MOV': '.mov',
            'Convert to FLV': '.flv'
        },
        # For 'Convert Audio'
        {
            'Convert to MP3': '.mp3',
            'Convert to AAC': '.aac',
            'Convert to WAV': '.wav',
            'Convert to FLAC': '.flac',
            'Convert to WMA': '.wma'
        },
        # For 'Convert Audio to Video'
        {
            'Convert to MP3': '.mp3',
            'Convert to AAC': '.aac',
            'Convert to WAV': '.wav',
            'Convert to FLAC': '.flac',
            'Convert to OGG': '.ogg',
            'Convert to WMA': '.wma'
        },
        # For 'Convert Image Sequence to Video'
        {
            'Convert to MP4': '.mp4',
            'Convert to MKV': '.mkv',
            'Convert to AVI': '.avi',
            'Convert to MOV': '.mov',
            'Convert to GIF': '.gif'
        },
        # For 'Convert Video to GIF'
        {
            'Convert to GIF': '.gif'
        }
    ]

    while True:
        options_list = list(options.keys())
        type_list = list(options.values())
        ch = menu("Convert Options",options_list)
        if ch == len(options_list)+1:
            return
        elif ch == -1:
            continue
        
        if ch == 4:
            n = int(input("Enter the number of images in the sequence: "))
            for _ in range(n):
                type_list[3] += "+Image"
            
        input_file_dir,input_file_name,input_file_format = getInput(type_list[ch-1])
        
        if input_file_dir == [] and input_file_name == [] and input_file_format == []:
            continue
        
        
        sub_options_list = list(sub_options[ch-1].keys())
        file_format_list = list(sub_options[ch-1].values())
        while True:
            ch2 = menu(options_list[ch-1],sub_options_list)
            if ch2 == len(sub_options_list)+1:
                break
            elif ch2 == -1:
                continue 
            else:
                output_file_dir,output_file_name = manageOutput()
                if output_file_dir == -1 and output_file_name == -1:
                    continue
                output_file_format = file_format_list[ch2-1]
                input_file = []
                input_file = [(input_file_name[i] + input_file_format[i]) for i in range(len(input_file_name))]
                output_file = output_file_name + output_file_format
                convert(input_file_dir,input_file,output_file_dir,output_file)
                return