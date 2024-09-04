import os
import re
from menu import menu
from colorPrint import error

def getFiles(dir,extensions):
    files = [os.path.join(folder[0], file) for folder in os.walk(dir) for file in folder[2] if os.path.splitext(file)[1] in extensions]
    return files

def getExtensions(type):
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

def manageOutput():
    while True:
        print("Select an output Directory: ")
        dir = '.'
        while True:
            print(f"\nCurrent Directory: {os.path.abspath(dir)}",end="")
            choices = ["Select Directory"] + os.listdir(dir) + ["Previous Directory"]
            ch2 = menu("Select an output Directory:", choices)
            
            if ch2 == 1:
                if os.path.isdir(dir):
                    new_dir = os.path.abspath(dir)
                    break
                else:
                    error("NOT A DIRECTORY!")
            elif ch2 == len(choices):
                dir = os.path.abspath(os.path.join(dir, '..'))
                continue
            elif ch2 == len(choices) + 1:
                return -1,-1
            else:
                if os.path.isdir(dir):
                    dir = os.path.join(dir, choices[ch2 - 1])
                else:
                    error("NOT A DIRECTORY!")
                    continue
        
        while True:
            new_name = input("Enter new output file name: ")
            pattern = r'^[a-zA-Z0-9_\-()]+$'
            if re.match(pattern, new_name) is not None:
                return new_dir,new_name
            else:
                error("Invalid File Name!\nOnly use letters (a-z, A-Z), numbers (0-9), underscores (_), hyphens (-), and parentheses (()).")
                continue

def getInput(type):
    type_list = type.split('+')
    
    file_dir, file_name, file_format = [], [], []
    for type in type_list:
        dir = '.'
        while True:
            print(f"\nCurrent Directory: {os.path.abspath(dir)}",end="")
            choices = [f"Search all {type} files"] + os.listdir(dir) + ["Previous Directory"]
            ch = menu(f"Select an input {type} file", choices)
            
            if ch == 1:
                dir = os.path.abspath(os.path.join(dir,'.'))
                file_list = getFiles(dir, getExtensions(type))
                if not file_list:
                    error(f"No {type} files found in {dir}")
                    continue
                try:
                    while True:
                            basename_list = [os.path.basename(file) for file in file_list]
                            ch = menu(f"{type} Files in {dir}", basename_list)
                            if ch == len(file_list) + 1:
                                break
                            elif ch == -1:
                                continue
                            else:
                                file = basename_list[ch - 1]
                                file_dir.append(os.path.dirname(file_list[ch - 1]))
                                file_name.append(os.path.splitext(file)[0])
                                file_format.append(os.path.splitext(file)[1])
                                raise Exception
                except Exception:
                    break

            elif ch == len(choices):
                dir = os.path.abspath(os.path.join(dir, '..'))
                continue
            elif ch == len(choices) + 1:
                return [],[],[]
            elif ch == -1:
                continue
            else:
                item = os.path.join(dir, choices[ch - 1])
                if os.path.isfile(item):
                    if os.path.splitext(item)[1] not in getExtensions(type):
                        error(f"Not a {type} file")
                        continue
                    file = os.path.basename(item)
                    file_dir.append(os.path.dirname(item))
                    file_name.append(os.path.splitext(file)[0])
                    file_format.append(os.path.splitext(file)[1])
                    break
                elif os.path.isdir(item):
                    dir = item
                    continue
                else:
                    error("Not a valid choice!")
                    continue
    
    return file_dir,file_name,file_format