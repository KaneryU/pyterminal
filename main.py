import sys
import os
import json
import info
import subprocess
from pathlib import Path
from internal_utils import divider, delline, choice


from tqdm import tqdm

os.system("cls")
print("Starting pyTerm...")
with open ("pyTerm.txt", "a+") as pyTerm:
    pyTerm.seek(0)
    try:
        dump = json.load(pyTerm)
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
    global cwd
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
        
def find(cmd):
    global PATH
    global cwd
    global runlist
    local_path = []

    for i in PATH:
        local_path.append(i)
    iter = 0
        
    local_path.append(cwd)
    
    for i in local_path:
        if i[len(i) - 1] != "\\":
            local_path[iter] = local_path[iter] + "\\"
        iter += 1
        
    runlist = []
    
    

         
    for i in tqdm(local_path, leave = False): # for each path in PATH and current directory
        
        
        for j in tqdm(os.listdir(i), leave = False): # for each subdirectory and file in i
            
            if os.path.isdir(i + j + '\\'): # if it is a directory
                
                #print(i + j + r"\\" + cmd[0])
                
                if os.path.exists(i + j + cmd[0]): # does the file exist here?
                    
                    runlist = [i + j + r"\\" + cmd[0]] # if yes, then run it
                    
                    for k in cmd[1:]:
                        
                        runlist.append(k) # also add all arguments
                        
                    return(runlist)
                
                elif not os.listdir(i + j) == []:
                    
                    findRecusable(i + j + '\\', cmd)        
                        
            elif i + j == i + cmd[0]:
                
                runlist = [i + j] # if yes, then run it
                
                for k in cmd[1:]:
                    
                    runlist.append(k) # also add all arguments
                return(runlist)         
                       
            

                    
                    
    return([]) # if you reached here, the file was not found

def findRecusable(path, cmd):
    
    for j in tqdm(os.listdir(path), leave = False): # for each subdirectory and file the given path
            
            if os.path.isdir(path + j + '\\'): # if it is a directory
                
                #print(path + j + r"\\" + cmd[0])
                
                if os.path.exists(path + j + cmd[0]): # does the file exist here?
                    
                    runlist = [path + j + r"\\" + cmd[0]] # if yes, then run it
                    
                    for k in cmd[1:]:
                        
                        runlist.append(k) # also add all arguments
                        
                    return(runlist)
                
                elif not os.listdir(path + j) == []:
                    
                    findRecusable(path + j + '\\', cmd)        
                        
            elif os.path.exists(path + j + '\\' + cmd[0]):
                
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
            for i in pathfile:
                if not i in PATH or i == "" or i == "\n":
                  PATH.append(i)
      
def cleanPath():
    iter = 0               
    for i in PATH:
        if i == "" or i == "\n":
            PATH.remove(i)
        if not os.path.exists(i):
            PATH.remove(i)
        if i[len(i) - 1] != "\\":
            PATH[iter] = PATH[iter] + "\\"
        iter += 1
    
while True:
    cleanPath()
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
            for i in PATH:
                print(i)

    if run == 0:
        try:
            runlist = find(cmd)
        except PermissionError as e:
            print("PermisionError: " + str(e))                   
        if runlist == []:
            if 1 == 1: #enable or disable printing path and arugments
                print("Command not found.")    