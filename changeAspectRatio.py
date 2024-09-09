import os
import ffmpeg
from menu import menu
from colorPrint import error
from IOFunctions import getInput, getExtensions, manageOutput

def getAspectRatio(inputFile):
    ratios = {
        '16:9 (Widescreen)': '16/9',
        '4:3 (Standard)': '4/3',
        '21:9 (Cinematic/Ultra-Widescreen)': '21/9',
        '1:1 (Square)': '1/1',
        '9:16 (Vertical)': '9/16',
        '2.39:1 (Anamorphic Widescreen)': '2.39/1',
        '2:1 (Univisium)': '2/1',
        '3:2': '3/2',
        '5:4': '5/4'
    }
    ratiosKeys = list(ratios.keys())
    ratiosValues = list(ratios.values())
    
    while True:
        ch = menu("CHOOSE AN ASPECT RATIO", ratiosKeys)
        if ch == -1:
            continue
        elif ch == len(ratiosKeys) + 1:
            return -1, -1
        else:
            try:
                ratio = ratiosValues[ch - 1]
                probe = ffmpeg.probe(inputFile)
                video_stream = next(
                    (stream for stream in probe['streams'] if stream['codec_type'] == 'video'),
                    None
                )
                if video_stream is None:
                    raise ValueError("No video stream found")
                
                width = int(video_stream['width'])
                height = int(video_stream['height'])
                
                antecedent, consequent = map(float, ratio.split('/'))
                aspect_width = width
                aspect_height = int(width / antecedent * consequent)
                
                if aspect_height > height:
                    aspect_height = height
                    aspect_width = int(height / consequent * antecedent)
                
                return aspect_width, aspect_height
            
            except ValueError as e:
                error(e)
                return -1, -1

def changeAspectRatio():
    while True:
        ch = menu("CHOOSE AN OPTION!", ['CHANGE ASPECT RATIO OF A SINGLE FILE', 'CHANGE ASPECT RATIO OF A DIRECTORY'])
        if ch == 3:
            return
        elif ch == -1:
            continue
        elif ch == 1:
            while True:
                input_dir, input_file, input_format = getInput('Video')
                if input_dir == [] and input_file == [] and input_format == []:
                    break
                
                file = os.path.join(input_dir[0], input_file[0] + input_format[0])
                
                while True:
                    output_dir, output_file = manageOutput()
                    if output_dir == -1 and output_file == -1:
                        break
                    
                    output = os.path.join(output_dir, output_file + os.path.splitext(file)[1])
                    
                    while True:
                        try:
                            width, height = getAspectRatio(file)
                            if width == -1 and height == -1:
                                break
                            video_stream = ffmpeg.input(file).video
                            audio_stream = ffmpeg.input(file).audio
                            filetered_video_stream = video_stream.filter('scale', width, height, force_original_aspect_ratio='increase').filter('crop',width,height)
                            ffmpeg.output(filetered_video_stream,audio_stream,output,preset='ultrafast').run()
                            print(f"Processed file saved as {output}")
                            return
                        
                        except ffmpeg.Error as e:
                            error(f"\nFFmpeg Error: {str(e)}\n")
                            if e.stderr:
                                error(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
                            return
                        
                        except Exception as e:
                            error(f"\nUnexpected Error: {str(e)}\n")
                            return
        
        elif ch == 2:
            while True:
                input_dir, input_file, input_format = getInput('Dir')
                if input_dir == [] and input_file == [] and input_format == []:
                    break
                
                dir = input_dir[0]
                files = [
                    os.path.join(dir, file) for file in os.listdir(dir)
                    if os.path.isfile(os.path.join(dir, file)) and os.path.splitext(file)[1] in getExtensions('Video')
                ]
                
                while True:
                    output_dir, output_file = manageOutput()
                    if output_dir == -1 and output_file == -1:
                        break
                    
                    for file in files:
                        output = os.path.join(output_dir, output_file + os.path.splitext(file)[1])
                        
                        while True:
                            try:
                                width, height = getAspectRatio(file)
                                if width == -1 and height == -1:
                                    break
                                video_stream = ffmpeg.input(file).video
                                audio_stream = ffmpeg.input(file).audio
                                filetered_video_stream = video_stream.filter('scale', width, height, force_original_aspect_ratio='increase').filter('crop',width,height)
                                ffmpeg.output(filetered_video_stream,audio_stream,output,preset='ultrafast').run()
                                print(f"Processed file saved as {output}")
                                return
                                print(f"Processed file saved as {output}")
                            
                            except ffmpeg.Error as e:
                                error(f"\nFFmpeg Error: {str(e)}\n")
                                if e.stderr:
                                    error(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
                                return
                            
                            except Exception as e:
                                error(f"\nUnexpected Error: {str(e)}\n")
                                return
