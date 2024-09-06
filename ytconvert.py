import os
import yt_dlp
import ffmpeg
from menu import menu
from colorPrint import *
from IO_functions import manageOutput


def get_available_resolutions(url):
    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        resolutions = {}
        index = 1
        for f in formats:
            if f.get('vcodec') != 'none':
                filesize = f.get('filesize')
                if filesize:
                    filesize = f"{round(filesize / (1024 * 1024), 2)} MB"
                else:
                    filesize = "Unknown"

                resolutions[index] = {
                    'format_id': f['format_id'],
                    'resolution': f['resolution'],
                    'ext': f['ext'],
                    'filesize': filesize,
                    'vcodec': f['vcodec']
                }
                index += 1
                
        print("Available resolutions:")
        print(f"{'NO':<5}{'RESOLUTION':<15}{'EXTENSION':<15}{'FILE SIZE':<20}{'VCODEC'}")
        for res, res2 in resolutions.items():
            print(f"{str(res):<6}{res2['resolution']:<17}{res2['ext']:<13}{res2['filesize']:<15}{res2['vcodec']}")
        print(f"{len(resolutions)+1}    EXIT")
        try:
            ch = int(input("Select a Resolution: "))
        except ValueError:
            error("INVALID INPUT! ONLY ENTER NUMBERS!")
        if ch == len(resolutions)+1:
            return -1
        elif ch < 1 and ch > len(resolutions)+1:
            error("INVLAID!")
        else:
            if ch in resolutions:
                return resolutions[ch]['format_id']
            else:
                error("INVALID!")
                



def ytconvert():
    while True:
        try:
            url = input("\nPaste the YouTube Video URL (0 to exit): ")
            if url == '0':
                return -1,-1
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
                        if output_dir == -1 and output_file == -1:
                            continue
                        output_template = os.path.join(output_dir, f"{output_file}.%(ext)s")

                        if ch == 1:
                            formatid = get_available_resolutions(url)
                            if formatid == -1:
                                continue
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
                                'format': formatid,
                                'writeautomaticsub': True if sub == 'y' else False,
                                'writesubtitles': True if sub == 'y' else False,
                                'subtitleslangs': ['en'] if sub == 'y' else [],
                                'subtitlesformat': 'srt' if sub == 'y' else '',
                                'writedescription': True if desc == 'y' else False,
                                'outtmpl': output_template,
                                'merge_output_format': sub_options_values_list[ch2-1]
                            }
                        else:
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
                            return "Audio downloaded and converted to",audio_output_path
                        else:
                            return "Video downloaded to",output_template
                    except Exception as e:
                        error(f"An error occurred: {e}")
                        return -1,-1