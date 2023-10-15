#this is for debugging specific functions that are under development
def findvars(txt):
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
        
    vars = globals()
    errorMsg = "Variables "
    
    for i in temps:
        if not i in vars:
            if errorMsg[len(errorMsg) - 1 ] == "'" :
                errorMsg = errorMsg + ","
            errorMsg = errorMsg + "'"+ i + "'"
    errorMsg = errorMsg + " were not found."
    if not errorMsg == "Variables  were not found.": 
        return((errorMsg, None, True)) 
    
    index = 0
    for i in temps:
        temps[index] = str(vars.get(i))
        index += 1
        
    index = 0   
    while index <= string.count('%') + 1:
        string = string.replace('%', temps[index], 1) #replace occurences of variable expressions with the variable value
        index += 1
        
    return((string, temps, False))   
        
def parsecmd(cmd):
    cmd = findvars(cmd)
    if cmd[2] == True:
        return(cmd[0])
    cmd = cmd[0] #we don't need the other stuff
    temp = ""
    args = []
    vars = globals
    
    for i in cmd:
        temp += i
        if i == " ":
            args.append(temp[0:len(temp)-1])
            temp = ""
    args.append(temp)
    #print(args)
    return(args)
name = input("What is your name? ")
print(parsecmd("hello %name% how are you %name%"))
