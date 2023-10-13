from internal_utils import divider, delline
import tqdm
import sys

class version_:
    def __init__(self):
        self.version = "0.1.0"
        self.date = "10-12-23"
        self.contrubutors = "KaneryU"
        
        self.write_version = "write_version: 0.1.0"
        self.write_date = "Started work on 10-12-23"
        self.write_contrubutors = "Contrubutors: KaneryU"
        
        self.history = [
            "0.0.1 10/11/23 Creation of the project",
            "0.0.2 10/12/23 Halfway done with dir command",
            "0.0.3 10/13/23 90% Done with dir, working on file search"
            "0.1.0 10/13/23 dir -sort shelved. Terminal is now techinically usefull, it can run any file"
        ]


version = version_()

args = sys.argv

if len(args) > 1:
    
    if args[1] == "-v" or args[1] == "--version" or args[1] == "-version" or args[1] == "--v":
        screen = divider.screen()
        print(divider.textCenter("pyTerm Version", screen.screenWidth, "-"))
        print(version.write_version)
        print(version.write_date)
        print(version.write_contrubutors)
        
        
    if args[1] == "-h" or args[1] == "--help" or args[1] == "-help" or args[1] == "--h":
        for i in tqdm(version.history, leave = False):
            print(i)
       
else:
    screen = divider.screen()
    print(divider.textCenter("pyTerm Version", screen.screenWidth, "-"))
    print(version.write_version)
    print(version.write_date)
    print(version.write_contrubutors)
    