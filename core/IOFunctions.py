import os
import re
from .menu import menu
from .colorPrint import error

def get_drives():
    """Return a list of existing drives like ['C:\\', 'D:\\', ...] on Windows."""
    return [f"{d}:\\" for d in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{d}:\\")]

def navigate_directory(dir, drive_flag, type):
    """
    Return a tuple (choices, drive_flag) based on the current directory and drive_flag.
    Handles drive listing and directory contents.
    """
    drives = get_drives()
    if drive_flag:
        if type == 'Dir':
            choices = drives
        else:
            choices = [f'Search all {type} files'] + drives
    else:
        if type == 'Dir':
            choices = ["Select Directory"] + os.listdir(dir) + ["Previous Directory"]
        else:
            choices = [f"Search all {type} files"] + os.listdir(dir) + ["Previous Directory"]
    return choices, drives, drive_flag

def getFiles(dir, extensions):
    """
    Recursively find all files in 'dir' matching any of the given 'extensions'.
    Returns list of full paths.
    """
    files = [os.path.join(folder[0], file) for folder in os.walk(dir)
             for file in folder[2] if os.path.splitext(file)[1].lower() in extensions]
    return files

def getExtensions(type):
    """
    Return a list of valid file extensions based on the input type string.
    """
    match type:
        case 'Video':
            valid_extensions = ['.mp4', '.mkv', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mpeg', '.mpg', '.m4v']
        case 'Audio':
            valid_extensions = ['.mp3', '.aac', '.wav', '.flac', '.ogg', '.wma', '.alac', '.aiff', '.m4a', '.ac3']
        case 'Image':
            valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp']
        case 'Subtitle':
            valid_extensions = ['.srt', '.ass', '.ssa', '.sub', '.vtt']
        case 'GIF':
            valid_extensions = ['.gif']
        case _:
            valid_extensions = []
    return valid_extensions

def manageOutput(dir='.'):
    """
    Interactively prompt user to select an output directory and valid filename.
    Returns tuple (new_dir, new_name), or (-1, -1) on exit.
    """
    drive_flag = 0
    while True:
        print("Select an output Directory: ")
        while True:
            print(f"\nCurrent Directory: {os.path.abspath(dir)}", end="")
            choices, drives, drive_flag = navigate_directory(dir, drive_flag, 'Dir')
            
            ch = menu("Select an output Directory:", choices)
            if ch == -1:
                continue
            elif ch == 1:
                if os.path.isdir(dir):
                    new_dir = os.path.abspath(dir)
                    break
                else:
                    error("NOT A DIRECTORY!")
            elif ch == len(choices) and not drive_flag:
                if dir in drives:
                    drive_flag = 1
                else:
                    dir = os.path.abspath(os.path.join(dir, '..'))
                continue
            elif ch == len(choices) + 1:
                return -1, -1
            else:
                dir = os.path.join(dir, choices[ch - 1])
                if not os.path.isdir(dir):
                    error("NOT A DIRECTORY!")
                    dir = os.path.abspath(os.path.join(dir, '..'))
                    continue
                if drive_flag:
                    drive_flag = 0

        while True:
            new_name = input("Enter new output file name (0 to exit): ")
            if new_name == '0':
                break
            pattern = r'^[a-zA-Z0-9_.\-()]+$'  # added dot (.) support
            if re.match(pattern, new_name) is not None:
                return new_dir, new_name
            else:
                error("Invalid File Name!\nOnly use letters (a-z, A-Z), numbers (0-9), underscores (_), hyphens (-), dots (.), and parentheses (()).\n")
                continue

def getInput(type, dir='.'):
    """
    Interactively prompt user to select files or directories of specified type(s).
    Returns tuple of lists: (file_dirs, file_names, file_formats).
    """
    type_list = type.split('+')
    file_dir, file_name, file_format = [], [], []

    for type in type_list:
        drive_flag = 0
        while True:
            print(f"\nCurrent Directory: {os.path.abspath(dir)}", end="")
            choices, drives, drive_flag = navigate_directory(dir, drive_flag, type)
            
            ch = menu(f"Select an input Directory" if type == "Dir" else f"Select an input {type} file", choices)
            if ch == -1:
                continue
            elif ch == 1 and not drive_flag:
                if type == 'Dir':
                    if os.path.isdir(dir):
                        file_dir.append(os.path.abspath(dir))
                        break
                    else:
                        error("NOT A DIRECTORY!")
                        continue
                else:
                    dir_abs = os.path.abspath(dir)
                    file_list = getFiles(dir_abs, getExtensions(type))
                    if not file_list:
                        error(f"No {type} files found in {dir_abs}")
                        continue
                    while True:
                        basename_list = [os.path.basename(file) for file in file_list]
                        ch2 = menu(f"{type} Files in {dir_abs}", basename_list)
                        if ch2 == len(file_list) + 1:
                            break
                        elif ch2 == -1:
                            continue
                        else:
                            file = basename_list[ch2 - 1]
                            file_dir.append(os.path.dirname(file_list[ch2 - 1]))
                            file_name.append(os.path.splitext(file)[0])
                            file_format.append(os.path.splitext(file)[1])
                            break  # replaced exception break with break
                    break
            elif ch == len(choices) and not drive_flag:
                if dir in drives:
                    drive_flag = 1
                else:
                    dir = os.path.abspath(os.path.join(dir, '..'))
                continue
            elif ch == len(choices) + 1:
                return [], [], []
            else:
                item = os.path.join(dir, choices[ch - 1])
                if os.path.isfile(item):
                    if os.path.splitext(item)[1].lower() not in getExtensions(type):
                        error("Not a Directory") if type == 'Dir' else error(f"Not a {type} file")
                        continue
                    file = os.path.basename(item)
                    file_dir.append(os.path.dirname(item))
                    file_name.append(os.path.splitext(file)[0])
                    file_format.append(os.path.splitext(file)[1])
                    break
                elif os.path.isdir(item):
                    if drive_flag:
                        drive_flag = 0
                    dir = item
                    continue
                else:
                    error("Not a valid choice!")
                    continue
    return file_dir, file_name, file_format

