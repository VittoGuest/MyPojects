import serial
import time
import keyboard

ser = serial.Serial('COM5', 115200, timeout=1)  # adjust port
time.sleep(2)

print("WASD=Motors (stop on release), Arrows=Servos (incremental), Q=quit")

while True:
    try:
        # Motors
        if keyboard.is_pressed("w"):
            ser.write(b"w\n")
        elif keyboard.is_pressed("s"):
            ser.write(b"s\n")
        elif keyboard.is_pressed("a"):
            ser.write(b"a\n")
        elif keyboard.is_pressed("d"):
            ser.write(b"d\n")
        else:
            ser.write(b"x\n")  # stop motors if no key pressed

        # Servos (incremental)
        if keyboard.is_pressed("up"):
            ser.write(b"up\n")
            time.sleep(0.1)
        elif keyboard.is_pressed("down"):
            ser.write(b"down\n")
            time.sleep(0.1)
        elif keyboard.is_pressed("left"):
            ser.write(b"left_servo\n")
            time.sleep(0.1)
        elif keyboard.is_pressed("right"):
            ser.write(b"right_servo\n")
            time.sleep(0.1)

        # Quit
        if keyboard.is_pressed("q"):
            break

        time.sleep(0.05)

    except KeyboardInterrupt:
        break

ser.write(b"x\n")  # stop motors
ser.close()
