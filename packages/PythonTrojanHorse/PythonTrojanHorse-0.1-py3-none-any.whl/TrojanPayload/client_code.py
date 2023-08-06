#!/usr/bin/env python

import socket

class Port:
    def __init__(self, data):
        #TCP_IP = '127.0.0.1' # <-- IP of the Server on Elvis
        #TCP_IP = '192.168.0.11' # <-- IP of the Server on Windows different comp
        TCP_IP = '192.168.0.5' # <-- IP of the Server on Windows same comp
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        #MESSAGE = 'Hello, World from Group A-2!'

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((TCP_IP, TCP_PORT))
        self.transmit_data(data)
        #s.send(MESSAGE)
    def __del__(self):
        self.s.close()

    def transmit_data(self, data):
        self.s.send(data.encode())
