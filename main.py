import sys, os, json, info, subprocess, time
from pathlib import Path
from internal_utils import divider, delline, choice


from tqdm import tqdm

os.system("cls")
print("Starting pyTerm...")
locationOfTerminal = os.getcwd() + '\\'
pyTermDump = {}
fileLocations = {}
filelist = []
runtimeVars = {}
runlist = []
PATH = []
if len(sys.argv) > 1:
    if os.path.exists(sys.argv[1]):
        cwd = sys.argv[1] + '\\'
    else:
        print("The given path does not exist")
        cwd = locationOfTerminal
else:
    cwd = locationOfTerminal
if os.path.exists("isinstalled"):
    internalFileLocations = {"dir": f"{locationOfTerminal}\\dir\\dir.exe", "info": "info.exe", "help": "help.exe", "request" : f"{locationOfTerminal}\\dir\\request.exe"}
else:
    internalFileLocations = {"dir": "dir.py", "info": "info.py", "help": "help.py", "request" : "request.py"} 
with open ("pyTerm.dump", "a+") as pyTerm:
    pyTerm.seek(0)
    try:
        pyTermDump = json.load(pyTerm)
    except:
        pass 
with open("pyTerm.path", 'a+') as pathfile:
            for i in pathfile.read().split("\n"):
                print(i)
                PATH.append(i)  
def mergeDict(dict1, dict2):
    res = {**dict1, **dict2}
    return res
def findvars(txt):
    if txt.count("%") > 0:
        temps = []
        string = ""
        started = [False, 1]
        index = 0
        
        if txt.count("%") % 2 != 0:
            return("An opened variable expression was not closed.")
        
        for i in txt:
            if i == "%" and started[0] == False: #start a variable expression
                temps.append("") #create an empty string to input the variable name later
                string = string + '%' #add the % back to the string for reconstruction later
                started = [True, index] #set started to true and set the index of the start of the variable expression
            if started[0] == False:
                string = string + i #add the character to the string
            elif i == "%" and started[0] == True and index != started[1]:
                started[0] = False #end the variable expression
            if started[0] == True:
                if not index == started[1]: #if the index is not the same as the start of the variable expression
                    temps[len(temps)-1] = temps[len(temps)-1] + i #add the character to the variable name
            index += 1
            
        vars = mergeDict(globals(), runtimeVars)
        errorMsg = "Variables "
        
        for i in temps:
            if not i in vars:
                if errorMsg[len(errorMsg) - 1 ] == "'" :
                    errorMsg = errorMsg + ","
                errorMsg = errorMsg + "'"+ i + "'"
        errorMsg = errorMsg + " were not found."
        if not errorMsg == "Variables  were not found.": 
            return((errorMsg, "Some", True)) 
        
        index = 0
        for i in temps:
            temps[index] = str(vars.get(i))
            index += 1
            
        index = 0   
        while index <= string.count('%'):
            string = string.replace('%', temps[index], 1) #replace occurences of variable expressions with the variable value
            index += 1
            
        return((string, temps, False))   
    else:
        return(txt, None, False)
def parsecmd(cmd):
    cmd = findvars(cmd)
    if cmd[2] == True:
        return(cmd[0])
    cmd = cmd[0] #we don't need the other stuff
    temp = ""
    args = []
    
    for i in cmd:
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
    global PATH, cwd, runlist, fileLocations, internalFileLocations, filelist
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
    if internalFileLocations.get(cmd[0]) != None:
        runlist = [internalFileLocations[cmd[0]]]
        for i in cmd[1:]:
            runlist.append(i)
        return(runlist)
    
        
    for i in tqdm(local_path, leave = False, desc = " Search Host"): # for each path in PATH and current directory
        j = ""
        
        for j in tqdm(os.listdir(i), leave = False, desc = f"Subdir Search, {i+j}"): # for each subdirectory and file in i
            if os.path.isfile(i+j):
                if not i+j in filelist:
                    filelist.append(i+j)
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
    global fileLocations, filelist
    j = ""
    for j in tqdm(os.listdir(path), leave = False, desc = f"Recursible Host, {path + j}"): # for each subdirectory and file the given path
            if os.path.isfile(i+j):
                if not i+j in filelist:
                     filelist.append(path+j)
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
    print(findvars(p)[0])    
def SET(key, value):
    global runtimeVars
    runtimeVars[key] = value
    
     
while True:
    
    cleanPath(PATH)
    run = 0
    cmd = input(f"{cwd}^> ")
    unparsedCmd = cmd
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
    if cmd[0] == "echo":
        run = 1
        echo(unparsedCmd[len(cmd[0]) + 1:])   
        
    if cmd[0] == "SET":
        run = 1
        if len(cmd) == 4:
            
            if cmd[2] == "=":
                SET(cmd[1], cmd[3])
            else:
                print("Invalid Syntax (SET a = b)")
        else:
            print("Not enough / too many arugments (SET a = b)")
            
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
    