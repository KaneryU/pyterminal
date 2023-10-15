import sys
import os
import datetime
from internal_utils import delline, divider
from tqdm import tqdm
import json
import regex

args = sys.argv
with open ("pyTerm.dump", "a+") as pyTerm:
    pyTerm.seek(0)
    try:
        pyTermDump = json.load(pyTerm)
    except:
        print("Failed getting cwd from " + pyTerm.name)
    
cwd = pyTermDump["cwd"]

screen = divider.screen()
def toReadable(input):
    return (datetime.datetime.fromtimestamp(input).strftime('%Y-%m-%d %H:%M:%S'))

def get_size(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def parse(dirlist, wd = cwd):
    retlist = []
    screen_divisions = screen.screenWidth // 4
   #add the headers                                                                                                                                                                                             I live off the jank ˅
    retlist.append(divider.textLeft("Type", screen_divisions + 1, ' ') + divider.textCenter("Size", screen_divisions, ' ') + divider.textCenter("Name", screen_divisions, ' ') + divider.textRight(f"Last Modified", screen_divisions - 9, " "))
    retlist.append("")
    
    for i in tqdm(dirlist, leave = False):
        lastModified = toReadable(os.path.getmtime(wd + i))
        
        if os.path.isfile(wd + i):
            retlist.append(divider.textLeft("File", screen_divisions, ' ') + divider.textCenter(str(os.path.getsize(wd + i)), screen_divisions, ' ') + divider.textCenter(i , screen_divisions, ' ') + divider.textRight(f"{lastModified}", screen_divisions, " "))
       
        if os.path.isdir(wd + i):
            retlist.append(divider.textLeft("Dir ", screen_divisions, ' ') + divider.textCenter(str(get_size(wd + i)), screen_divisions, ' ') + divider.textCenter(i , screen_divisions, ' ') + divider.textRight(f"{lastModified}", screen_divisions, " "))
    
    return(retlist)

def sort(dirlist, wd = cwd):
    templist = []
    if wd == "dir/file":
        for i in dirlist:
            if os.path.isdir(i):
                templist.append(i)
        for i in dirlist:
            if os.path.isfile(i):
                templist.append(i)       
        return(templist)
    
    elif wd == "file/dir":
        for i in dirlist:
            if os.path.isfile(i):
                templist.append(i)
        for i in dirlist:
            if os.path.isdir(i):
                templist.append(i)
        return(templist)
    
    elif wd == "date":
        datelist = []
        templist = []
        templist.extend([""] * len(dirlist))
        for i in dirlist:
            datelist.append(os.path.getmtime(i))
            datelist.sort()
        for i in dirlist:
            index = datelist.index(os.path.getmtime(i))
            datelist.pop(index)
            templist[index] = i
        return templist  
     
    elif wd == "dir/date":
        datelist = []
        
        templistDir = []
        templistDir2 = []
        for i in dirlist:
            if os.path.isdir(i):
                templistDir.append(i)
        templistDir2.extend([""] * len(templistDir)) 
               
        templistFile = []
        templistFile2 = []
        for i in dirlist:
            if os.path.isfile(i):
                templistFile.append(i)
        templistFile2.extend([""] * len(templistFile))
        
        for i in templistDir:
            datelist.append(os.path.getmtime(i))
            datelist.sort()
        for i in templistDir:
            index = datelist.index(os.path.getmtime(i))
            datelist.pop(index)
            templistDir2[index] = i
        
        for i in templistFile:
            datelist.append(os.path.getmtime(i))
            datelist.sort()
        for i in templistDir:
            index = datelist.index(os.path.getmtime(i))
            datelist.pop(index)
            templistFile2[index] = i    
        
        for i in templistDir2:
            templist.append(i)
        for i in templistFile2:
            templist.append(i)    
            
        return templist     
    
          
            
if len(args) == 1:
    # No args, list all subdirectories of current directory
    dir_list = os.listdir(cwd)
    dir_list = parse(dir_list)
    for i in dir_list:
        print(i)
    
if len(args) > 1:
    '''
    -h / -help = print this message
    {search query} = search in directory
    -s / -sort:{date}/{size}/{name} = sort the results.
    '''
    run = 0
    
    if args[1] == "-h" or args[1] == "-help":
        run = 1
        print("-h / -help = print this message \n{search query} = search in directory\n-s / -sort {date}/{size}/{name} to sort the results.")
        
    elif args[1] == "-s" or args[1] == "-sort":
        if len(args) == 3:
            dir_list = parse(os.listdir(cwd))    
     
    elif args[1] == "-p" or args[1] == "-path":
        if len(args) == 3:
            dir_list = os.listdir(args[2])
            dir_list = parse(dir_list)
            for i in dir_list:
                print(i)
        
    else: # if the argument is a search query
        dir_list = os.listdir(cwd)
        temp = args[1].replace('*', '.*', 1)
        
        for i in tqdm(dir_list, leave = False):
            #print(str(regex.match(f"{temp}", i)) + " " + i)
            if str(regex.match(f"{temp}", i)) == "None":
                dir_list.remove(i)
                
        
        
        dir_list = parse(dir_list)
        for i in tqdm(dir_list, leave = False):
            print(i)

        
