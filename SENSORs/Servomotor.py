from machine import Pin, PWM
from time import sleep

# Configure the servo pin (e.g., GPIO 15 for ESP32)
servo_pin = PWM(Pin(26))
servo_pin.freq(50)  # Servo motors typically use a 50Hz PWM frequency

# Function to set the angle
def set_servo_angle(pin, angle):
    """
    Moves the servo to a specified angle.
    Args:
    - pin: The PWM pin connected to the servo.
    - angle: The angle to set the servo to (0 to 180 degrees).
    """
    # Map angle (0-180) to duty cycle (1000-9000)
    duty = int(1000 + (angle / 180.0) * 8000)
    pin.duty_u16(duty)  # Use `duty_u16` for finer resolution
    sleep(0.5)  # Small delay for servo to move

# Test the servo
try:
    position = 90
    while True: 
        user = input()
        if user == '+':
            position = position + 10
            set_servo_angle(servo_pin, int(position))   # Move to 0 degrees
            
        elif user == '-':
            print(str(position)+ '-')
            position = position - 10
            print(position)
        else:
            print('[-]')
        set_servo_angle(servo_pin, int(position))   # Move to 0 degrees
        sleep(1)
        
except KeyboardInterrupt:
    servo_pin.deinit()  # Turn off PWM when done
    print("Servo control stopped")
