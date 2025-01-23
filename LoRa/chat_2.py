import serial
import yaml
from time import sleep


with open("LoRa/chat_config.yaml","r") as file_object:
                config=yaml.load(file_object,Loader=yaml.SafeLoader)
                # dict = {'serial_port': '/dev/ttyUSB0', 'host_name': 'LoRa01'}
 

serialPort = serial.Serial(port=config['serial_port'], baudrate=9600)
entry_message = f"\n[{config['host_name']}] ONLINE!\n"

while KeyboardInterrupt:
    serialPort.write(entry_message.encode())
    sleep(2)
exit()
