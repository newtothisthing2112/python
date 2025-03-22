These are the python3 codes for a reverse backdoor (note:- do remember to CHANGE the IP and PORT in the code)
Features (for now):
1. move through directories
2. run cmd commands
3. download files
4. upload files
5. take webcam shots
6. take screenshots
7. record microphone

Note:- this backdoor is tested on the latest updated version of Windows 11 (22 March 2025) on a LOCAL network and bypasses the defender when converted into an exe file using pyinstaller (commands to include while converting --onefile --noconsole).
        Also, the commented-out part in the backdoor code is for persistence. You can enable it by removing the hashtags.


Example uses of all commands:

1. cd (displays the current directory), cd fullpathtochange
2. cmd commands like dir, more, etc
3. download filename.extension
4. upload filename.extension
5. (Note: The file will be downloaded in the listener file's directory, and the uploaded file should also be present in the same directory as the listener.)
6. 'webcam' to take Webshots
7. 'screenshot' to take screenshots
8. 'record time(in seconds)' to record the mic (the recording will be saved in .wav file extension)
