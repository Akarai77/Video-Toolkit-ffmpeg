from colorama import Fore, Style

def error(msg, end='\n'):
    print(f"{Fore.RED}{msg}{Style.RESET_ALL}", end=end)

def success(msg, end='\n'):
    print(f"{Fore.GREEN}{msg}{Style.RESET_ALL}", end=end)

