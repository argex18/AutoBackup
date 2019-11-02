from os import getcwd, listdir, path
from traceback import print_exc
from datetime import date
from time import strptime

import lib

SCOPES = "https://www.googleapis.com/auth/drive"
CREDENTIALS = input("Insert the name (or path\\name if it's in external dir) of the JSON file with your credentials: ")

def search():
    google = lib.GoogleDrive.from_token("token.pickle")
    result = google.search("AutoBackup")
    print(result)

if __name__ == "__main__":
    search()
else:
    print("This is a single script which cannot be imported")
    