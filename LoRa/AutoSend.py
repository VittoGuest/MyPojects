import serial
import time

def rssi():
    ser.write(b'+++\r\n')
    response = ser.read_until(b'\r\n').decode('utf-8').strip()
    print(response)
    if "Entry AT" not in response:
        print('[-] Cannot connect to AT mode')
        ser.write(b'+++\r\n')
        time.sleep(1)
    else:
        print("Module is ready.")
        ser.write(b'AT+RSSI\r\n')
        rssi = ser.read_until(b'\r\n').decode('utf-8').strip()
        rssi = rssi[-3]+rssi[-2]+rssi[-1]+'\r\n'
        ser.write(b'+++\r\n')
    return rssi

def AT_mode(ser, timeout):
    ser.write(b'+++\r\n')
    response = ser.read_until(b'\r\n').decode('utf-8').strip()
    print(response)
    time.sleep(timeout)

ser = serial.Serial('COM3', baudrate=9600, timeout=1)
while KeyboardInterrupt:

    AT_mode(ser, 3)

    #if "Entry AT" not in response:
        #print('[-] STBY')
        #time.sleep(1)
    #else:
    ser.write(b'AT+RSSI\r\n')
    time.sleep(1)
    rssi = ser.read_until(b'\r\n').decode('utf-8').strip()
    rssi = rssi[-3]+rssi[-2]+rssi[-1]+'\r\n'
    time.sleep(1)
    AT_mode(ser, 3)
    
    ser.write(rssi.encode('utf-8'))
    time.sleep(3)
    
    
    

