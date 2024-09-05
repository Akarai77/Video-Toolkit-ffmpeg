import os
import ffmpeg
from ytconvert import ytconvert
from menu import menu
from IO_functions import getInput,manageOutput
from colorPrint import *

def clipify(input_video):
    probe = ffmpeg.probe(input_video)
    video_duration = float(probe['format']['duration'])
    while True:
        print('Enter the duration of the clips: ')
        while True:
            try:
                hours = int(input('Hours (-1 to exit): '))
                if hours == -1:
                    return -1
                while True:
                    mins = int(input('Minutes (-1 to go back): '))
                    if mins == -1:
                        print("\033[F\033[2K", end="")
                        print("\033[F\033[2K", end="")
                        break
                    while True:
                        secs = int(input('Seconds (-1 to go back): '))
                        if secs == -1:
                            print("\033[F\033[2K", end="")
                            print("\033[F\033[2K", end="")
                            break
                        raise Exception
            except ValueError:
                error("Only Use Numbers")
            except Exception:
                break
        clip_duration = hours*3600 + mins*60 + secs
        if hours < 0 or mins < 0 or secs < 0:
            error("INVALID TIME!\n")
            continue
        elif clip_duration > video_duration:
            error("Clip Duration is longer than the actual Video Duration")
            continue
            
        numberofclips = int(video_duration // 60)
        while True:
            proceed = input(f"\n{numberofclips} clips can be formed from {os.path.basename(input_video)}. Proceed [y/n]: ").lower()
            if proceed == 'n':
                break
            elif proceed != 'y':
                error('INVALID!\n')
                continue
            
            print(f'''\n{numberofclips} clips will be generated with consecutive numbers as suffixes of a common output file name.
            For example, if 'sample' is the output file name, then the clips will be named 'sample1.mp4', 'sample2.mp4', and so on.\n''')
            output_dir,output_video = manageOutput()
            if output_dir == -1 and output_video == -1:
                continue
            try:
                for clipnum in range(numberofclips):
                    current_output = os.path.join(output_dir,output_video + str(clipnum+1))
                    format = os.path.splitext(input_video)[1]
                    ffmpeg.input(input_video, ss=clipnum*clip_duration, t=clip_duration).output(f"{current_output}{format}",vcodec='h264_nvenc',preset='fast', video_bitrate='1M',acodec="copy").run()
            except ffmpeg.Error as e:
                error(f"\nFFmpeg Error: {str(e)}\n")
                if e.stderr:
                    error(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
                return -1
            except Exception as e:
                error(f"\nUnexpected Error: {str(e)}\n")
                return -1
            success(f"{os.path.basename(input_video)} has been successfully converted into {numberofclips} clips")
            return 1
                
            
            


def handle_clips():
    options = ['Clip YT URL','Clip Media File']
    while True:
        ch = menu('Choose an option',options)
        if ch == len(options)+1:
            return
        elif ch == -1:
            continue
        if ch == 1:
            _,input_video = ytconvert()
            if _  != -1 and input_video != -1:
                if clipify(input_video) == -1:
                    continue
                else:
                    break
            continue
        elif ch == 2:
            input_dir,input_name,input_format = getInput('Video')
            if input_dir != [] and input_name != [] and input_format != []:
                input_video = os.path.join(input_dir[0],input_name[0]+input_format[0])
                if clipify(input_video) == -1:
                    continue
                else:
                    break