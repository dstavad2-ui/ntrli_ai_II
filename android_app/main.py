#!/usr/bin/env python3
# ============================================================================
# NTRLI' AI - ANDROID APPLICATION
# ============================================================================
"""
NTRLI' AI Android Application built with Kivy.

Features:
- Clean, modern UI for instruction input
- Provider selection and configuration
- Real-time execution output
- Settings management
"""

import os
import json
import threading
from functools import partial

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.switch import Switch
from kivy.uix.popup import Popup
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty, BooleanProperty, ListProperty
from kivy.utils import platform

# Import NTRLI AI core (will be bundled with the APK)
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from ntrli_ai.config import get_config, init_config
    from ntrli_ai.providers.registry import get_provider, list_providers
    from ntrli_ai.providers.router import Router, RouterStrategy
    from ntrli_ai.control_plane import ControlPlane
    NTRLI_AVAILABLE = True
except ImportError:
    NTRLI_AVAILABLE = False


class SettingsScreen(BoxLayout):
    """Settings configuration screen."""

    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        self.app = app

        # Header
        self.add_widget(Label(
            text='[b]Settings[/b]',
            markup=True,
            size_hint_y=None,
            height=40,
            font_size='20sp'
        ))

        # Scrollable settings
        scroll = ScrollView()
        settings_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        settings_layout.bind(minimum_height=settings_layout.setter('height'))

        # Router Strategy
        strategy_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        strategy_box.add_widget(Label(text='Router Strategy:', size_hint_x=0.4))
        self.strategy_spinner = Spinner(
            text='fallback',
            values=['fastest', 'cheapest', 'smartest', 'consensus', 'fallback'],
            size_hint_x=0.6
        )
        self.strategy_spinner.bind(text=self.on_strategy_change)
        strategy_box.add_widget(self.strategy_spinner)
        settings_layout.add_widget(strategy_box)

        # Verbose mode
        verbose_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        verbose_box.add_widget(Label(text='Verbose Output:', size_hint_x=0.7))
        self.verbose_switch = Switch(active=False, size_hint_x=0.3)
        self.verbose_switch.bind(active=self.on_verbose_change)
        verbose_box.add_widget(self.verbose_switch)
        settings_layout.add_widget(verbose_box)

        # Show Plan
        plan_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        plan_box.add_widget(Label(text='Show Execution Plan:', size_hint_x=0.7))
        self.plan_switch = Switch(active=True, size_hint_x=0.3)
        self.plan_switch.bind(active=self.on_plan_change)
        plan_box.add_widget(self.plan_switch)
        settings_layout.add_widget(plan_box)

        # Provider section header
        settings_layout.add_widget(Label(
            text='[b]Providers[/b]',
            markup=True,
            size_hint_y=None,
            height=40
        ))

        # Provider toggles
        self.provider_switches = {}
        providers = ['openai', 'claude', 'gemini', 'groq', 'mistral', 'together', 'deepseek']
        for provider in providers:
            provider_box = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
            provider_box.add_widget(Label(text=provider.title() + ':', size_hint_x=0.7))
            switch = Switch(active=True, size_hint_x=0.3)
            switch.bind(active=partial(self.on_provider_change, provider))
            self.provider_switches[provider] = switch
            provider_box.add_widget(switch)
            settings_layout.add_widget(provider_box)

        scroll.add_widget(settings_layout)
        self.add_widget(scroll)

        # Save button
        save_btn = Button(
            text='Save Settings',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.2, 1)
        )
        save_btn.bind(on_press=self.save_settings)
        self.add_widget(save_btn)

    def on_strategy_change(self, spinner, text):
        self.app.config_data['router']['strategy'] = text

    def on_verbose_change(self, switch, value):
        self.app.config_data['ui']['verbose'] = value

    def on_plan_change(self, switch, value):
        self.app.config_data['ui']['show_plan'] = value

    def on_provider_change(self, provider, switch, value):
        self.app.config_data['providers'][provider]['enabled'] = value

    def save_settings(self, btn):
        self.app.save_config()
        self.show_toast('Settings saved!')

    def show_toast(self, message):
        popup = Popup(
            title='',
            content=Label(text=message),
            size_hint=(0.6, 0.2),
            auto_dismiss=True
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)


class ExecutionScreen(BoxLayout):
    """Main execution screen."""

    output_text = StringProperty('')
    is_running = BooleanProperty(False)

    def __init__(self, app, **kwargs):
        super().__init__(orientation='vertical', padding=10, spacing=10, **kwargs)
        self.app = app

        # Header
        header = BoxLayout(size_hint_y=None, height=60)
        header.add_widget(Label(
            text="[b]NTRLI' AI[/b]",
            markup=True,
            font_size='24sp'
        ))
        self.add_widget(header)

        # Status indicator
        self.status_label = Label(
            text='Ready',
            size_hint_y=None,
            height=30,
            color=(0.5, 0.8, 0.5, 1)
        )
        self.add_widget(self.status_label)

        # Instruction input
        self.instruction_input = TextInput(
            hint_text='Enter your instruction here...',
            multiline=True,
            size_hint_y=None,
            height=100,
            font_size='16sp'
        )
        self.add_widget(self.instruction_input)

        # Strategy selector
        strategy_box = BoxLayout(size_hint_y=None, height=50, spacing=10)
        strategy_box.add_widget(Label(text='Strategy:', size_hint_x=0.3))
        self.strategy_spinner = Spinner(
            text='fallback',
            values=['fastest', 'cheapest', 'smartest', 'consensus', 'fallback'],
            size_hint_x=0.7
        )
        strategy_box.add_widget(self.strategy_spinner)
        self.add_widget(strategy_box)

        # Execute button
        self.execute_btn = Button(
            text='Execute',
            size_hint_y=None,
            height=60,
            font_size='20sp',
            background_color=(0.2, 0.5, 0.8, 1)
        )
        self.execute_btn.bind(on_press=self.execute)
        self.add_widget(self.execute_btn)

        # Progress bar
        self.progress = ProgressBar(max=100, size_hint_y=None, height=10)
        self.add_widget(self.progress)

        # Output area
        self.add_widget(Label(text='Output:', size_hint_y=None, height=30))

        self.output_scroll = ScrollView()
        self.output_label = Label(
            text='',
            size_hint_y=None,
            text_size=(None, None),
            halign='left',
            valign='top',
            markup=True
        )
        self.output_label.bind(texture_size=self.output_label.setter('size'))
        self.output_scroll.add_widget(self.output_label)
        self.add_widget(self.output_scroll)

        # Bottom buttons
        btn_box = BoxLayout(size_hint_y=None, height=50, spacing=10)

        copy_btn = Button(text='Copy Output')
        copy_btn.bind(on_press=self.copy_output)
        btn_box.add_widget(copy_btn)

        clear_btn = Button(text='Clear')
        clear_btn.bind(on_press=self.clear_output)
        btn_box.add_widget(clear_btn)

        self.add_widget(btn_box)

    def execute(self, btn):
        if self.is_running:
            return

        instruction = self.instruction_input.text.strip()
        if not instruction:
            self.show_error('Please enter an instruction')
            return

        self.is_running = True
        self.execute_btn.disabled = True
        self.status_label.text = 'Executing...'
        self.status_label.color = (0.8, 0.8, 0.2, 1)
        self.output_label.text = ''
        self.progress.value = 10

        # Run in background thread
        thread = threading.Thread(
            target=self._execute_task,
            args=(instruction, self.strategy_spinner.text)
        )
        thread.start()

    def _execute_task(self, instruction, strategy):
        """Execute instruction in background thread."""
        try:
            if not NTRLI_AVAILABLE:
                result = {
                    'error': 'NTRLI AI core not available',
                    'message': 'Running in demo mode'
                }
            else:
                # Initialize providers from environment
                providers = self.app.initialize_providers()

                if not providers:
                    result = {
                        'error': 'No API keys configured',
                        'message': 'Set API keys in Settings or environment variables'
                    }
                else:
                    router = Router(providers)
                    control_plane = ControlPlane(router)

                    result = control_plane.handle({
                        'command': 'EXECUTE',
                        'conversation_id': 'android-app',
                        'instructions': instruction
                    })

            Clock.schedule_once(lambda dt: self._on_complete(result))

        except Exception as e:
            Clock.schedule_once(lambda dt: self._on_error(str(e)))

    def _on_complete(self, result):
        """Handle completion on main thread."""
        self.is_running = False
        self.execute_btn.disabled = False
        self.progress.value = 100
        self.status_label.text = 'Complete'
        self.status_label.color = (0.5, 0.8, 0.5, 1)

        if isinstance(result, dict):
            self.output_label.text = json.dumps(result, indent=2, default=str)
        else:
            self.output_label.text = str(result)

    def _on_error(self, error):
        """Handle error on main thread."""
        self.is_running = False
        self.execute_btn.disabled = False
        self.progress.value = 0
        self.status_label.text = 'Error'
        self.status_label.color = (0.8, 0.3, 0.3, 1)
        self.output_label.text = f'[color=ff3333]Error: {error}[/color]'

    def copy_output(self, btn):
        if self.output_label.text:
            Clipboard.copy(self.output_label.text)
            self.show_toast('Copied to clipboard')

    def clear_output(self, btn):
        self.output_label.text = ''
        self.instruction_input.text = ''
        self.progress.value = 0
        self.status_label.text = 'Ready'
        self.status_label.color = (0.5, 0.8, 0.5, 1)

    def show_error(self, message):
        popup = Popup(
            title='Error',
            content=Label(text=message),
            size_hint=(0.8, 0.3)
        )
        popup.open()

    def show_toast(self, message):
        popup = Popup(
            title='',
            content=Label(text=message),
            size_hint=(0.6, 0.15),
            auto_dismiss=True
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.5)


class NTRLIApp(App):
    """NTRLI' AI Android Application."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_data = self.load_config()

    def build(self):
        """Build the application UI."""
        # Main layout with tabs
        self.tabs = TabbedPanel(do_default_tab=False)

        # Execute tab
        execute_tab = TabbedPanelItem(text='Execute')
        execute_tab.add_widget(ExecutionScreen(self))
        self.tabs.add_widget(execute_tab)

        # Settings tab
        settings_tab = TabbedPanelItem(text='Settings')
        settings_tab.add_widget(SettingsScreen(self))
        self.tabs.add_widget(settings_tab)

        # About tab
        about_tab = TabbedPanelItem(text='About')
        about_content = BoxLayout(orientation='vertical', padding=20)
        about_content.add_widget(Label(
            text="[b]NTRLI' AI[/b]\n\n"
                 "Deterministic, Execution-First\n"
                 "Artificial Intelligence System\n\n"
                 "Version 1.0.0\n\n"
                 "[i]10 Behavioral Laws Enforced[/i]",
            markup=True,
            halign='center',
            font_size='18sp'
        ))
        about_tab.add_widget(about_content)
        self.tabs.add_widget(about_tab)

        return self.tabs

    def load_config(self):
        """Load configuration."""
        default_config = {
            'providers': {
                'openai': {'enabled': True, 'model': 'gpt-4o'},
                'claude': {'enabled': True, 'model': 'claude-sonnet-4-20250514'},
                'gemini': {'enabled': True, 'model': 'gemini-2.5-flash'},
                'groq': {'enabled': True, 'model': 'llama-3.3-70b-versatile'},
                'mistral': {'enabled': True, 'model': 'mistral-large-latest'},
                'together': {'enabled': True, 'model': 'meta-llama/Llama-3.3-70B-Instruct'},
                'deepseek': {'enabled': True, 'model': 'deepseek-chat'},
            },
            'router': {
                'strategy': 'fallback',
                'timeout_seconds': 30,
            },
            'ui': {
                'verbose': False,
                'show_plan': True,
            }
        }

        config_path = self.get_config_path()
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    return json.load(f)
            except:
                pass

        return default_config

    def save_config(self):
        """Save configuration."""
        config_path = self.get_config_path()
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, 'w') as f:
            json.dump(self.config_data, f, indent=2)

    def get_config_path(self):
        """Get platform-appropriate config path."""
        if platform == 'android':
            from android.storage import app_storage_path
            return os.path.join(app_storage_path(), 'config.json')
        else:
            return os.path.expanduser('~/.ntrli_ai/android_config.json')

    def initialize_providers(self):
        """Initialize enabled providers."""
        if not NTRLI_AVAILABLE:
            return {}

        providers = {}
        provider_configs = self.config_data.get('providers', {})

        env_keys = {
            'openai': 'OPENAI_API_KEY',
            'claude': 'ANTHROPIC_API_KEY',
            'gemini': 'GOOGLE_API_KEY',
            'groq': 'GROQ_API_KEY',
            'mistral': 'MISTRAL_API_KEY',
            'together': 'TOGETHER_API_KEY',
            'deepseek': 'DEEPSEEK_API_KEY',
        }

        for name, config in provider_configs.items():
            if not config.get('enabled', True):
                continue

            env_key = env_keys.get(name)
            if not env_key:
                continue

            api_key = os.getenv(env_key)
            if not api_key:
                continue

            try:
                model = config.get('model')
                providers[name] = get_provider(name, api_key=api_key, model=model)
            except Exception:
                pass

        return providers


if __name__ == '__main__':
    NTRLIApp().run()
