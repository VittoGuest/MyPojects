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
    
    # Test sending a message
    try:
        while True:
            send_message("Hello, LoRa World!")
            time.sleep(5)  # Wait for 5 seconds before sending the next message
    except KeyboardInterrupt:
        print("Script stopped by user.")
        set_lora_mode('sleep')  # Set LoRa module to sleep mode before exiting

if __name__ == '__main__':
    main()
