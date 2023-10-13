import shutil
        
class screen:
    def __init__(self):
        self.screenWidth, self.screenHeight = shutil.get_terminal_size()
      
if __name__ == "__main__":
    print("This is a module, not a program.")
    print("Please run the main program.")
    input("Press enter to exit.")
    exit() 
         
def textCenter(text, screenWidth, divider_ = "█"):
    return(text.center(screenWidth, divider_))

def textLeft(text, screenWidth, divider_ = "█"):
    return(text.ljust(screenWidth - len(text), divider_))

def textRight(text, screenWidth, divider_ = "█"):
    
    return(text.rjust(screenWidth - len(text), divider_))
    
