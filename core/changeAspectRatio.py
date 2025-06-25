import os
import ffmpeg
from .menu import menu
from .colorPrint import error
from .IOFunctions import getInput, getExtensions, manageOutput

def getAspectRatio(inputFile):
    """
    Prompt user to select an aspect ratio, then calculate
    and return (width, height) for the new aspect ratio based
    on the input file's dimensions.
    Returns (-1, -1) on error or cancel.
    """
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

def process_file(file, output_path, width, height):
    """
    Process a single video file, changing its aspect ratio by scaling and cropping.
    Saves output to output_path.
    """
    try:
        video_stream = ffmpeg.input(file).video
        audio_stream = ffmpeg.input(file).audio
        filtered_video_stream = (
            video_stream
            .filter('scale', width, height, force_original_aspect_ratio='increase')
            .filter('crop', width, height)
        )
        ffmpeg.output(filtered_video_stream, audio_stream, output_path, preset='ultrafast').run()
        print(f"Processed file saved as {output_path}")
    except ffmpeg.Error as e:
        error(f"\nFFmpeg Error: {str(e)}\n")
        if e.stderr:
            error(f"\nERROR DETAILS: {e.stderr.decode('utf-8')}\n")
    except Exception as e:
        error(f"\nUnexpected Error: {str(e)}\n")

def changeAspectRatio(dir):
    """
    Main interactive function to let user change aspect ratio of either
    a single video file or all videos in a directory.
    """
    while True:
        ch = menu("CHOOSE AN OPTION!", ['CHANGE ASPECT RATIO OF A SINGLE FILE', 'CHANGE ASPECT RATIO OF A DIRECTORY'])
        if ch == 3:
            return
        elif ch == -1:
            continue

        if ch == 1:
            # Single file mode
            while True:
                input_dir, input_file, input_format = getInput('Video', dir)
                if not input_dir and not input_file and not input_format:
                    break

                file = os.path.join(input_dir[0], input_file[0] + input_format[0])

                while True:
                    output_dir, output_file = manageOutput(dir)
                    if output_dir == -1 and output_file == -1:
                        break

                    output = os.path.join(output_dir, output_file + os.path.splitext(file)[1])

                    width, height = getAspectRatio(file)
                    if width == -1 and height == -1:
                        break

                    process_file(file, output, width, height)
                    return  # Exit after processing one file

        elif ch == 2:
            # Directory mode
            while True:
                input_dir, _, _ = getInput('Dir', dir)
                if not input_dir:
                    break

                target_dir = input_dir[0]
                files = [
                    os.path.join(target_dir, file)
                    for file in os.listdir(target_dir)
                    if os.path.isfile(os.path.join(target_dir, file)) and os.path.splitext(file)[1].lower() in getExtensions('Video')
                ]

                if not files:
                    error(f"No video files found in {target_dir}")
                    break

                while True:
                    output_dir, output_file = manageOutput(dir)
                    if output_dir == -1 and output_file == -1:
                        break

                    width, height = getAspectRatio(files[0])
                    if width == -1 and height == -1:
                        break

                    for i, file in enumerate(files, start=1):
                        output = os.path.join(output_dir, f"{output_file}{i}{os.path.splitext(file)[1]}")
                        process_file(file, output, width, height)

                    return  # Exit after processing directory

