import os
import yt_dlp
from .menu import menu
from .colorPrint import *
from .IOFunctions import manageOutput

def getAvailableResolutions(url):
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
                    'resolution': f.get('resolution') or f.get('format_note') or 'Unknown',
                    'filesize': filesize,
                    'vcodec': f['vcodec']
                }
                index += 1

        print("\nAvailable resolutions:\n")
        print(f"\t{'NO':<5}{'RESOLUTION':<15}{'FILE SIZE':<20}{'VCODEC'}")
        for res, res_info in resolutions.items():
            print(f"\t{str(res):<6}{res_info['resolution']:<15}{res_info['filesize']:<15}{res_info['vcodec']}")
        print(f"\t{len(resolutions) + 1}    EXIT\n")
        try:
            ch = int(input("Select a Resolution: "))
        except ValueError:
            error("INVALID INPUT! ONLY ENTER NUMBERS!")
            return -1
        if ch == len(resolutions) + 1:
            return -1
        elif ch < 1 or ch > len(resolutions):
            error("INVALID CHOICE!")
            return -1
        else:
            return resolutions[ch]['format_id']

def ytConvert(dir):
    while True:
        url = input("\nPaste the YouTube Video URL (0 to exit): ").strip()
        if url == '0':
            return -1, -1
        try:
            ydl_opts = {}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                yt_title = info_dict.get('title', 'Unknown Title')
        except Exception:
            error("INVALID URL or yt-dlp Error")
            continue
        break

    options = ['Convert to Video', 'Convert to Audio']
    sub_options = [
        {
            'Convert to MP4': 'mp4',
            'Convert to MKV': 'mkv',
            'Convert to WEBM': 'webm'
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
            return -1, -1
        elif ch == -1:
            continue

        sub_options_keys_list = list(sub_options[ch - 1].keys())
        sub_options_values_list = list(sub_options[ch - 1].values())

        while True:
            ch2 = menu("Select a Format: ", sub_options_keys_list)
            if ch2 == len(sub_options_keys_list) + 1:
                break
            elif ch2 == -1:
                continue

            output_dir, output_file = manageOutput(dir)
            if output_dir == -1 and output_file == -1:
                continue

            # For video, get format id and ask subtitle/description options
            if ch == 1:
                formatid = getAvailableResolutions(url)
                if formatid == -1:
                    continue
                while True:
                    sub = input("Write Subtitles [y/n] ?: ").lower()
                    if sub in ('y', 'n'):
                        break
                    error("INVALID!")
                while True:
                    desc = input("Write Description [y/n] ?: ").lower()
                    if desc in ('y', 'n'):
                        break
                    error("INVALID!")
                success(f"VIDEO TITLE: {yt_title}")

                output_template = os.path.join(output_dir, f"{output_file}.{sub_options_values_list[ch2 - 1]}")
                ydl_opts = {
                    'format': f"{formatid}+bestaudio",
                    'writeautomaticsub': sub == 'y',
                    'writesubtitles': sub == 'y',
                    'subtitleslangs': ['en'] if sub == 'y' else [],
                    'subtitlesformat': 'srt' if sub == 'y' else '',
                    'writedescription': desc == 'y',
                    'outtmpl': output_template,
                    'merge_output_format': sub_options_values_list[ch2 - 1]
                }
            else:
                # Audio only
                output_template = os.path.join(output_dir, f"{output_file}.{sub_options_values_list[ch2 - 1]}")
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': output_template,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': sub_options_values_list[ch2 - 1],
                        'preferredquality': '192',
                    }],
                }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                error(f"An error occurred: {e}")
                return -1, -1

            if ch == 2:
                return f"Audio of {yt_title} downloaded and converted to", output_template
            else:
                return f"{yt_title} downloaded to", output_template

