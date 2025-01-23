from PIL import Image
import gpx_converter
import subprocess
import time
import pandas
import simplekml, pdf2image, img2pdf

                                                                                             

class Converter:
    def __init__(self):
        self.banner=r'''                                                                                                      
        ___  ___      _ _   _ _____                           _             
        |  \/  |     | | | (_)  __ \                         | |            
        | .  . |_   _| | |_ _| /  \/ ___  _ ____   _____ _ __| |_ ___ _ __  
        | |\/| | | | | | __| | |    / _ \| '_ \ \ / / _ \ '__| __/ _ \ '__| 
        | |  | | |_| | | |_| | \__/\ (_) | | | \ V /  __/ |  | ||  __/ |    
        \_|  |_/\__,_|_|\__|_|\____/\___/|_| |_|\_/ \___|_|   \__\___|_|                                                                                                                                                                                                                                                                                                                                             
        
        
        Select between the following numbers for conversions, [CTRL+C] to exit...\n\n
        '''          
        try:
            while True:    
                # First Menu
                print(self.banner)
                selection = input('1) IMAGEs\n2) GEOREF\n3) DOCUMENTs\n\n>> ')
                if selection=='1':
                    
                    # IMAGEs
                    self.clear_monitor()
                    selection = input('\n1) JPG <-> PNG\n2) PNG -> ICO\n\n>> ')
                    if selection=='1':
                        self.clear_monitor()
                        selection= input('\n1) JPG -> PNG\n2) PNG -> JPG\n\n>> ')
                        if selection=='1':
                            self.clear_monitor()
                            self.jpg_to_png()
                        elif selection=='2':
                            self.clear_monitor()
                            self.png_to_jpg()
                    elif selection== '2':
                        self.clear_monitor()
                        self.png_to_ico()
                    elif selection=='back':
                        self.clear_monitor()
                    else:
                        print('\n[-] Wrong char!\n\n')
                        time.sleep(2)
                        self.clear_monitor()
                
                elif selection=='2':
                    
                    # GEOREFs
                    self.clear_monitor()
                    selection= input('\n1) GPX <-> KML\n2) GPX <-> JSON\n3) GPX <-> CSV\n\n>> ')
                    if selection=='1':
                        self.clear_monitor()
                        selection= input('\n1) GPX -> KML\n2) KML -> GPX\n\n>> ')
                        if selection=='1':
                            self.clear_monitor()
                            self.gpx_to_kml()
                        elif selection=='2':
                            self.clear_monitor()
                            self.kml_to_gpx()
                        elif selection=='back':
                            self.clear_monitor()
                        else:
                            print('\n[-] Wrong char!\n\n')
                            time.sleep(2)
                            self.clear_monitor()
                    elif selection== '2':
                        self.clear_monitor()
                        selection= input('\n1) GPX -> JSON\n2) JSON -> GPX\n\n>> ')
                        if selection=='1':
                            self.clear_monitor()
                            self.gpx_to_json()
                        elif selection=='2':
                            self.clear_monitor()
                            self.json_to_gpx()
                        elif selection=='back':
                            self.clear_monitor()
                        else:
                            print('\n[-] Wrong char!\n\n')
                            time.sleep(2)
                            self.clear_monitor()

                    elif selection== '3':
                        self.clear_monitor()
                        selection= input('\n1) GPX -> CSV\n2) CSV -> GPX\n\n>> ')
                        if selection=='1':
                            self.clear_monitor()
                            self.gpx_to_csv()
                        elif selection=='2':
                            self.clear_monitor()
                            self.csv_to_gpx()
                        elif selection=='back':
                            self.clear_monitor()
                        else:
                            print('\n[-] Wrong char!\n\n')
                            time.sleep(2)
                            self.clear_monitor()

                elif selection=='3':
                    
                    # DOCUMENTs
                    self.clear_monitor()
                    selection= input('\n1) PDF <-> JPG\n2) CSV <-> XLS\n\n>> ')
                    if selection== '1':
                        self.clear_monitor()
                        selection= input('\n1) PDF -> JPG\n2) JPG -> PDF\n\n>> ')
                        if selection== '1':
                            self.clear_monitor()
                            print('[!] Still working on it!!')
                            time.sleep(2)
                            self.clear_monitor()
                        if selection== '2':
                            self.clear_monitor()
                            self.jpg_to_pdf()
                        elif selection=='back':
                            self.clear_monitor()
                        else:
                            print('\n[-] Wrong char!\n\n')
                            time.sleep(2)
                            self.clear_monitor()

                    elif selection== '2':
                        self.clear_monitor()
                        selection= input('\n1) CSV -> XLS\n2) XLS -> CSV\n\n>> ')
                        if selection== '1':
                            self.clear_monitor()
                            self.csv_to_xls()
                        if selection== '2':
                            self.clear_monitor()
                            self.xls_to_csv()
                        elif selection=='back':
                            self.clear_monitor()
                        else:
                            print('\n[-] Wrong char!\n\n')
                            time.sleep(2)
                            self.clear_monitor()
                elif selection=='back':
                    self.clear_monitor()
                
                else:
                    print('\n[-] Wrong char!\n\n')
                    time.sleep(2)
                    self.clear_monitor()
        except KeyboardInterrupt:
            print('\n\n@ Thank you! See ya...')
            time.sleep(2)
            exit()

    # IMAGEs
    def jpg_to_png(self):
        while True:
            file=input('\n[+] Full-path to the file (filename must end with .jpg) >> ')
            try:
                logo = Image.open(file)
                break
            except Exception:
                print('\n[-] Wrong path! Retry...\n')
                

        output= input('\n[+] Output path (filename must end with .png)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            logo.save(output,format='PNG')
            print('\n[+] Done!\n\n')
            self.stop()

        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.jpg_to_png()

    def png_to_jpg(self):
        while True:
            file=input('\n[+] Full-path to the file (filename must end with .png) >> ')
            try:
                logo = Image.open(file)
                logo= logo.convert('RGB')
                break
            except Exception:
                print('\n[-] Wrong path! Retry...\n')
                
        output= input('\n[+] Output path (filename must end with .jpg)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            logo.save(output, format='JPEG')
            print('\n[+] Done!\n\n')
            self.stop()

        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.png_to_jpg()

    def png_to_ico(self): 
        while True:
            file=input('\n[+] Full-path to the file (filename must end with .png) >> ')
            try:
                logo = Image.open(file)
                break
            except Exception:
                print('\n[-] Wrong path! Retry...\n')
                

        output= input('\n[+] Output path (filename must end with .ico)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            logo.save(output,format='ICO')
            print('\n[+] Done!\n\n')
            self.stop()

        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.png_to_ico()

    # GEOREF
    def gpx_to_kml(self):
            file=input('\n[+] Full-path to the file (filename must end with .gpx) >> ')
            output= input('\n[+] Output path (filename must end with .kml)>> ')
        #try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            gpx_converter.Converter(input_file=file).gpx_to_csv(output_file='data.csv')
            data= pandas.read_csv('data.csv')
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
                kml.savekmz(output)

            print('\n[+] Done!\n\n')
            self.stop()
        
        #except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.gpx_to_kml()
    
    def kml_to_gpx(self):
        pass
    
    def gpx_to_json(self):
        file=input('\n[+] Full-path to the file (filename must end with .gpx) >> ')
        output= input('\n[+] Output path (filename must end with .json)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            gpx_converter.Converter(input_file=file).gpx_to_json(output_file=output)
            print('\n[+] Done!\n\n')
            self.stop()
        
        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.gpx_to_json()

    def json_to_gpx(self):
        file=input('\n[+] Full-path to the file (filename must end with .json) >> ')
        output= input('\n[+] Output path (filename must end with .gpx)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            gpx_converter.Converter(input_file=file).json_to_gpx(output_file=output)
            print('\n[+] Done!\n\n')
            self.stop()
        
        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.json_to_gpx()
    
    def gpx_to_csv(self):
        file=input('\n[+] Full-path to the file (filename must end with .gpx) >> ')
        output= input('\n[+] Output path (filename must end with .csv)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            gpx_converter.Converter(input_file=file).gpx_to_csv(output_file=output)
            print('\n[+] Done!\n\n')
            self.stop()

        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.gpx_to_csv()
        
    def csv_to_gpx(self):
        file=input('\n[+] Full-path to the file (filename must end with .csv) >> ')
        output= input('\n[+] Output path (filename must end with .gpx)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            gpx_converter.Converter(input_file=file).csv_to_gpx(output_file=output)
            print('\n[+] Done!\n\n')
            self.stop()

        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.csv_to_gpx()
    
    # DOCUMENTs
    def pdf_to_jpg(self):
        
        # It is needed a Poppler bin file to read pages in pdf!
        file=input('\n[+] Full-path to the file (filename must end with .pdf) >> ')
        output= input('\n[+] Output path (filename must end with .jpg)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            
            pdf= pdf2image.convert_from_path(file)
            for i in range(len(pdf)):
                # Save pages as images in the pdf
                pdf[i].save('page'+ str(i) +'.jpg', 'JPEG')

            print('\n[+] Done!\n\n')
            self.stop()

        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.pdf_to_jpg()

    def jpg_to_pdf(self):
        file=input('\n[+] Full-path to the file (filename must end with .jpg) >> ')
        output= input('\n[+] Output path (filename must end with .pdf)>> ')
        try:
            print('\n[*] Path file = '+file)
            print('\n[*] Save to path = '+output)
            
            image= Image.open(file)
            pdf_bytes= img2pdf.convert(image.filename)

            with open(output,'wb') as pdf:
                pdf.write(pdf_bytes)

            print('\n[+] Done!\n\n')
            self.stop()

        except Exception:
            print('\n[-] Something went wrong! Retry...')
            self.jpg_to_pdf()

    def csv_to_xls(self):
        print('[!] Working progress....')
        self.clear_monitor()

    def xls_to_csv(self):
        print('[!] Working progress....')
        self.clear_monitor()

    # UTILITIEs
    def clear_monitor(self):
        subprocess.call('cls', shell=True)
        print(self.banner)

    def stop(self):
        query= input('\nPress 1 to return to the main page, 0 to close...\n>> ')
        if query=='1':
            print('\nReturning back to the main page...\n')
            time.sleep(2)
            subprocess.call('cls', shell=True)
        elif query=='0':
            print('\nThank you for your OUTSTANDING cooperation!!\n')
            time.sleep(2)
            subprocess.call('cls', shell=True)
            exit()
            

converter= Converter()
