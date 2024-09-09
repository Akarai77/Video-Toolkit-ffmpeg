from convert import handleConvert
from ytConvert import ytConvert
from extract import handleExtract
from getCodecs import getCodecs
from colorPrint import *
from menu import menu
from changeCodecs import changeCodecs
from clips import handleClips
from changeAspectRatio import changeAspectRatio

options = ['YT Video Conversion','Convert','Extract','Get Audio and Video Codecs','Change Audio and video codecs','Turn Video into Clips','Change Aspect Ratio']

while True:
    choice = menu(f"\t\tWELCOME!\n{'-'*50}\nWhat would you like to do today?",options)
    if choice == len(options)+1:
        break
    elif choice == -1:
        continue
    match choice:
        case 1 : 
            msg,output = ytConvert()
            if msg != -1 and output != -1:
                success(f"{msg}{output}") 
            else:
                continue
        case 2 : 
            handleConvert()
            
        case 3:
            handleExtract()
                
        case 4 :
            try:
                _,cds = getCodecs()
                if _ != -1 and cds != -1:
                    success(f"Video Codec: {cds[0]}",end="")
                    if cds[1]:
                        success(f"Audio Codec: {cds[1]}")
            except Exception:
                error("An Error Occured!")
            
        case 5:
            changeCodecs()
        
        case 6:
            handleClips()
            
        case 7:
            changeAspectRatio()
        
        case 8: 
            exit()
            
        case default: 
            print("\nINVALID CHOICE!")
        