import os
import ffmpeg
from .getCodecs import getCodecs
from .colorPrint import *
from .menu import menu
from .IOFunctions import getExtensions, manageOutput

def changeVideoCodec(input_file, dir, current_video_codec, choice, codec_values):
    """
    Change the video codec of the input file to the selected codec.
    """
    selected_codec = codec_values[choice - 1]
    output_file_dir, output_file_name = manageOutput(dir)
    if output_file_dir == -1 and output_file_name == -1:
        return -1
    output_file = os.path.join(output_file_dir, output_file_name + os.path.splitext(input_file)[1])

    try:
        input_ffmpeg = ffmpeg.input(input_file)
        input_video = input_ffmpeg['v']
        input_audio = input_ffmpeg['a']
        try:
            input_subtitle = input_ffmpeg['s']
        except KeyError:
            input_subtitle = None

        if input_subtitle:
            output_ffmpeg = ffmpeg.output(
                input_video, input_audio, input_subtitle, output_file,
                vcodec=selected_codec, acodec='copy', scodec='copy', preset='ultrafast'
            )
        else:
            output_ffmpeg = ffmpeg.output(
                input_video, input_audio, output_file,
                vcodec=selected_codec, acodec='copy', preset='ultrafast'
            )
        ffmpeg.run(output_ffmpeg)
        success(f"Video Codec of {input_file} has been successfully converted from {current_video_codec} to {selected_codec}")
    except ffmpeg.Error as e:
        error(f"FFmpeg Error: {str(e)}")
        if e.stderr:
            error(f"ERROR DETAILS: {e.stderr.decode('utf-8')}")
    except Exception as e:
        error(f"Unexpected Error: {str(e)}")

def changeAudioCodec(input_file, dir, current_audio_codec, choice, codec_values):
    """
    Change the audio codec of the input file to the selected codec.
    """
    selected_codec = codec_values[choice - 1]
    output_file_dir, output_file_name = manageOutput(dir)
    if output_file_dir == -1 and output_file_name == -1:
        return -1
    output_file = os.path.join(output_file_dir, output_file_name + os.path.splitext(input_file)[1])

    try:
        input_ffmpeg = ffmpeg.input(input_file)
        input_video = input_ffmpeg['v']
        input_audio = input_ffmpeg['a']
        try:
            input_subtitle = input_ffmpeg['s']
        except KeyError:
            input_subtitle = None

        if input_subtitle:
            output_ffmpeg = ffmpeg.output(
                input_video, input_audio, input_subtitle, output_file,
                acodec=selected_codec, vcodec='copy', scodec='copy', preset='ultrafast'
            )
        else:
            output_ffmpeg = ffmpeg.output(
                input_video, input_audio, output_file,
                acodec=selected_codec, vcodec='copy', preset='ultrafast'
            )
        ffmpeg.run(output_ffmpeg)
        success(f"Audio Codec of {input_file} has been successfully converted from {current_audio_codec} to {selected_codec}")
    except ffmpeg.Error as e:
        error(f"FFmpeg Error: {str(e)}")
        if e.stderr:
            error(f"ERROR DETAILS: {e.stderr.decode('utf-8')}")
    except Exception as e:
        error(f"Unexpected Error: {str(e)}")

def changeBoth(input_file, dir, codecs, video_choice, video_codec_values, audio_choice, audio_codec_values):
    """
    Change both video and audio codecs of the input file to selected codecs.
    """
    selected_video_codec = video_codec_values[video_choice - 1]
    selected_audio_codec = audio_codec_values[audio_choice - 1]
    output_file_dir, output_file_name = manageOutput(dir)
    if output_file_dir == -1 and output_file_name == -1:
        return -1
    output_file = os.path.join(output_file_dir, output_file_name + os.path.splitext(input_file)[1])

    try:
        input_ffmpeg = ffmpeg.input(input_file)
        input_video = input_ffmpeg['v']
        input_audio = input_ffmpeg['a']
        try:
            input_subtitle = input_ffmpeg['s']
        except KeyError:
            input_subtitle = None

        if input_subtitle:
            output_ffmpeg = ffmpeg.output(
                input_video, input_audio, input_subtitle, output_file,
                vcodec=selected_video_codec, acodec=selected_audio_codec, scodec='copy', preset='ultrafast'
            )
        else:
            output_ffmpeg = ffmpeg.output(
                input_video, input_audio, output_file,
                vcodec=selected_video_codec, acodec=selected_audio_codec, preset='ultrafast'
            )
        ffmpeg.run(output_ffmpeg)
        success(f"Video Codec and Audio Codec of {input_file} have been successfully converted from {codecs[0]} and {codecs[1]} to {selected_video_codec} and {selected_audio_codec} respectively")
    except ffmpeg.Error as e:
        error(f"FFmpeg Error: {str(e)}")
        if e.stderr:
            error(f"ERROR DETAILS: {e.stderr.decode('utf-8')}")
    except Exception as e:
        error(f"Unexpected Error: {str(e)}")

def changeCodecs(dir):
    """
    Interactive function to let user change codecs of a video or audio file.
    """
    file, codecs = getCodecs(dir, ['Change Codecs of a Video File', 'Change Codecs of an Audio File'])
    if file == -1 and codecs == -1:
        return

    ext = os.path.splitext(file)[1].lower()
    if ext in getExtensions('Video'):
        media_type = 'Video'
    elif ext in getExtensions('Audio'):
        media_type = 'Audio'
    else:
        error("An Error Occurred!")
        return

    if len(codecs) > 1 and codecs[1]:
        success(f"Codec Information of {file}:\nVideo Codec: {codecs[0]}\nAudio Codec: {codecs[1]}")
    else:
        success(f"Codec Information of {file}:\nAudio Codec: {codecs[0]}")

    options = ['Change Video Codec', 'Change Audio Codec', 'Change Both'] if media_type == 'Video' else ['Change Audio Codec']

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

    while True:
        ch = menu("What do you want to change?", options)
        if ch == len(options) + 1:
            return
        elif ch == -1:
            continue

        if media_type == 'Video':
            if ch == 1:
                while True:
                    ch2 = menu('Select the Resultant Video Codec:', video_codec_list)
                    if ch2 == len(video_codec_list) + 1:
                        break
                    elif ch2 == -1:
                        continue
                    if changeVideoCodec(file, dir, codecs[0], ch2, video_codec_values) == -1:
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
                    if changeAudioCodec(file, dir, codecs[1], ch2, audio_codec_values) == -1:
                        continue
                    else:
                        return
            else:  # Change Both
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
                        if changeBoth(file, dir, codecs, ch2, video_codec_values, ch3, audio_codec_values) == -1:
                            continue
                        else:
                            return

        else:  # Audio only
            if ch == 1:
                while True:
                    ch2 = menu('Select the Resultant Audio Codec:', audio_codec_list)
                    if ch2 == len(audio_codec_list) + 1:
                        break
                    elif ch2 == -1:
                        continue
                    if changeAudioCodec(file, dir, codecs[0], ch2, audio_codec_values) == -1:
                        continue
                    else:
                        return

