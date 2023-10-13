if __name__ == "__main__":
    print("This is a module, not a program.")
    print("Please run the main program.")
    input("Press enter to exit.")
    exit() 




def choice(Desc, opt):
    print(f"{Desc} [{opt[1].upper}/{opt[2].upper}]")
    given = "ghgafgjkjgalkjfjhgjjhjhgrjhrljshg" #There's no way one of the options contain this
    while not given.upper == opt[1].upper or given == opt[2].upper:
        given.upper = input().upper
    
    if given.upper == opt[1].upper:
        return(True)
    if given.upper == opt[2].upper:
        return(False)