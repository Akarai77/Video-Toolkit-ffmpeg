from convert import handle_convert
from ytconvert import ytconvert
from extract import handle_extract
from get_codecs import get_codecs
from colorPrint import *
from menu import menu
from change_codecs import change_codecs
from clips import handle_clips

options = ['YT Video Conversion','Convert','Extract','Get Audio and Video Codecs','Change Audio and video codecs','Turn Video into Clips']

while True:
    choice = menu(f"\t\tWELCOME!\n{'-'*50}\nWhat would you like to do today?",options)
    if choice == len(options)+1:
        break
    elif choice == -1:
        continue
    match choice:
        case 1 : 
            msg,output = ytconvert()
            if msg != -1 and output != -1:
                success(f"{msg}{output}") 
            else:
                continue
        case 2 : 
            handle_convert()
            
        case 3:
            handle_extract()
                
        case 4 :
            try:
                _,cds = get_codecs()
                if _ != -1 and cds != -1:
                    success(f"Video Codec: {cds[0]}",end="")
                    if cds[1]:
                        success(f"Audio Codec: {cds[1]}")
            except Exception:
                error("An Error Occured!")
            
        case 5:
            change_codecs()
        
        case 6:
            handle_clips()
        
        case 7 : 
            exit()
            
        case default: 
            print("\nINVALID CHOICE!")
        