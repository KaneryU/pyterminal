import sys
import os
import datetime
from internal_utils import delline, divider
from tqdm import tqdm
import regex

args = sys.argv
cwd = os.getcwd() + "\\"
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
    retlist.append(divider.textLeft("Type", screen_divisions, ' ') + divider.textCenter("Size", screen_divisions, ' ') + divider.textCenter("Name", screen_divisions, ' ') + divider.textRight(f"Last Modified", screen_divisions - 9, " "))
    retlist.append("")
    
    for i in tqdm(dirlist, leave = False):
        lastModified = toReadable(os.path.getmtime(wd + i))
        
        if os.path.isfile(wd + i):
            retlist.append(divider.textLeft("File", screen_divisions, ' ') + divider.textCenter(str(os.path.getsize(wd + i)), screen_divisions, ' ') + divider.textCenter(i , screen_divisions, ' ') + divider.textRight(f"{lastModified}", screen_divisions, " "))
       
        if os.path.isdir(wd + i):
            retlist.append(divider.textLeft("Dir ", screen_divisions, ' ') + divider.textCenter(str(get_size(wd + i)), screen_divisions, ' ') + divider.textCenter(i , screen_divisions, ' ') + divider.textRight(f"{lastModified}", screen_divisions, " "))
    
    return(retlist)

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
    -s / -sort:{date}/{size}/{name} = sort (not available right now)
    '''
    run = 0
    
    if args[1] == "-h" or args[1] == "-help":
        run = 1
        print("-h / -help = print this message \n{search query} = search in directory\n-s / -sort {date}/{size}/{name} to sort the results.")
    elif args[1] == "-s" or args[1] == "-sort":
        pass    
     
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

        
