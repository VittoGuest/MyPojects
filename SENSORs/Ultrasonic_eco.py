import machine
import time

# Define GPIO pins
TRIG_PIN = 3
ECHO_PIN = 2
#BUZZER_PIN = 28

# Initialize pins
trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)

# Initialize PWM for the buzzer
#buzzer = machine.PWM(machine.Pin(BUZZER_PIN))
#buzzer.freq(1000)  # Set a default frequency (e.g., 1 kHz)

def get_distance():
    # Send a 10us pulse to trigger
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    
    # Wait for echo to go high and start timing
    while echo.value() == 0:
        start_time = time.ticks_us()
        
    # Wait for echo to go low and stop timing
    while echo.value() == 1:
        end_time = time.ticks_us()
    
    # Calculate distance in cm (speed of sound is ~343 m/s)
    duration = time.ticks_diff(end_time, start_time)
    distance = (duration * 0.0343) / 2  # Divide by 2 for round trip
    return distance

while True:
    dist = get_distance()
    print(f"Distance: {dist:.2f} cm")
    
    '''if dist < 50:  # Only sound the buzzer if within 50 cm
        # Calculate duty cycle based on distance (closer = louder)
        # Map distance (50 to 0 cm) to duty cycle (0% to 100%)
        duty = max(0, min(100, int((50 - dist) * 2)))  # Scale 50 cm to 0-100%
        buzzer.duty_u16(int(duty * 65535 / 100))  # Convert percentage to 16-bit value
    else:
        buzzer.duty_u16(0)  # Turn off the buzzer'''
    
    time.sleep(1)
