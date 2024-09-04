from colorPrint import error

def menu(title,array):
    print(f"\n{title}:\n")
    for i,item in enumerate(array,start=1):
        print(f"\t{i} : {item}")
    print(f"\t{len(array)+1} : EXIT")

    try:
        choice = int(input("\nEnter your choice: "))
    except ValueError:
        error("INVALID INPUT! Please Enter A Number!")
        return -1
    
    if choice < 1 or choice > len(array)+1:
        error("INVALID INPUT!")
        return -1
    else:
        return choice