import os
import yt_dlp
import ffmpeg
from menu import menu
from colorPrint import *
from IO_functions import manageOutput

def ytconvert():
    while True:
        try:
            url = input("\nPaste the YouTube Video URL: ")
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                yt_title = info_dict.get('title', None)
        except Exception as e:
            error(f"INVALID URL or yt-dlp Error")
            continue
        break

    options = ['Convert to Video', 'Convert to Audio']
    sub_options = [
        {
            'Convert to MP4': 'mp4',
            'Convert to MKV': 'mkv',
            'Convert to WEBM': 'webm',
        },
        {
            'Convert to MP3': 'mp3',
            'Convert to M4A': 'm4a',
            'Convert to WAV': 'wav',
            'Convert to FLAC': 'flac',
        }
    ]

    while True:
        ch = menu('Select an option', options)
        if ch == len(options) + 1:
            return
        elif ch == -1:
            continue
        else:
            while True:
                sub_options_keys_list = list(sub_options[ch-1].keys())
                sub_options_values_list = list(sub_options[ch-1].values())
                ch2 = menu("Select a Format: ", sub_options_keys_list)
                if ch2 == len(sub_options_keys_list) + 1:
                    break
                elif ch2 == -1:
                    continue
                else:
                    try:
                        output_dir, output_file = manageOutput()
                        output_template = os.path.join(output_dir, f"{output_file}.%(ext)s")

                        if ch == 1:  # Video
                            while True:
                                sub = input("Write Subtitles [y/n] ?: ").lower()
                                if not (sub =='y' or sub == 'n'):
                                    error("INVALID!")
                                    continue
                                desc = input("Write Decription [y/n] ?: ").lower()
                                if not (desc =='y' or desc == 'n'):
                                    error("INVALID!")
                                    continue
                                break
                            
                            ydl_opts = {
                                'format': 'bestvideo+bestaudio/best',
                                'writeautomaticsub': True if sub == 'y' else False,  # Download automatically generated subtitles if no subtitles are available
                                'writesubtitles': True if sub == 'y' else False,  # Downloads subtitles
                                'subtitleslangs': ['en'] if sub == 'y' else [],  # Specifies the language for subtitles
                                'subtitlesformat': 'srt' if sub == 'y' else '',  # Subtitle format
                                'writedescription': True if desc == 'y' else False,
                                'outtmpl': output_template,
                                'merge_output_format': sub_options_values_list[ch2-1]
                            }
                        else:  # Audio
                            ydl_opts = {
                                'format': 'bestaudio/best',
                                'outtmpl': output_template,
                                'postprocessors': [{
                                    'key': 'FFmpegExtractAudio',
                                    'preferredcodec': sub_options_values_list[ch2-1],
                                    'preferredquality': '192',
                                }],
                            }

                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            ydl.download([url])

                        if ch == 2:
                            audio_output_path = os.path.splitext(output_template)[0] + '.' + sub_options_values_list[ch2-1]
                            success(f"Audio downloaded and converted to {audio_output_path}")
                            return
                        else:
                            success(f"Video downloaded to {output_template}")
                            return

                    except ffmpeg.Error as e:
                        error(f"FFmpeg Error: {str(e)}")
                    except Exception as e:
                        error(f"An error occurred: {e}")
                    break