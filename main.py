import sys, os, json, info, subprocess, time
from pathlib import Path
from internal_utils import divider, delline, choice


from tqdm import tqdm

os.system("cls")
print("Starting pyTerm...")
pyTermDump = {}
fileLocations = {}
with open ("pyTerm.dump", "a+") as pyTerm:
    pyTerm.seek(0)
    try:
        pyTermDump = json.load(pyTerm)
    except:
        pass

def parsecmd(cmd):
    temp = ""
    args = []
    for i in tqdm(cmd, leave = False, desc = "Parsing command", disable = True):
        temp += i
        if i == " ":
            args.append(temp[0:len(temp)-1])
            temp = ""
    args.append(temp)
    #print(args)
    return(args)


def cd(cmd):
    global cwd, pyTermDump
    if len(cmd) > 1:
        if cmd[1] == "..":
            if os.path.exists(Path(cwd).parents[0]):
                cwd = str(Path(cwd).parents[0])
            else:
                print("Path does not exist.")
        else:
            if os.path.exists(cmd[1]):
                cwd = cmd[1] 
            else:
                print("Path does not exist.")
    else:
        print(cwd)
    pyTermDump["cwd"] = cwd
    with open ("pyTerm.dump", "w") as pyTerm:
        json.dump(pyTermDump, pyTerm)
    return(cwd)
        
def find(cmd):
    global PATH, cwd, runlist, fileLocations
    local_path = []

    for i in PATH:
        local_path.append(i)
    iter = 0
        
    local_path.append(cwd)
    
    cleanPath(local_path)    
    runlist = []
    
    if fileLocations.get(cmd[0]) != None:
        runlist = [fileLocations[cmd[0]]]
        for i in cmd[1:]:
            runlist.append(i)
        return(runlist)

         
    for i in tqdm(local_path, leave = False, desc = " Search Host"): # for each path in PATH and current directory
        j = ""
        
        for j in tqdm(os.listdir(i), leave = False, desc = f"Subdir Search, {i+j}"): # for each subdirectory and file in i
            
            if os.path.isdir(i + j + '\\'): # if it is a directory
                
                #print(i + j + r"\\" + cmd[0])
                
                if os.path.exists(i + j + cmd[0]): # does the file exist here?
                    
                    runlist = [i + j + r"\\" + cmd[0]] # if yes, then run it
                    
                    for k in cmd[1:]:
                        
                        runlist.append(k) # also add all arguments
                    fileLocations[cmd[0]] = i + j + r"\\" + cmd[0]    
                    return(runlist)
                
                elif not os.listdir(i + j) == []:
                    
                    findRecusable(i + j + '\\', cmd)        
                        
            elif i + j == i + cmd[0]:
                fileLocations[cmd[0]] = i + j
                runlist = [i + j] # if yes, then run it
                
                for k in cmd[1:]:
                    
                    runlist.append(k) # also add all arguments
                    
                return(runlist)         
                       
            

                    
                    
    return([]) # if you reached here, the file was not found

def findRecusable(path, cmd):
    global fileLocations
    j = ""
    for j in tqdm(os.listdir(path), leave = False, desc = f"Recursible Host, {path + j}"): # for each subdirectory and file the given path
            if os.path.isdir(path + j + '\\'): # if it is a directory
                
                #print(path + j + r"\\" + cmd[0])
                
                if os.path.exists(path + j + cmd[0]): # does the file exist here?
                    
                    runlist = [path + j + "\\" + cmd[0]] # if yes, then run it
                    
                    for k in cmd[1:]:
                        
                        runlist.append(k) # also add all arguments
                        
                    return(runlist)
                
                elif not os.listdir(path + j) == []:
                    
                    findRecusable(path + j + '\\', cmd)        
                        
            elif os.path.exists(path + j + '\\' + cmd[0]):
                fileLocations[cmd[0]] = i + j  + cmd[0]
                runlist = [path + j + r"\\" + cmd[0]] # if yes, then run it
                
                for k in cmd[1:]:
                    
                    runlist.append(k) # also add all arguments
                return(runlist)         
                        
            

                
    return([])
locationOfTerminal = os.getcwd() + '\\'

if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        cwd = sys.argv[1] + '\\'
    else:
        print("The given path does not exist")
        cwd = locationOfTerminal
else:
    cwd = locationOfTerminal
    
runlist = []
PATH = []
with open("pyTerm.path", 'r') as pathfile:
            for i in pathfile.read().split("\n"):
                print(i)
                PATH.append(i)
      
def cleanPath(PATH_):
    if len(PATH_) > 1:
        iter = 0               
        while iter < len(PATH_):
            if PATH_[iter] == "" or PATH_[iter] == "\n":
                del PATH_[iter]
            if not os.path.exists(PATH_[iter]) and PATH_[iter] in PATH_:
                del PATH_[iter]
            if PATH_[iter][len(PATH_[iter]) - 1] != "\\":
                PATH_[iter] = PATH_[iter] + "\\"
            iter += 1
def echo(p):
    print("Echo is uncompleted")
    print(p)      
     
while True:
    cleanPath(PATH)
    run = 0
    cmd = input(f"{cwd}^> ")
    cmd = parsecmd(cmd)
    if not cwd[len(cwd)-1] == "\\":
        cwd = cwd + '\\'
    
    if cmd[0] == "":
        print("Please enter a command.")
        run = 1
    if cmd[0] == "exit" or cmd[0] == "quit":
        with open("pyTerm.path", 'w') as pathfile:
            iter = 0
            for i in PATH:
                if iter == 0:
                    pathfile.write(i)
                else:
                    pathfile.write("\n" + i)
        
        input("Press any key to exit...")
        sys.exit()
        
    if cmd[0] == "cd":
        run = 1
        cd(cmd)
    if cmd[0] == "PATH":
        run = 1
        if len(cmd) > 1:
            if cmd[1] == '-h':
                print(
                    '''
                    Arguments:\n
                    \n
                    -h: Display this message\n
                    -r: Replace with new given paths (not recomended)\n
                    -a: Add new paths to the current path (default)\n
                    No Arguments: Print the current path\n
                    '''
                )
            elif not cmd[1][0] == '-' or cmd[1] == '-a':
                if not cmd[1][0] == '-':
                    for i in cmd[1:]:
                        if os.path.exists(i):
                            PATH.append(i)
                        else:
                            print(i + " Was not added to path becuase it isn't a valid path")
                        
                elif cmd[1] == '-a':
                    
                    for i in cmd[2:]:
                        if os.path.exists(i):
                            PATH.append(i)
                        else:
                            print(i + " Was not added to path becuase it isn't a valid path")
                        
            elif cmd[1] == '-r':
                
                if choice.choice("Are you sure you want to delete the current path and replace it?", ['Y', 'N']):
                    PATH = []
                    for i in cmd[2:]:
                        if os.path.exists(i):
                            PATH.append(i)
                        else:
                            print(i + " Was not added to path becuase it isn't a valid path")
        else: 
            if len(PATH) == 0:
                print("Path is empty.")
            else:
                for i in PATH:
                    if not i == "":
                        print(i)
                    else:
                        print("Empty Item")
    if cmd[0] == "_fileLocations":
        for i in fileLocations:
            print(i + ": " + fileLocations[i])
            
    if run == 0:
        try:
            runlist = find(cmd)
        except PermissionError as e:
            print("PermisionError: " + str(e))                   
        if runlist == []:
            if 1 == 1: #enable or disable printing path and arugments
                print("Command not found.")
        else:
            subprocess.run(runlist, shell = True)    