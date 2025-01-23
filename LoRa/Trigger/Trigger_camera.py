import cv2
from datetime import datetime
from threading import Thread
import serial
import yaml
from playsound import playsound
import subprocess


# DEFINE THE STREAMING COMMAND!
# Usage of trigger with LoRa
class VideoCapture(Thread):
    
    def __init__(self, yaml_config): 
        Thread.__init__(self)
        self.yaml_config = yaml_config

    def run(self):
        # Definition of control variables
        status = int 
        self.check = int

        # Start video capture  
        video = cv2.VideoCapture(0) 

        present = datetime.now()
        format_present = str(present.strftime('%d_%b_%Y_%H%M%S'))

        # Video parameters
        width = 640
        height = 480
        fps = 30

        video.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        video.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        video.set(cv2.CAP_PROP_FPS, fps)

        fourcc = cv2.VideoWriter_fourcc(*'MPEG')
        output = cv2.VideoWriter(f"{format_present}.avi", fourcc, fps, (width,height))       

        # Cascade classifier
        #face_cascade= cv2.CascadeClassifier("OpenCV/haarcascade_frontalface_default.xml")
        face_cascade= cv2.CascadeClassifier("OpenCV/haarcascade_frontalface_default.xml")
        
        while True:
            
            # Start the video flow
            ret, frame= video.read() 
            
            # Condition to trigger only once 
            if status == 0:
                self.check = 0
            
            status = 0
            
            if not ret:
                print('\n[-] Not Ret!')
                break

            gray= cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray,
            scaleFactor = 1.25,
            minNeighbors = 3)
            
            # Square the recognized figures
            #for x, y, w, h in faces:
            #    boundary = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 1)

            current_time_now=datetime.now()
            current_time= str(current_time_now.strftime('%d-%b-%Y   %H:%M:%S'))
            date_text= cv2.putText(frame, current_time, (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1, cv2.LINE_8)

            try:
                if faces.all()!= None:
                    status=1

            except AttributeError:
                pass
            
            # Save video 
            if status==1:
                output.write(frame)

            # If not used before it trigs the server through lora connection
            if status == 1 and self.check == 0:
                try:
                    self.send()
                except:
                    self.lora_error()
            
            # Show the preview
            #cv2.imshow("Video", frame)

            # Command to quit ('q')
            key = cv2.waitKey(1)
            if key==ord('q'):
                break
        
        # Play the video
        video.release()
        if output.isOpened():
            output.release()

    def send(self):

        playsound('LoRa/alert_intrusion.mp3') 
        serialPort = serial.Serial(port=self.yaml_config['serial_port'], baudrate=9600)
        message = "True\n"
        serialPort.write(message.encode())
        self.check = 1

    def lora_error(self):
        print('[-] Problem with LoRa Device\n')
        self.check=1


class Receiver(Thread):
    def __init__(self, serialPort): 
        Thread.__init__(self)
        self.serialPort = serialPort 

    def run(self):
        command = 'mediamtx.sh'
        text = ""
        while True:
            text = serialPort.readline()
            text = text.decode()
            if '1' in text:
                subprocess.Popen([command], shell=True)
                serialPort.write('rtp://<ip-address>:port/mystream')
                

with open("LoRa/chat_config.yaml","r") as file_object:
                config=yaml.load(file_object,Loader=yaml.SafeLoader)
                # dict = {'serial_port': '/dev/ttyUSB0', 'host_name': 'LoRa01'}
 

serialPort = serial.Serial(port=config['serial_port'], baudrate=9600)
message = f"[{config['host_name']}] ONLINE\n\n"

video = VideoCapture(yaml_config=config)
receive = Receiver(serialPort) 
video.start()
receive.start()
