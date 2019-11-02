from os import getcwd, listdir, system
import os.path as path
from traceback import print_exc
from datetime import date
from time import strptime, sleep

import pickle

import lib
from __wait import wait

SCOPES = "https://www.googleapis.com/auth/drive"
CREDENTIALS = input("Insert the name (or path\\name if it's in external dir) of the JSON file with your credentials: ")

def backup():
    google = None
    today = date.today().strftime("%d.%m.%y")
    flag = False
    try:
        for day in listdir(getcwd() + "\\GoogleDrive"):
            if day == "Done":
                continue

            if path.isdir(getcwd() + "\\GoogleDrive\\" + day):
                for fdate in day.split("."):
                    if len(fdate) > 2:
                        raise NameError(
                            "Error in: " + day +
                            " format for: " + fdate)
                        break

                #print(date.today().strftime("%d.%m.%y"))
                if strptime(today, "%d.%m.%y") == strptime(day, "%d.%m.%y"):

                    if path.exists("token.pickle"):
                        google = lib.GoogleDrive.from_token("token.pickle")
                    else:
                        google = lib.GoogleDrive(SCOPES, CREDENTIALS)
                    
                    for upload in listdir(getcwd() + "\\GoogleDrive\\" + day):
                        google.upload(
                            fpath=getcwd() + "\\GoogleDrive\\" + day + "\\" + upload,
                            title=upload.split(".")[0],
                            folder="AutoBackup")

                elif strptime(today, "%d.%m.%y") > strptime(day, "%d.%m.%y"):
                    print("Past date detected: " + day)
                    print("Copying it to Done...\n")

                    system("xcopy /e GoogleDrive\\" + day + " GoogleDrive\\Done\\Uploaded")
                    print("Deleting it...\n")
                    system("rd GoogleDrive\\" + day)
                else:
                    for time in listdir(getcwd() + "\\GoogleDrive\\" + day):
                        ftime = time.replace(".", ":")

                        #if day.startswith("0"):
                        #    day = day.replace("0", "", 1)
                        
                        #if ftime.startswith("0"):
                        #    ftime = ftime.replace("0", "", 1)

                        until = wait(day, ftime)
                        #If it's within one day
                        if until.days == 0:
                            sleep(until.seconds)
                            #Once it has slept
                            if path.exists("token.pickle"):
                                google = lib.GoogleDrive.from_token("token.pickle")
                            else:
                                google = lib.GoogleDrive(SCOPES, CREDENTIALS)

                            for element in listdir(getcwd() + "\\GoogleDrive\\" + day + "\\" + time):
                                google.upload(
                                    fpath=getcwd() + "\\GoogleDrive\\" + day + "\\" + time + "\\" + element,
                                    title=element,
                                    folder="AutoBackup")
                                system("xcopy GoogleDrive\\" + day + " GoogleDrive\\Done\\Uploaded")
                                print("Deleting it...\n")
                                system("rd GoogleDrive\\" + day)
                        #Otherwise if it's over
                        else:
                            continue
            else:
                element = day
                today = date.today().strftime("%d.%m.%y")
                if not flag:
                    system("mkdir GoogleDrive\\Done\\Uploaded\\{}".format(
                        today
                    ))
                    flag = True
                
                if path.exists("token.pickle"):
                    google = lib.GoogleDrive.from_token("token.pickle")
                else:
                    google = lib.GoogleDrive(SCOPES, CREDENTIALS)

                google.upload(
                    fpath=getcwd() + "\\GoogleDrive\\" + element,
                    title=element,
                    folder="AutoBackup")
                system('xcopy GoogleDrive\\"{}" GoogleDrive\\Done\\Uploaded\\"{}"'.format(element, today))
                print("Deleting it...\n")
                system('del /f GoogleDrive\\"{}"'.format(element))
    except NameError:
        print_exc()
        print("THE DATE MUST BE OF THE FOLLOWING FORMAT: DD.MM.YY. FOR EXAMPLE: 01.11.19")
    except ValueError:
        print_exc()
        print("THE PLANNED DATE CANNOT PASS THE CURRENT DATE")
    except:
        print_exc()

if __name__ == "__main__":
    backup()
else:
    print("This is a single script which cannot be imported")





    