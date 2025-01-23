from kivy.app import App
from kivy.uix.label import Label
from plyer import gps

class GPSApp(App):
    def build(self):
        self.label = Label(text='Getting GPS location...')
        gps.configure(on_location=self.on_location)
        gps.start()
        return self.label

    def on_location(self, **kwargs):
        latitude = kwargs.get('lat', 0)
        longitude = kwargs.get('lon', 0)
        self.label.text = f'Latitude: {latitude}\nLongitude: {longitude}'

if __name__ == '__main__':
    GPSApp().run()