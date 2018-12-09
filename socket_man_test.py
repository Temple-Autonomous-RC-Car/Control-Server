import socket
import sys

#TCP_IP = '10.42.0.217'
TCP_IP = '127.0.0.1'
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
