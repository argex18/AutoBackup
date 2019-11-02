# This is a script to automate your backups on Google Drive cloud service. Please, read these instructions carefully before using it !

# REQUISITES TO MAKE THE SCRIPT WORK:

    1) You need the Google Drive API installed among your Python          packages.
       Link to download it: https://github.com/googleapis/google-api-python-client.
       
       // You can simply open your terminal and digit:

            pip install virtualenv
            virtualenv <your-env>
            <your-env>\Scripts\activate
            <your-env>\Scripts\pip.exe install google-api-python-client

        //
    
    2) You need to have a Python version higher than 2.7 one
#   WARNING: THIS IS REALLY IMPORTANT !
    3) You need to have a json file with your user credentials to
       allow to the script to sign in your Google Drive account.

       If you don't know how to get one, i recommend you to read the official Google documentation for developers:
       https://developers.google.com/drive/api/v2/about-auth
#   WARNING: THE SCRIPT TO WORK REQUIRES A FULL READ-WRITE DATA SCOPE, THAT IS: https://www.googleapis.com/auth/drive
#   THIS SCOPE WAS PRE-INCLUDED IN THE SCRIPT CODE, SO IF YOU DON'T SET IT, THE SCRIPT WILL DO IT THE FIRST TIME YOU RUN IT.

# HOW TO USE THE SCRIPT:

    1) If you need to make your backup immediately, simply put into       the GoogleDrive folder all the files you want to upload.
       Then start the script by double-clicking on backup.py or
       digiting in your console: python backup.py.
       The script is going to upload to your Google Drive account all those files, then they are going to be copied in GoogleDrive\Done\Uploaded\the_current_date directory.
#      Once done this, the script will delete the files.
    
    2) Instead, if you need to set your backup for a certain date,
       you have to create a folder into GoogleDrive directory which has, as name, the date and then another sub-folder inside it which has, as name, the time in which you want to perform your backup.
#      Both these folders are mandatory 
#      THE SCRIPT WON'T WORK WITHOUT THEM !

#      The date folder name must be of the following format: dd.mm.yy
#      Any other format won't be accepted

#      The time folder name must be of the following format: hh.mm
#      Any other format won't be accepted
       Once you will correctly have set the script, you will simply have to launch it in the same way explained before.




