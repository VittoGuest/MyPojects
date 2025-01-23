from machine import UART, Pin
import time
from micropyGPS import MicropyGPS
import ujson

# Initialize UART for LoRa and GPS
# UART1: Tx=Pin(8), Rx=Pin(9)
lora_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))
gps_serial = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9))

# Init of MicropyGPS
my_gps = MicropyGPS()

# GPIO for LoRa M0 and M1 (to set working mode)
M0 = Pin(10, Pin.OUT)
M1 = Pin(11, Pin.OUT)

def set_lora_mode(mode='normal'):
    """
    Set LoRa working mode
    :param mode: 'normal', 'wake_up', 'power_saving', 'sleep'
    """
    if mode == 'normal':
        M0.value(0)
        M1.value(0)
    elif mode == 'wake_up':
        M0.value(1)
        M1.value(0)
    elif mode == 'power_saving':
        M0.value(0)
        M1.value(1)
    elif mode == 'sleep':
        M0.value(1)
        M1.value(1)
    else:
        raise ValueError("Invalid mode selected!")
    time.sleep(0.1)  # Allow mode to stabilize

def send_message(message):
    """
    Send a message using the LoRa module
    :param message: Message to send (string)
    """
    if not isinstance(message, str):
        raise TypeError("Message must be a string!")
    
    set_lora_mode('normal')  # Set mode to normal for transmission
    lora_uart.write(message + '\n')  # Send message with newline character
    print(f"Message sent: {message}")

def main():
    # Set LoRa to normal mode to ensure proper initialization
    set_lora_mode('normal')
    
    while True:
        # Test sending a message
        try:
            while gps_serial.any():
                data = gps_serial.read()
                for byte in data:
                    stat = my_gps.update(chr(byte))
                    if stat is not None:
                        
                        utc_timestamp = my_gps.timestamp
                        date = my_gps.date_string('long')
                        lat = my_gps.latitude_string()
                        long = my_gps.longitude_string()
                        alt = my_gps.altitude
                        satellites = my_gps.satellites_in_use
                        prec = my_gps.hdop
                        
                        
                        # Prepare JSON data
                        
                        data = {
                            'date': date,
                            'lat': lat,
                            'long': long,
                            'alt': alt
                        }
                        
                        # Convert JSON
                        json_data = ujson.dumps(data)
                        
                        # Send data
                        send_message(json_data) 
                        time.sleep(10)

        except KeyboardInterrupt:
            print("Script stopped by user.")
            set_lora_mode('sleep')  # Set LoRa module to sleep mode before exiting

if __name__ == '__main__':
    main()
