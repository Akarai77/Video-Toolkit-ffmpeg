from colorama import Fore

def error(msg,end='\n'):
    print(f"\n{Fore.RED}{msg}{Fore.WHITE}",end=end)
    
def success(msg,end='\n'):
    print(f"\n{Fore.GREEN}{msg}{Fore.WHITE}",end=end)