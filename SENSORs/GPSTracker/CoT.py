import datetime
import socket
import xml.etree.ElementTree as ET
import serial 
import time
import re
import argparse
import os
from CoT_multicast import *
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class GPS_Tracker():
    def __init__(self, tak_ip, tak_port, serial_port, baudrate, source_ip):
        
        self.banner = """
               _________       _____________      ________                   ______  
                ___  __ \\_____ ______  /__(_)________  __/____________ _________  /__
                __  /_/ /  __ `/  __  /__  /_  __ \\_  /  __  ___/  __ `/  ___/_  //_/
                _  _, _// /_/ // /_/ / _  / / /_/ /  /   _  /   / /_/ // /__ _  ,<   
                /_/ |_| \\__,_/ \\__,_/  /_/  \\____//_/    /_/    \\__,_/ \\___/ /_/|_|  
            
                    Make sure you open WinTAK and you have the radio connected  """                                                                       
        print(self.banner)
        
        # CoT base schema
        cot = """<event version="2.0" uid="3f381ed1-bfff-4af8-b816-4c23a5ffcee4" type="a-u-G" time="2025-01-17T17:39:39.00Z" start="2025-01-17T17:40:58.08Z" stale="2025-01-24T17:40:58.08Z" how="h-g-i-g-o" access="Undefined"><point lat="43.41156696" lon="10.41654156" hae="123.42185313" ce="9999999" le="9999999" /><detail><link type="a-f-G-U-C-I" uid="S-1-5-21-2465958065-103384072-4164049192-1002" parent_callsign="HQ" relation="p-p" production_time="2025-01-17T17:39:34Z" /><archive /><usericon iconsetpath="COT_MAPPING_2525C/a-u/a-u-G" /><contact callsign="Tracker01" /><precisionlocation geopointsrc="???" altsrc="DTED0" /></detail></event>"""
        
        # Network objects
        self.tak_ip = tak_ip
        self.tak_port = tak_port
        self.source_ip = str(source_ip)
        
        # Connect to serial 
        self.ser = self.connect_serial(serial_port, baudrate)

        logging.debug('Serial initialized')

        # Main function
        self.status = '[+] CoT sent: '
        self.main(cot)
   
    
    def connect_serial(self, serial_port, baudrate):
        
        i=0
        while i != 10:
            try:
                ser = serial.Serial(port=serial_port, baudrate=baudrate)
                print(f"[+] Connected to serial port {serial_port}")
                return ser
            except serial.SerialException as e:
                print(f"[!] Serial connection error: {e}")
                time.sleep(1)
                i=i+1
    
    def convert_to_degrees(self,deg, minutes):

        # Convert degrees and minutes to degrees
        value = float(deg) + float(minutes) / 60
        return round(value, 7)

    def update_cot(self, cot, latitude_deg, longitude_deg):
        now = datetime.datetime.now(datetime.timezone.utc)
        stale = now + datetime.timedelta(minutes=2)
        logging.debug(f'Modifying CoT: {now} - {stale}')
        # Update XML
        root = ET.fromstring(cot)
        root.attrib.update({
            "time": now.isoformat(),
            "stale": stale.isoformat()
        })
        point = root.find('point')
        if point is not None:
            point.attrib.update({
                "lat": str(latitude_deg),
                "lon": str(longitude_deg)
            })
        logging.debug(f'Set LAT-LONG to xml')

        # Send XML
        xml_str = ET.tostring(root, encoding='unicode')
        logging.debug(f'Return a xml_str: {xml_str}')
        try:
            return xml_str.encode('utf-8')
        except Exception as e:
            print(f'[!] Exception occurred: {e}')
            return cot

    def clear_screen(self):
        os.system('cls')
        self.status = self.status+'*'
        print(self.banner)
        print(self.status)


    def main(self,cot):
        
        try:
            logging.debug('Starting main fun')
            while True:
                raw = self.ser.readline()
                raw = raw.decode()               
                if raw:
                    logging.debug(f'Raw data: {raw}')
                    matches = re.findall(r"(\d+)° ([\d.]+)'", raw)
                    if matches and len(matches) >= 2:
                        latitude_deg = self.convert_to_degrees(matches[0][0], matches[0][1])
                        longitude_deg = self.convert_to_degrees(matches[1][0], matches[1][1])
                        
                        logging.debug(f'LAT LONG values: {latitude_deg} - {longitude_deg}')
                        # Update CoT lat-long
                        event = self.update_cot(cot,latitude_deg, longitude_deg)
                        logging.debug(f'Modified CoT: {event}')
                        
                        # Send CoT through udp-multicast and tcp-loopback
                        logging.debug(f'Sending with following parameters: {self.tak_ip}-{self.tak_port}-{self.source_ip} + event')
                        send_multicast_message((self.tak_ip,self.tak_port), self.source_ip, event)
                        time.sleep(0.2)
                        tcp_connection((self.source_ip,4242),event)
                        
                        # Clear screen
                        self.clear_screen()
                        # NB the CoT is shown on ATAK only when the connection closes

        except KeyboardInterrupt:
            print("[*] Exiting program...")
        except Exception as e:
            print(f"[!] Error occurred: {e}")
        finally:
            self.ser.close()


if __name__ == '__main__':

    hostname= socket.gethostname()
    
    parser = argparse.ArgumentParser(description="GPS Tracker for TAK")
    parser.add_argument('--tak_ip', default='239.2.3.1', help='TAK server IP')
    parser.add_argument('--tak_port', type=int, default=6969, help='TAK server port')
    parser.add_argument('--serial_port', default='COM4', help='Serial port for GPS')
    parser.add_argument('--baudrate', type=int, default=9600, help='Baudrate for serial communication')
    parser.add_argument('--source_ip', type=str, default=socket.gethostbyname(hostname), help='Local IP. It is needed to select the working interface [NB if you are wonking on a VPN, insert the local VPN IP ]')
    args = parser.parse_args()

    start = GPS_Tracker(args.tak_ip, args.tak_port, args.serial_port, args.baudrate, args.source_ip)
    
    # Exiting...
    print('[*] Exiting...')
    exit()

    








