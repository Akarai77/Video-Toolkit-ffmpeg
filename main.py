from core.convert import handleConvert
from core.ytConvert import ytConvert
from core.extract import handleExtract
from core.getCodecs import getCodecs
from core.colorPrint import *
from core.menu import menu
from core.IOFunctions import getInput
from core.changeCodecs import changeCodecs
from core.clips import handleClips
from core.changeAspectRatio import changeAspectRatio

options = [
    'Set Working Directory',
    'YT Video Conversion',
    'Convert',
    'Extract',
    'Get Audio and Video Codecs',
    'Change Audio and video codecs',
    'Turn Video into Clips',
    'Change Aspect Ratio'
]
wrking_dir = '.'

while True:
    choice = menu(
        f"\t\tWELCOME!\n{'-'*50}\nCURRENT DIRECTORY: {wrking_dir}\nWhat would you like to do today?",
        options
    )
    
    if choice == len(options) + 1:
        break
    elif choice == -1:
        continue

    match choice:
        case 1:
            file_dir, _, __ = getInput('Dir', wrking_dir)
            if not file_dir:
                continue
            wrking_dir = file_dir[0]

        case 2: 
            msg, output = ytConvert(wrking_dir)
            if msg != -1 and output != -1:
                success(f"{msg}{output}") 
            else:
                continue

        case 3: 
            handleConvert(wrking_dir)

        case 4:
            handleExtract(wrking_dir)

        case 5:
            try:
                file, cds = getCodecs(wrking_dir)
                if file != -1 and cds != -1:
                    if cds[1]:
                        success(f"Codec Information of {file}:\nVideo Codec : {cds[0]}\nAudio Codec : {cds[1]}")
                    else:
                        success(f"Codec Information of {file}:\nAudio Codec : {cds[0]}")
            except Exception:
                error("An Error Occurred!")

        case 6:
            changeCodecs(wrking_dir)

        case 7:
            handleClips(wrking_dir)

        case 8:
            changeAspectRatio(wrking_dir)

        case 9:
            exit()

        case _:
            print("\nINVALID CHOICE!")

