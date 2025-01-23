import serial
import time
import math

def read_rssi(serial_port):
    """
    Communicates with ASR6601 over serial to read RSSI after receiving a packet.

    Args:
        serial_port (str): The serial port connected to ASR6601 (e.g., "COM3" or "/dev/ttyUSB0").
    """
    try:
        # Open the serial connection
        ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
        time.sleep(2)  # Allow the connection to stabilize
        
        # Ensure the module is responsive
        ser.write(b'+++\r\n')
        response = ser.read_until(b'\r\n').decode('utf-8').strip()
        print(response)
        if "Entry AT" not in response:
            print("Module not responding to AT commands.")
            return

        print("Module is ready.")

        # Listen for incoming packets
        while True:
            # Check if there's data to read
            if ser.in_waiting > 0:
                incoming_data = ser.read_until(b'\r\n').decode('utf-8').strip()
                print("Received:", incoming_data)
                
                # Check if it's a LoRa packet (specific response will depend on your module)
                if "+RECV:" in incoming_data:
                    print("Packet received.")

                    # Query RSSI (if not included in the incoming data)
                    ser.write(b'AT+RSSI\r\n')
                    rssi_response = ser.read_until(b'\r\n').decode('utf-8').strip()
                    print("RSSI:", rssi_response)
                    
    except serial.SerialException as e:
        print(f"Serial error: {e}")
    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()

def readRssi(ser):
    try:       
        # Ensure the module is responsive
        ser.write(b'+++\r\n')
        response = ser.read_until(b'\r\n').decode('utf-8').strip()
        print(response)
        if "Entry AT" not in response:
            print("Module not responding to AT commands.")
            return

        print("Module is ready.")

        ser.write(b'AT+RSSI\r\n')
        rssi = ser.read_until(b'\r\n').decode('utf-8').strip()
        
        ser.write(b'+++\r\n')
        return rssi
    except:
        return 
    
def calculate_distance(rssi, tx_power, path_loss_exponent=2.0, system_loss=0):
    """
    Estimate the distance between two LoRa devices based on RSSI.

    Parameters:
        rssi (float): Received Signal Strength Indicator in dBm
        tx_power (float): Transmitter power in dBm
        path_loss_exponent (float): Path loss exponent (environment-specific)
        system_loss (float): Constant system loss (optional)

    Returns:
        float: Estimated distance in meters
    """
    # Compute distance using the log-distance path loss model
    distance = 10 ** ((tx_power - int(rssi) - system_loss) / (10 * path_loss_exponent))
    return distance

# Open the serial connection

serial_port = 'COM3'
tx_power = 22  # Transmitter power in dBm
path_loss_exponent = 2.7  # Typical urban area

ser = serial.Serial(serial_port, baudrate=9600, timeout=1)
time.sleep(2)  # Allow the connection to stabilize
print('[*] Listening...\n')

while True:
    receive = ser.read_until(b'\r\n').decode('utf-8').strip()
    if 'check' in receive:

        # Example usage
        rssi = readRssi(ser)  # RSSI in dBm (measured)
        rssi = rssi[-3]+rssi[-2]+rssi[-1]
        print(rssi)
        
        if rssi != None:
            estimated_distance = calculate_distance(rssi, tx_power, path_loss_exponent)
            print(f"Estimated Distance: {estimated_distance:.2f} meters")

        else:
            print('[-] Cannot read COM!')

