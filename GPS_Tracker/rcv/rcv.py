import serial
import CoT
import os
import time
import requests
from datetime import datetime
import json

''' RCV is designed to be used with a device that works with ATAK.
    It receives gps data from LoRa device and it sends a CoT to ATAK.
    At the moment it only works in local (127.0.0.1:8087).
    The aim is to send over Multicast (239.2.3.1:6969)'''

class RCV:
    
    
    def __init__(self):
        
        # ATAK Init

        self.ATAK_IP = os.getenv('ATAK_IP', '127.0.0.1')
        self.ATAK_PORT = int(os.getenv('ATAK_PORT', '8087'))
        self.ATAK_PROTO = os.getenv('ATAK_PROTO', 'UDP')

        self.params = {  # SWX parking lot
            "lat": 43.42079,
            "lon": 10.41774,
            "uid": "Tracker-01",
            "identity": "unknown",
            "dimension": "land-unit",
            "entity": "military",
            "type": "G-U-C"
        #    "type": "U-C-R-H"
        }
                
    def listen(self):
        
        # Serial Init

        serialPort = 'COM7'
        baudrate = 9600

        sr = serial.Serial(serialPort, baudrate)
        data=''
        try:
            while True:
                data = sr.read()
                self.send(data)
                time.sleep(1)
        except KeyboardInterrupt:
            exit()

    def send(self, data):
        
        # Takes data and set it to params xml
        lat = data['lat']
        long = data['long']
        
        self.params['lat']= float(lat)
        self.params['lon'] = float(long)
        
        # Pass values to CoT to get an xml 
        cot = CoT.CursorOnTarget()
        cot_xml = cot.atoms(self.params)
        
        # Send to ATAK 
        print ("\nPushing to ATAK...")
        if self.ATAK_PROTO == "TCP":
            sent = cot.pushTCP(self.ATAK_IP, self.ATAK_PORT, cot_xml.encode())
        else:
            sent = cot.pushUDP(self.ATAK_IP, self.ATAK_PORT, cot_xml.encode())
        print(str(sent) + " bytes sent to " + self.ATAK_IP + " on port " + str(self.ATAK_PORT))
        time.sleep(2)

        print(cot_xml)
    
    def public_to_server(self, data):
        
        # POST request to publish data to the server
        res = requests.post("http://ec2-13-61-2-224.eu-north-1.compute.amazonaws.com/main/main.php", data=data)
        
    def read_from_server(self):
        
        # GET request to take data 
        grab = requests.get('http://ec2-13-61-2-224.eu-north-1.compute.amazonaws.com/main/main.php')
        coord = json.loads(grab.text)
        
        # Display to ATAK 
        self.send(coord)


if __name__ == '__main__':
    start = RCV()
    
    now = datetime.now()
    # DATA coming from source !! IMPLEMENT LoRa one interface
    coord = dict(lat=43.98876, long=23.09786, date= now)

    start.read_from_server()
    
    # Send CoT to ATAK 
    #start.send(coord)
    
    
    
    
    






