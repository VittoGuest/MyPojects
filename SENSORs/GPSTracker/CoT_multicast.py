import socket
import time
import logging
import struct

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - [+] %(message)s')

def tcp_connection(address, cot):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(address)
        sock.sendall(cot)
        sock.close()

    except KeyboardInterrupt:
        print("Stopped.")
        

def listening_multicast():
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        ttl = struct.pack('b', 5)  # Increase TTL to 5
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', 6969))
        
        try:
            while True:
                
                data, addr = sock.recvfrom(1024)
                print(data.decode())
                time.sleep(2) 
        except KeyboardInterrupt:
            exit()
        
    except KeyboardInterrupt:
        print("Multicast stopped.")
    finally:
        sock.close()


def send_multicast_message(address, interface, data):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(interface))

    sock.sendto(data, address)
    sock.close()
    

def udp_multicast(network, address, cot):

    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        ttl = struct.pack('b', 5)  # Increase TTL to 5
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_IF, socket.inet_aton(network))
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.sendto(cot, address)
        print('[+] Sending CoT...')
        time.sleep(2) 
        
    except KeyboardInterrupt:
        print("Multicast stopped.")
    finally:
        sock.close()


def udp_broadcast(address, cot):

    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        sock.sendto(cot.encode(), address)
        print(f"CoT message broadcasted with {address}")
        time.sleep(2)  

    except KeyboardInterrupt:
        print("Broadcasting stopped.")
    finally:
        sock.close()


def test_recursively():

    # CoT event example
    cot_message = """<event version="2.0" uid="f94dba22-e841-4db9-bd6b-5a6915cdbb69" type="a-u-G" time="2025-01-11T18:14:36.24Z" start="2025-01-11T18:14:36.24Z" stale="2025-01-11T18:19:36.24Z" how="h-g-i-g-o" access="Undefined"><point lat="43.4129966" lon="10.4171612" hae="145.949" ce="9999999" le="9999999" /><detail><status readiness="true" /><archive /><color argb="-1" /><precisionlocation altsrc="DTED2" /><remarks /><archive /><link uid="ANDROID-2a73b0aff9afa7ae" production_time="2025-01-11T18:14:05.207Z" type="a-f-G-U-C" parent_callsign="COKINA" relation="p-p" /><usericon iconsetpath="COT_MAPPING_2525C/a-u/a-u-G" /><contact callsign="U.11.191405" /></detail></event>
"""
    # Addresses             
    unicast = { 'localhost':('192.168.196.80',4242), # OK
                'loopback':('127.0.0.1',4242), # OK
                'redmi':('192.168.196.28',4242), # OK
                'acer' :('192.168.196.229',4242)} # OK

    multicast = { 'multicast_6969':('239.2.3.1',6969), 
                'multicast_7070':('239.2.3.1',7070),
                'multicast_4242':('239.2.3.1',4242)}

    broadcast = {'broadcast_6969':('255.255.255.255',6969),  # OK su desk
    'broadcast_7070':('255.255.255.255',7070),'broadcast_4242':('255.255.255.255',4242)} #OK su desk tranne 4242

    try:
        while True:
            for i in unicast.items():
                logging.debug(f'Sending CoT to {i[0]}  {i[1]}')
                try:
                    tcp_connection(i[1], cot_message)
                except:
                    pass
                time.sleep(1)
            
            for i in multicast.items():
                logging.debug(f'Sending CoT to {i[0]}  {i[1]}')
                
                try:
                    udp_multicast(i[1], cot_message)
                except:
                    pass
                time.sleep(1)

            for i in broadcast.items():
                logging.debug(f'Sending CoT to {i[0]}  {i[1]}')
                try:
                    udp_multicast(i[1], cot_message)
                except:
                    pass
                time.sleep(1)

    except KeyboardInterrupt:
        exit()


cot = """<event version="2.0" uid="3f381ed1-bfff-4af8-b816-4c23a5ffcee4" type="a-u-G" time="2025-01-17T17:39:39.00Z" start="2025-01-17T17:40:58.08Z" stale="2025-01-24T17:40:58.08Z" how="h-g-i-g-o" access="Undefined"><point lat="43.41156696" lon="10.41654156" hae="123.42185313" ce="9999999" le="9999999" /><detail><link type="a-f-G-U-C-I" uid="S-1-5-21-2465958065-103384072-4164049192-1002" parent_callsign="HQ" relation="p-p" production_time="2025-01-17T17:39:34Z" /><archive /><usericon iconsetpath="COT_MAPPING_2525C/a-u/a-u-G" /><contact callsign="Tracker01" /><precisionlocation geopointsrc="???" altsrc="DTED0" /></detail></event>"""

eth= '192.168.1.50'
eth5= '192.168.56.1'
NordLynx= '10.5.0.2'
ZeroTier = '192.168.196.80'

multicast_group = ('239.2.3.1', 6969)  # Multicast address

#send_multicast_message(multicast_group, '192.168.192.80', cot.encode())
