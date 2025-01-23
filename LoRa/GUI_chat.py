import serial
from threading import Thread
import yaml
import customtkinter as ctk

class GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("800x700")
        self.title("LoRa - Chat")    
        
        # add widgets to app
        self.canvas = ctk.CTkCanvas(self, height= 600, width= 500)
        self.canvas.grid(row=0, column=0, padx=20, pady=10)

        self.input = ctk.CTkEntry(self, width=500)
        self.input.grid(row=1, column=0, padx=5, pady=10)

        self.button = ctk.CTkButton(self, text='Send', command=self.button_click)
        self.button.grid(row=1, column=1, padx=5, pady=10)

    # add methods to app
    def button_click(self):
        print("button click")

 


class Receiver(Thread):
    def __init__(self, serialPort): 
        Thread.__init__(self)
        self.serialPort = serialPort 

    def run(self):
        text = ""
        while True:
            
            text = serialPort.readline()
            text = text.decode()
            print (str(text))   

class Sender(Thread):
    def __init__(self, serialPort):
        Thread.__init__(self)
        self.serialPort = serialPort 

    def run(self):
        text = ""
        while True:
            text = input()
            text = f"[{config['host_name']}]: " + text+'\n'
            self.serialPort.write(text.encode())
            

with open("LoRa/chat_config.yaml","r") as file_object:
                config=yaml.load(file_object,Loader=yaml.SafeLoader)
                # dict = {'serial_port': '/dev/ttyUSB0', 'host_name': 'LoRa01'}
 

app = GUI()
app.mainloop()

serialPort = serial.Serial(port=config['serial_port'], baudrate=9600)
entry_message = f"\n[{config['host_name']}] ONLINE!\n"
serialPort.write(entry_message.encode())

send = Sender(serialPort) 
receive = Receiver(serialPort) 
send.start() 
receive.start()

