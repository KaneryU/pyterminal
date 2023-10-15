import requests
import sys

args = sys.argv

if len(args) > 1:
    url = args[1]
    r = requests.get(url)
    pass