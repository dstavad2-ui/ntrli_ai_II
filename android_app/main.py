from kivy.app import App
from kivy.uix.label import Label

class NTRLIApp(App):
    def build(self):
        return Label(text="NTRLI APK BUILD OK", font_size=24)

if __name__ == "__main__":
    NTRLIApp().run()
