"""NTRLI AI - Minimal Android App"""
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button


class NTRLIApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        layout.add_widget(Label(
            text='NTRLI AI',
            font_size='32sp',
            size_hint_y=0.2
        ))

        layout.add_widget(Label(
            text='Deterministic AI System',
            font_size='18sp',
            size_hint_y=0.1
        ))

        self.input = TextInput(
            hint_text='Enter instruction...',
            multiline=True,
            size_hint_y=0.3
        )
        layout.add_widget(self.input)

        btn = Button(
            text='Execute',
            size_hint_y=0.15
        )
        btn.bind(on_press=self.on_execute)
        layout.add_widget(btn)

        self.output = Label(
            text='Ready',
            size_hint_y=0.25
        )
        layout.add_widget(self.output)

        return layout

    def on_execute(self, instance):
        text = self.input.text
        if text:
            self.output.text = f'Received: {text[:50]}...'
        else:
            self.output.text = 'Please enter an instruction'


if __name__ == '__main__':
    NTRLIApp().run()
