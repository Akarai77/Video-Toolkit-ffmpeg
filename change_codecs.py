import os
import ffmpeg
from get_codecs import get_codecs
from colorPrint import *
from menu import menu
from IO_functions import getExtensions
from IO_functions import manageOutput

directory = "."

def change_video_codec(file,cvc,choice,codec_values):
    selected_codec = codec_values[choice - 1]
    output_file_dir,output_file = manageOutput()
    if output_file_dir == -1 and output_file == -1:
        return -1
    output_file_path = os.path.join(output_file_dir,output_file+os.path.splitext(file)[1])
    try:
        ffmpeg.input(file).output(output_file_path, vcodec=selected_codec).run()
        print(f"\t\tVideo Codec of {file} has been successfully converted from {cvc} to {selected_codec}\n")
    except ffmpeg.Error as e:
        print(f"\nFFmpeg Error: {str(e)}\n")
        if e.stderr:
            print(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}\n")
        

def change_audio_codec(file,cac,choice,codec_values):
    selected_codec = codec_values[choice - 1]
    output_file_dir,output_file = manageOutput()
    if output_file_dir == -1 and output_file == -1:
        return -1
    output_file_path = os.path.join(output_file_dir,output_file+os.path.splitext(file)[1])
    try:
        ffmpeg.input(file).output(output_file_path, acodec=selected_codec).run()
        print(f"\t\tVideo Codec of {file} has been successfully converted from {cac} to {selected_codec}\n")
    except ffmpeg.Error as e:
        print(f"\nFFmpeg Error: {str(e)}\n")
        if e.stderr:
            print(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}\n")

def change_both(file,cds,choice1,video_codec_values,choice2,audio_codec_values):
    selected_video_codec = video_codec_values[choice1 - 1]
    selected_audio_codec = audio_codec_values[choice2-1]
    output_file_dir,output_file = manageOutput()
    if output_file_dir == -1 and output_file == -1:
        return -1
    output_file_path = os.path.join(output_file_dir,output_file+os.path.splitext(file)[1])
    try:
        ffmpeg.input(file).output(output_file_path, vcodec=selected_video_codec,acodec=selected_audio_codec).run()
        print(f"\t\tVideo Codec and Audio Codec of {file} has been successfully converted from {cds[0]} and {cds[1]} to {selected_video_codec} and {selected_audio_codec} respectively\n")
    except ffmpeg.Error as e:
        print(f"\nFFmpeg Error: {str(e)}\n")
        if e.stderr:
            print(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
    except Exception as e:
        print(f"\nUnexpected Error: {str(e)}\n")

def change_codecs():
    file, cds = get_codecs(['Change Codecs of a Video File', 'Change Codecs of an Audio File'])
    if file == -1 and cds == -1:
        return
    if os.path.splitext(file)[1] in getExtensions('Video'):
        type = 'Video'
    elif os.path.splitext(file)[1] in getExtensions('Audio'):
        type = 'Audio'
    else:
        error("An Error Occured!")
        return
    
    # Display current codecs
    success(f"Current Video Codec: {cds[0]}",end="")
    if len(cds) > 1:
        success(f"Current Audio Codec: {cds[1]}")
    
    # Determine options
    options = ['Change Video Codec', 'Change Audio Codec','Change Both'] if type == 'Video' else ['Change Audio Codec']
    
    while True:
        ch = menu("What do you want to change?", options)
        if ch == len(options) + 1:
            return
        elif ch == -1:
            continue
            # Define codec dictionaries
        video_codecs = {
            'H.263': 'h263',
            'H.264': 'libx264',
            'H.265': 'libx265',
            'HEVC': 'libx265',
            'MPEG-4': 'mpeg4',
            'VP9': 'libvpx-vp9',
            'MPEG-2': 'mpeg2video',
            'XVID': 'libxvid',
            'MJPEG': 'mjpeg'
        }
        audio_codecs = {
            'MP3': 'libmp3lame',
            'AAC': 'aac',
            'Opus': 'libopus',
            'Vorbis': 'libvorbis',
            'FLAC': 'flac',
            'ALAC': 'alac',
            'WAV': 'pcm_s16le',
            'AC3': 'ac3',
            'E-AC3': 'eac3',
            'MPEG-2 Audio': 'mp2'
        }
        
        video_codec_list = list(video_codecs.keys())
        video_codec_values = list(video_codecs.values())
        audio_codec_list = list(audio_codecs.keys())
        audio_codec_values = list(audio_codecs.values())
        if type == 'Video':
            if ch == 1:
                while True:
                    ch2 = menu('Select the Resultant Video Codec:', video_codec_list)
                    if ch2 == len(video_codec_list) + 1:
                        break
                    elif ch2 == -1:
                        continue
                    if change_video_codec(file,cds[0],ch2,video_codec_values) == -1:
                        continue
                    else:
                        return
            elif ch == 2:
                while True:
                    ch2 = menu('Select the Resultant Audio Codec:', audio_codec_list)
                    if ch2 == len(audio_codec_list) + 1:
                        break
                    elif ch2 == -1:
                        continue
                    if change_audio_codec(file,cds[1],ch2,audio_codec_values) == -1:
                        continue
                    else:
                        return
            else:
                while True:
                    ch2 = menu('Select the Resultant Video Codec:', video_codec_list)
                    if ch2 == len(video_codec_list) + 1:
                        break
                    elif ch2 == -1:
                        continue
                    while True:
                        ch3 = menu('Select the Resultant Audio Codec:', audio_codec_list)
                        if ch3 == len(audio_codec_list) + 1:
                            break
                        elif ch3 == -1:
                            continue
                        if change_both(file,cds,ch2,video_codec_values,ch3,audio_codec_values) == 1:
                            continue
                        else:
                            return
                        
        else:
            if ch == 1:
                while True:
                    ch2 = menu('Select the Resultant Audio Codec:', audio_codec_list)
                    if ch2 == len(audio_codec_list) + 1:
                        break
                    elif ch2 == -1:
                        continue
                    if change_audio_codec(file,cds[0],ch2,audio_codec_values) == -1:
                        continue
                    else:
                        return
                    
            
        #     while True:
        #         ch2 = menu('Select the Resultant Video Codec:', codec_list)
        #         if ch2 == len(codec_list) + 1:
        #             break
        #         elif ch2 == -1:
        #             continue
        #         else:
        #             selected_codec = codec_values[ch2 - 1]
        #             output_file_dir,output_file = manageOutput()
        #             output_file_path = os.path.join(output_file_dir,output_file+os.path.splitext(vid)[1])
        #             try:
        #                 ffmpeg.input(vid).output(output_file_path, vcodec=selected_codec).run()
        #                 print(f"\t\tVideo Codec of {vid} has been successfully converted to {selected_codec}\n")
        #             except ffmpeg.Error as e:
        #                 print(f"\nFFmpeg Error: {str(e)}\n")
        #                 if e.stderr:
        #                     print(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
        #             except Exception as e:
        #                 print(f"\nUnexpected Error: {str(e)}\n")
        #             break

        # elif (ch == 2 and len(cds) == 2) or (ch == 1 and len(cds) == 1):  # Audio Codec change
        #     codec_list = list(audio_codecs.keys())
        #     codec_values = list(audio_codecs.values())
        #     while True:
        #         ch2 = menu('Select the Resultant Audio Codec:', codec_list)
        #         if ch2 == len(codec_list) + 1:
        #             break
        #         elif ch2 == -1:
        #             continue
        #         else:
        #             selected_codec = codec_values[ch2 - 1]
        #             output_file_dir,output_file = manageOutput()
        #             output_file_path = os.path.join(output_file_dir,output_file+os.path.splitext(vid)[1])
        #             try:
        #                 ffmpeg.input(vid).output(output_file_path, acodec=selected_codec).run()
        #                 print(f"\t\tAudio Codec of {vid} has been successfully converted to {selected_codec}\n")
        #             except ffmpeg.Error as e:
        #                 print(f"\nFFmpeg Error: {str(e)}\n")
        #                 if e.stderr:
        #                     print(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
        #             except Exception as e:
        #                 print(f"\nUnexpected Error: {str(e)}\n")
        #             break
                    
change_codecs()