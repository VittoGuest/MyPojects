import tkinter
import customtkinter as ctk
from tkinter import *
import tkinter.filedialog as filedialog
from gpx_converter import Converter
import csv
import simplekml
import pandas
import os


class Main():
    def __init__(self):

        ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
        ctk.set_default_color_theme("green")  # Themes: blue (default), dark-blue, green

        window = ctk.CTk()
        window.title("KML-GPX converter")
        window.geometry("600x490")
        window.maxsize(width=600, height=490)

        # Add image file
        file= input('Put the path:')
        bg = PhotoImage(file = file)

        l0= tkinter.Label(window, image=bg, borderwidth=0)
        l0.place(x=0, y=200)

        l1=ctk.CTkLabel(window, text="File  :", justify='left', width=70)
        l2=ctk.CTkLabel(window, text="Output :", justify='left', width=70)

        l1.grid(row=1, column=0, padx=10, pady=10)
        l2.grid(row=2, column=0, padx=10, pady=10)

        self.e1=ctk.CTkEntry(window,  width=350)
        self.e2=ctk.CTkEntry(window, width=350)

        self.e1.grid(row=1, column=1, padx=10, pady=10)
        self.e2.grid(row=2, column=1, padx=10, pady=10)

        b1= ctk.CTkButton(window,text="Apri", command=self.file, width=70, border_width=2,  border_color= 'darkgrey')
        b2= ctk.CTkButton(window,text="Apri", command=self.save, width=70, border_width=2,  border_color= 'darkgrey')
        b3= ctk.CTkButton(window,text="Waypoints Only",command=self.Waypoints, width=70, border_width=2,  border_color= 'green')
        b4= ctk.CTkButton(window,text="Get Tracks",command=self.Tracks, width=70, border_width=2,  border_color= 'green')

        b1.grid(row=1, column=2, padx=10, pady=10)
        b2.grid(row=2, column=2, padx=10, pady=10)
        b3.grid(row=3, column=1, padx=10, pady=10)
        b4.grid(row=3, column=1, padx=10, pady=10, sticky= 'e')

        if __name__=='__main__':
            window.mainloop()

    def file(self):

        self.path_in = filedialog.askopenfilename()        
        self.e1.delete(1, END)
        self.e1.insert(0, self.path_in)

    def save(self):

        self.path_out
        self.e2
        self.path_out= filedialog.askdirectory()
        self.e2.delete(1, END)
        self.e2.insert(0, self.path_out)

    def Tracks(self):

        with open(self.path_out+"/WAYPOINTS.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

        Converter(input_file=self.path_in).gpx_to_csv(output_file=self.path_out+"/WAYPOINTS.csv")
        
        data = pandas.read_csv(self.path_out+"/WAYPOINTS.csv")

        LAT = list(data["latitude"])
        LONG = list(data["longitude"])
        #ALT = list(data["altitude"])
        
        kml = simplekml.Kml()
        coord = []
        
        for lt,ln in zip(LAT,LONG):

            coords= (ln,lt)
            coord.append(coords)
            #point = kml.newpoint(coords= [(ln,lt)])

        ls = kml.newlinestring(name='Track')
        ls.coords = coord 
        ls.extrude = 1
        ls.altitudemode = simplekml.AltitudeMode.relativetoground
        ls.style.linestyle.width = 5
        ls.style.linestyle.color = simplekml.Color.blue                

        l3 = ctk.CTkLabel(self.window, text='export trks', width=70)
        l3.grid(row=4, column=1, sticky='e')
        os.startfile(self.path_out)

        kml.savekmz(self.path_out+"/TRACK.kml")

        self.e1.delete(0, END)
        self.e2.delete(0, END)

    def Waypoints(self):
        
        with open(self.path_out+"/WAYPOINTS.csv", 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

        Converter(input_file=self.path_in).gpx_to_csv(output_file=self.path_out+"/WAYPOINTS.csv")
        
        data = pandas.read_csv(self.path_out+"/WAYPOINTS.csv")


        LAT = list(data["latitude"])
        LONG = list(data["longitude"])
        ALT = list(data["altitude"])
        
        kml = simplekml.Kml()
        
        for lt,ln, alt in zip(LAT,LONG, ALT):

            point = kml.newpoint(coords= [(ln,lt,alt)])
            point.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
            point.style.labelstyle.color = simplekml.Color.red
                    
                    
        kml.savekmz(self.path_out+"/WAYPOINTS.kml")

        os.startfile(self.path_out)

        self.e1.delete(0, END)
        self.e2.delete(0, END)

Main()







