#import machine
import socket
import logging
import json

logging.basicConfig(filemode='DEBUG', format='[+] DEBUG ', level=logging.DEBUG)

IP_MASTER = '0.0.0.0'
PORT  = 1234
COMMAND = b''

def connection():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data = bytes
    sock.bind((IP_MASTER, PORT))
    sock.listen(0)
    conn, addr = sock.accept()
    with conn:
        try:
            data=''
            while True:
                try:
                    data= data + sock.recv(1024)
                    execute(json.loads(data))
                except ValueError:
                    continue
                    

        except KeyboardInterrupt as e:
            sock.close()
            exit()

def execute(command):
    print(command)