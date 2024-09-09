import os
import ffmpeg
from ytConvert import ytConvert
from menu import menu
from IOFunctions import getInput,manageOutput
from colorPrint import *

def clear(frquency):
    for _ in range(frquency):
        print("\033[F\033[2K", end="")

def getTime():
    try:
        hours = int(input('HOUR(S) (-1 to exit): '))
        if hours == -1:
            return -1
        elif hours < 0:
            error("INVALID TIME!\n")
            return None
        while True:
            mins = int(input('MINUTE(S) (-1 to go back): '))
            if mins == -1:
                clear(2)
                break
            elif mins < 0:
                error("INVALID TIME!\n")
                continue
            while True:
                secs = int(input('SECOND(S) (-1 to go back): '))
                if secs == -1:
                    clear(2)
                    break
                elif secs < 0:
                    error("INVALID TIME!\n")
                    continue
                return hours*3600 + mins*60 + secs
    except ValueError:
        error("Only Use Numbers")
        return 'error'

def clipify(input_video):
    while True:
        ch = menu("CLIP OPTIONS",['Consecutive Clipping','Custom Clipping'])
        if ch == 3:
            return -1
        elif ch == -1:
            continue
        probe = ffmpeg.probe(input_video)
        video_duration = float(probe['format']['duration'])
        if ch == 1:
            clip_duration = 0
            while True:
                print("\nEnter the starting time of clipping (H:M:S), Enter (0:0:0) to mark the start of the video: : ")
                start = getTime()
                if start == -1:
                    break
                elif start == None:
                    clear(2)
                    continue
                elif start == 'error':
                    continue
                else:
                    video_duration = video_duration - start
                while True:
                    print("\nEnter the ending time of clipping (H:M:S), Enter (0:0:0) to mark the end of the video: ")
                    end = getTime()
                    if end == -1:
                        clear(8)
                        break
                    elif end == None:
                        clear(2)
                        continue
                    elif ch == 'error':
                        continue
                    elif end!= 0:
                        video_duration = end - start
                    while True:
                        print("\nEnter the duration of the clips (H:M:S): ")
                        clip_duration = getTime()
                        if clip_duration == -1:
                            clear(8)
                            break
                        elif clip_duration == None:
                            clear(2)
                            continue
                        elif clip_duration == 'error':
                            continue
                        if clip_duration != 0 and clip_duration > video_duration:
                            error("NO CLIPS CAN BE FORMED! CLIP DURATION IS LONGER THAN THE ACTUAL VIDEO DURATION!")
                            continue
                        elif clip_duration == 0:
                            error("CLIP DURATION CANT BE 0!")
                            clear(8)
                            continue
                        numberofclips = int(video_duration // clip_duration)
                        while True:
                            proceed = input(f"\n{numberofclips} clips can be formed from {os.path.basename(input_video)}. Proceed [y/n]: ").lower()
                            if proceed == 'n':
                                clear(7)
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
                                    ffmpeg.input(input_video, ss=clipnum*clip_duration+start, t=clip_duration).output(f"{current_output}{format}",preset='ultrafast',acodec="copy").run()
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
        else:
            starting_time = []
            ending_time = []
            while True:
                print("\nEnter the starting time of clip (H:M:S), Enter (0:0:0) to mark the start of the video: : ")
                start = getTime()
                if start == -1:
                    clear(2)
                    break
                elif start == None:
                    clear(2)
                    continue
                elif start == 'error':
                    continue
                while True:
                    print("\nEnter the ending time of clip (H:M:S) : ")
                    end = getTime()
                    if end == -1:
                        clear(8)
                        break
                    elif end == None:
                        clear(2)
                        continue
                    elif end == 'start':
                        continue
                    if end < start:
                        error("ENDING TIME CANT BE BEFORE STARTING TIME!")
                        continue
                    starting_time.append(start)
                    ending_time.append(end)
                    try:
                        while True:
                            ch2 = input("\nDo you want to continue clipping? Proceed [y/n/0 to return] : ").lower()
                            if ch2 == 'n':
                                raise Exception                            
                            elif ch2 != 'y':
                                error("INVALID INPUT!")
                            else:
                                break
                    except Exception:
                        break
                    print(f'''\n{len(starting_time)} clips will be generated with consecutive numbers as suffixes of a common output file name.
                    For example, if 'sample' is the output file name, then the clips will be named 'sample1.mp4', 'sample2.mp4', and so on.\n''')
                    output_dir,output_video = manageOutput()
                    if output_dir == -1 and output_video == -1:
                        continue
                    try:
                        for i,start_time,end_time in zip(range(len(starting_time)),starting_time,ending_time):
                            current_output = os.path.join(output_dir,output_video + str(i+1))
                            format = os.path.splitext(input_video)[1]
                            ffmpeg.input(input_video, ss=start_time, to=end_time).output(f"{current_output}{format}",preset='ultrafast',acodec="copy").run()
                    except ffmpeg.Error as e:
                        error(f"\nFFmpeg Error: {str(e)}\n")
                        if e.stderr:
                            error(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
                        return -1
                    except Exception as e:
                        error(f"\nUnexpected Error: {str(e)}\n")
                        return -1
                    success(f"{os.path.basename(input_video)} has been successfully converted into {len(starting_time)} clips")
                    return 1

def handleClips():
    options = ['Clip YT URL','Clip Media File']
    while True:
        ch = menu('Choose an option',options)
        if ch == len(options)+1:
            return
        elif ch == -1:
            continue
        if ch == 1:
            _,input_video = ytConvert()
            if _  != -1 and input_video != -1:
                print(input_video)
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