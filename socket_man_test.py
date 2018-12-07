import socket
import sys
import struct
import ip

TCP_IP = ip.IPADDR
#TCP_IP = '127.0.0.1'
TCP_PORT = 12346

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

def pullfromCLient(line):
    try:
        #while True:
            #line = sys.stdin.readline()
        if line:
            s.send(line.encode())
        else:
            return

    except KeyboardInterrupt:
        s.close()
        sys.exit()

def sendFormattedCommand(line):
    try:
        if line:
            s.send(struct.pack("i", len(line)) + line.encode())
        else:
            return
    except KeyboardInterrupt:
        s.close()
        sys.exit()