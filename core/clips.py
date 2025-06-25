import os
import ffmpeg
from .ytConvert import ytConvert
from .menu import menu
from .IOFunctions import getInput, manageOutput
from .colorPrint import *

def clear(frequency):
    """Clears the last `frequency` lines from the terminal."""
    for _ in range(frequency):
        print("\033[F\033[2K", end="")

def getTime():
    """Get time input from user in hours, minutes, seconds. Returns total seconds or control flags."""
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
                return None
            elif mins < 0:
                error("INVALID TIME!\n")
                continue
            
            while True:
                secs = int(input('SECOND(S) (-1 to go back): '))
                if secs == -1:
                    clear(2)
                    return None
                elif secs < 0:
                    error("INVALID TIME!\n")
                    continue
                return hours * 3600 + mins * 60 + secs
    except ValueError:
        error("Only use numbers!")
        return None

def clipify(input_video, dir):
    """Interactively clip the input video into segments."""
    while True:
        ch = menu("CLIP OPTIONS", ['Consecutive Clipping', 'Custom Clipping'])
        if ch == 3:
            return -1
        elif ch == -1:
            continue
        
        probe = ffmpeg.probe(input_video)
        video_duration = float(probe['format']['duration'])

        if ch == 1:  # Consecutive Clipping
            while True:
                print("\nEnter the starting time of clipping (H:M:S), Enter (0:0:0) for start of video:")
                start = getTime()
                if start == -1:
                    break
                elif start is None:
                    clear(2)
                    continue
                
                remaining_duration = video_duration - start
                if remaining_duration <= 0:
                    error("Start time is beyond video duration!")
                    continue

                while True:
                    print("\nEnter the ending time of clipping (H:M:S), Enter (0:0:0) for end of video:")
                    end = getTime()
                    if end == -1:
                        clear(8)
                        break
                    elif end is None:
                        clear(2)
                        continue
                    if end != 0:
                        clip_duration = end - start
                    else:
                        clip_duration = remaining_duration
                    
                    if clip_duration <= 0:
                        error("Invalid clip duration!")
                        clear(8)
                        continue
                    
                    while True:
                        print("\nEnter the duration of the clips (H:M:S): ")
                        clip_len = getTime()
                        if clip_len == -1:
                            clear(8)
                            break
                        elif clip_len is None:
                            clear(2)
                            continue
                        
                        if clip_len <= 0:
                            error("CLIP DURATION CANNOT BE 0 OR NEGATIVE!")
                            clear(8)
                            continue
                        
                        if clip_len > clip_duration:
                            error("CLIP DURATION IS LONGER THAN THE SELECTED CLIP DURATION!")
                            continue
                        
                        number_of_clips = int(clip_duration // clip_len)
                        while True:
                            proceed = input(f"\n{number_of_clips} clips can be formed from {os.path.basename(input_video)}. Proceed [y/n]: ").lower()
                            if proceed == 'n':
                                clear(7)
                                break
                            elif proceed != 'y':
                                error('INVALID INPUT!\n')
                                continue
                            
                            output_dir, output_video = manageOutput(dir)
                            if output_dir == -1 and output_video == -1:
                                continue
                            
                            try:
                                for clipnum in range(number_of_clips):
                                    current_output = os.path.join(output_dir, output_video + str(clipnum + 1))
                                    ext = os.path.splitext(input_video)[1]
                                    ffmpeg.input(input_video, ss=clipnum * clip_len + start, t=clip_len).output(
                                        f"{current_output}{ext}", preset='ultrafast', acodec="copy").run()
                            except ffmpeg.Error as e:
                                error(f"\nFFmpeg Error: {str(e)}\n")
                                if e.stderr:
                                    error(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
                                return -1
                            except Exception as e:
                                error(f"\nUnexpected Error: {str(e)}\n")
                                return -1
                            success(f"{os.path.basename(input_video)} successfully clipped into {number_of_clips} clips.")
                            return 1
                    break
                break
        
        else:  # Custom Clipping
            starting_times = []
            ending_times = []
            while True:
                print("\nEnter the starting time of clip (H:M:S), Enter (0:0:0) for start of video:")
                start = getTime()
                if start == -1:
                    clear(2)
                    break
                elif start is None:
                    clear(2)
                    continue
                
                print("\nEnter the ending time of clip (H:M:S):")
                end = getTime()
                if end == -1:
                    clear(8)
                    continue
                elif end is None:
                    clear(2)
                    continue
                
                if end < start:
                    error("ENDING TIME CANNOT BE BEFORE STARTING TIME!")
                    continue
                
                starting_times.append(start)
                ending_times.append(end)
                
                cont = input("\nDo you want to continue clipping? Proceed [y/n/0 to return]: ").lower()
                if cont == 'n' or cont == '0':
                    break
                elif cont != 'y':
                    error("INVALID INPUT!")
                    continue
            
            if not starting_times:
                return  # Nothing to clip
            
            print(f"\n{len(starting_times)} clips will be generated with consecutive numbers as suffixes of a common output file name.")
            print("Example: If 'sample' is the output file name, clips will be named 'sample1.mp4', 'sample2.mp4', etc.\n")

            while True:
                output_dir, output_video = manageOutput(dir)
                if output_dir == -1 and output_video == -1:
                    continue
                try:
                    for i, (start_time, end_time) in enumerate(zip(starting_times, ending_times)):
                        current_output = os.path.join(output_dir, output_video + str(i + 1))
                        ext = os.path.splitext(input_video)[1]
                        ffmpeg.input(input_video, ss=start_time, to=end_time).output(
                            f"{current_output}{ext}", preset='ultrafast', acodec="copy").run()
                except ffmpeg.Error as e:
                    error(f"\nFFmpeg Error: {str(e)}\n")
                    if e.stderr:
                        error(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
                    return -1
                except Exception as e:
                    error(f"\nUnexpected Error: {str(e)}\n")
                    return -1
                success(f"{os.path.basename(input_video)} successfully clipped into {len(starting_times)} clips.")
                return 1

def handleClips(dir):
    """Main interface for clipping videos from YouTube URLs or media files."""
    options = ['Clip YT URL', 'Clip Media File']
    while True:
        ch = menu('Choose an option', options)
        if ch == len(options) + 1:
            return
        elif ch == -1:
            continue
        if ch == 1:
            _, input_video = ytConvert(dir)
            if _ != -1 and input_video != -1:
                print(input_video)
                if clipify(input_video, dir) == -1:
                    continue
                else:
                    break
            continue
        elif ch == 2:
            input_dir, input_name, input_format = getInput('Video', dir)
            if input_dir and input_name and input_format:
                input_video = os.path.join(input_dir[0], input_name[0] + input_format[0])
                if clipify(input_video, dir) == -1:
                    continue
                else:
                    break

