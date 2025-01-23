import serial
from threading import Thread
import yaml



class Receiver(Thread):
    def __init__(self, serialPort): 
        Thread.__init__(self)
        self.serialPort = serialPort 

    def run(self):
        text = ""
        while True:
            
            text = serialPort.readline()
            text = text.decode()
            print (str(text))   

class Sender(Thread):
    def __init__(self, serialPort):
        Thread.__init__(self)
        self.serialPort = serialPort 

    def run(self):
        text = ""
        while True:
            text = input()
            text = f"[{config['host_name']}]: " + text+'\n'
            self.serialPort.write(text.encode())
             

with open("LoRa/chat_config.yaml","r") as file_object:
                config=yaml.load(file_object,Loader=yaml.SafeLoader)
                # dict = {'serial_port': '/dev/ttyUSB0', 'host_name': 'LoRa01'}
 

serialPort = serial.Serial(port=config['serial_port'], baudrate=9600)
entry_message = f"\n[{config['host_name']}] ONLINE!\n"
serialPort.write(entry_message.encode())

send = Sender(serialPort) 
receive = Receiver(serialPort) 
send.start() 
receive.start()

