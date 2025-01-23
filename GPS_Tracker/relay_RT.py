from machine import UART, Pin
import time

# Initialize UART for LoRa
# UART1: Tx=Pin(8), Rx=Pin(9)
lora_uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))

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

def listen_for_data():
    """
    Listen for incoming data on the LoRa module.
    """
    set_lora_mode('normal')  # Ensure module is in normal mode
    print("Listening for incoming data...")
    
    try:
        while True:
            if lora_uart.any():  # Check if there's data available
                incoming_data = lora_uart.read()  # Read the data
                if incoming_data:
                    print(f"Received: {incoming_data.decode('utf-8').strip()}")
                    time.sleep(0.1)
                    lora_uart.write(incoming_data)
                    print('Relaying...')
            time.sleep(0.1)  # Slight delay to reduce CPU usage
            
    except KeyboardInterrupt:
        print("Listening stopped by user.")
        set_lora_mode('sleep')  # Set module to sleep mode before exiting

def main():
    # Ensure the LoRa module is ready
    set_lora_mode('normal')
    
    # Start listening for data
    listen_for_data()

if __name__ == '__main__':
    main()

