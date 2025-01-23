import serial
from threading import Thread
import yaml
from playsound import playsound
from time import sleep


class Receiver(Thread):
    def __init__(self, serialPort): 
        Thread.__init__(self)
        self.serialPort = serialPort 

    def run(self):
        text = ""
        while True:
            text = serialPort.readline()
            text = text.decode()
            if 'True' in text:
                for i in range(0,3):
                    playsound('LoRa/alert_intrusion.mp3')
                    sleep(0.3)
                    i+=1
                self.response()
                
            print (str(text))

    def response(self):
        choice=input('[*] Put 1 to play streaming or 0 to skip: ')
        if choice == 1:
            start_streamig = 'start' # Command to start the streaming
            serialPort.write(start_streamig.encode())
            
with open("LoRa/chat_config.yaml","r") as file_object:
                config=yaml.load(file_object,Loader=yaml.SafeLoader)
                # dict = {'serial_port': '/dev/ttyUSB0', 'host_name': 'LoRa01'}
 

try:
    serialPort = serial.Serial(port=config['serial_port'], baudrate=9600)
except serial.SerialException:
    print('[-] Check LoRa connection!\n')
    exit()

print('\n[ONLINE] Monitoring...\n')
message = f"[{config['host_name']}] ONLINE\n\n"

receive = Receiver(serialPort) 
receive.start()
