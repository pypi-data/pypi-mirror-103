#code to be run on the server end

#!/usr/bin/env python

import socket
from datetime import datetime
now = datetime.now()

def Log(text, addr):
	fileName = str(addr)
	fileName = fileName + ".txt"
	with open(fileName, "a") as logFile: # "a" stays for append mode
		logFile.write(text)
		logFile.write("\n")
		logFile.close()

TCP_IP = ''
TCP_PORT = 5005
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

conn, addr = s.accept()
print('Connection address ', addr)
Log("Connection Opened: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"), addr)
print("received data:")
while 1:
    data = conn.recv(BUFFER_SIZE)
    if not data: break
    output = data.decode()
    print(output)
    Log(output, addr)
conn.close()
Log("Connection closed: " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"), addr)


