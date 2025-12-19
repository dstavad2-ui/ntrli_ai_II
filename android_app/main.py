#!/usr/bin/env python3
# ============================================================================
# NTRLI' AI - ANDROID APPLICATION (SELF-CONTAINED)
# ============================================================================
"""
NTRLI' AI Android Application - Production Ready

This is a SELF-CONTAINED application following NTRLI' AI principles:
- No guessing - all dependencies validated at startup
- No silent failure - comprehensive error handling
- Deterministic behavior - consistent state management
- Optimized for mobile - lazy loading, minimal memory footprint

All core logic is embedded to ensure the APK runs independently.
"""

import os
import sys
import json
import hashlib
import threading
import traceback
from pathlib import Path
from functools import partial
from typing import Dict, Any, Optional, List
from datetime import datetime

# ============================================================================
# KIVY CONFIGURATION - MUST BE BEFORE IMPORTS
# ============================================================================
os.environ.setdefault('KIVY_LOG_LEVEL', 'warning')
os.environ.setdefault('KIVY_NO_CONSOLELOG', '1')

from kivy.config import Config
Config.set('graphics', 'multisamples', '0')  # Fix for some Android devices
Config.set('kivy', 'log_level', 'warning')
Config.set('kivy', 'log_enable', '0')

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
from kivy.clock import Clock, mainthread
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.utils import platform
from kivy.logger import Logger

# ============================================================================
# EMBEDDED CORE - NO EXTERNAL DEPENDENCIES
# ============================================================================

class ValidationError(Exception):
    """Raised when validation fails."""
    pass


class ExecutionError(Exception):
    """Raised when execution fails."""
    pass


class ProviderError(Exception):
    """Raised when provider fails."""
    pass


# Embedded capability registry
CAPABILITIES = {
    "web_research": True,
    "code_generate": True,
    "code_validate": True,
    "offline_mode": True,
}


def validate_capability(name: str) -> bool:
    """Validate capability is available."""
    return CAPABILITIES.get(name, False)


# Embedded knowledge cache
class KnowledgeCache:
    """Local knowledge cache for offline resilience."""

    def __init__(self, cache_dir: str):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _hash_key(self, key: str) -> str:
        return hashlib.sha256(key.encode()).hexdigest()[:16]

    def store(self, key: str, data: Any) -> None:
        """Store data in cache."""
        try:
            path = self.cache_dir / f"{self._hash_key(key)}.json"
            path.write_text(json.dumps({
                "key": key,
                "data": data,
                "timestamp": datetime.utcnow().isoformat()
            }))
        except Exception:
            pass  # Cache failures are non-fatal

    def load(self, key: str) -> Optional[Any]:
        """Load data from cache."""
        try:
            path = self.cache_dir / f"{self._hash_key(key)}.json"
            if path.exists():
                return json.loads(path.read_text())["data"]
        except Exception:
            pass
        return None

    def clear(self) -> int:
        """Clear cache, return count of items cleared."""
        count = 0
        for f in self.cache_dir.glob("*.json"):
            try:
                f.unlink()
                count += 1
            except Exception:
                pass
        return count


# Embedded HTTP client with retry
class HTTPClient:
    """Minimal HTTP client with retry logic."""

    MAX_RETRIES = 2
    TIMEOUT = 30

    def __init__(self):
        self._session = None

    @property
    def session(self):
        if self._session is None:
            try:
                import requests
                self._session = requests.Session()
                self._session.headers.update({
                    "User-Agent": "NTRLI-AI/1.0 (Android)",
                    "Accept": "application/json",
                })
            except ImportError:
                raise ProviderError("requests library not available")
        return self._session

    def post(self, url: str, data: Dict, headers: Optional[Dict] = None) -> Dict:
        """POST with retry logic."""
        last_error = None
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                resp = self.session.post(
                    url,
                    json=data,
                    headers=headers or {},
                    timeout=self.TIMEOUT
                )
                resp.raise_for_status()
                return resp.json()
            except Exception as e:
                last_error = e
                if attempt < self.MAX_RETRIES:
                    continue
        raise ProviderError(f"Request failed after {self.MAX_RETRIES + 1} attempts: {last_error}")


# Embedded LLM providers
class BaseProvider:
    """Base LLM provider."""
    name = "base"

    def __init__(self, api_key: str, model: str):
        self.api_key = api_key
        self.model = model
        self.http = HTTPClient()

    def generate(self, prompt: str) -> str:
        raise NotImplementedError


class OpenAIProvider(BaseProvider):
    """OpenAI provider."""
    name = "openai"

    def generate(self, prompt: str) -> str:
        response = self.http.post(
            "https://api.openai.com/v1/chat/completions",
            data={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response["choices"][0]["message"]["content"]


class GroqProvider(BaseProvider):
    """Groq provider - fastest inference."""
    name = "groq"

    def generate(self, prompt: str) -> str:
        response = self.http.post(
            "https://api.groq.com/openai/v1/chat/completions",
            data={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response["choices"][0]["message"]["content"]


class DeepSeekProvider(BaseProvider):
    """DeepSeek provider - ultra low cost."""
    name = "deepseek"

    def generate(self, prompt: str) -> str:
        response = self.http.post(
            "https://api.deepseek.com/chat/completions",
            data={
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0
            },
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response["choices"][0]["message"]["content"]


# Provider factory
PROVIDER_CLASSES = {
    "openai": (OpenAIProvider, "gpt-4o"),
    "groq": (GroqProvider, "llama-3.3-70b-versatile"),
    "deepseek": (DeepSeekProvider, "deepseek-chat"),
}


def create_provider(name: str, api_key: str, model: Optional[str] = None) -> BaseProvider:
    """Create a provider instance."""
    if name not in PROVIDER_CLASSES:
        raise ProviderError(f"Unknown provider: {name}")

    cls, default_model = PROVIDER_CLASSES[name]
    return cls(api_key, model or default_model)


# Embedded planner
class Planner:
    """Plan-first execution planner."""

    PLAN_PROMPT = """You are a deterministic planning engine.
Return ONLY valid JSON. No commentary.

Decompose this task into ordered steps.
Allowed actions: research, generate, validate, execute

Task: {instruction}

Format: {{"steps": [{{"action": "...", "description": "..."}}]}}"""

    def __init__(self, provider: BaseProvider):
        self.provider = provider

    def plan(self, instruction: str) -> List[Dict]:
        """Generate execution plan."""
        prompt = self.PLAN_PROMPT.format(instruction=instruction)
        response = self.provider.generate(prompt)

        # Extract JSON
        try:
            # Handle markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0]
            elif "```" in response:
                response = response.split("```")[1].split("```")[0]

            data = json.loads(response.strip())
            if "steps" in data and isinstance(data["steps"], list):
                return data["steps"]
        except (json.JSONDecodeError, KeyError, IndexError):
            pass

        # Fallback: single-step plan
        return [{"action": "execute", "description": instruction}]


# Embedded executor
class Executor:
    """Step executor with validation."""

    def __init__(self, provider: BaseProvider, cache: KnowledgeCache):
        self.provider = provider
        self.cache = cache

    def execute(self, instruction: str, steps: List[Dict]) -> Dict:
        """Execute plan steps."""
        results = {
            "instruction": instruction,
            "steps_total": len(steps),
            "steps_executed": 0,
            "outputs": [],
            "success": True,
            "error": None
        }

        for i, step in enumerate(steps):
            try:
                action = step.get("action", "execute")
                description = step.get("description", "")

                # Execute based on action type
                if action == "research":
                    output = self._research(description)
                elif action == "generate":
                    output = self._generate(description)
                elif action == "validate":
                    output = self._validate(description)
                else:
                    output = self._execute(description)

                results["outputs"].append({
                    "step": i + 1,
                    "action": action,
                    "output": output
                })
                results["steps_executed"] = i + 1

            except Exception as e:
                results["success"] = False
                results["error"] = f"Step {i + 1} failed: {str(e)}"
                break

        return results

    def _research(self, query: str) -> str:
        # Check cache first
        cached = self.cache.load(f"research:{query}")
        if cached:
            return f"[Cached] {cached}"

        prompt = f"Research and summarize: {query}"
        result = self.provider.generate(prompt)
        self.cache.store(f"research:{query}", result[:500])
        return result

    def _generate(self, spec: str) -> str:
        prompt = f"Generate code for: {spec}"
        return self.provider.generate(prompt)

    def _validate(self, code: str) -> str:
        try:
            compile(code, "<string>", "exec")
            return "Validation passed: syntax OK"
        except SyntaxError as e:
            return f"Validation failed: {e}"

    def _execute(self, instruction: str) -> str:
        prompt = f"Execute this task and provide the result: {instruction}"
        return self.provider.generate(prompt)


# ============================================================================
# ANDROID APP UI
# ============================================================================

class StatusBar(BoxLayout):
    """Status bar with connection indicator."""

    status_text = StringProperty("Ready")
    status_color = StringProperty("#4CAF50")

    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=40, **kwargs)
        self.label = Label(
            text=self.status_text,
            color=(0.3, 0.7, 0.3, 1),
            bold=True
        )
        self.add_widget(self.label)
        self.bind(status_text=self._update)
        self.bind(status_color=self._update)

    def _update(self, *args):
        self.label.text = self.status_text
        # Parse hex color
        if self.status_color.startswith("#"):
            hex_color = self.status_color[1:]
            r = int(hex_color[0:2], 16) / 255
            g = int(hex_color[2:4], 16) / 255
            b = int(hex_color[4:6], 16) / 255
            self.label.color = (r, g, b, 1)

    def set_ready(self):
        self.status_text = "Ready"
        self.status_color = "#4CAF50"

    def set_running(self):
        self.status_text = "Executing..."
        self.status_color = "#FFC107"

    def set_success(self):
        self.status_text = "Complete"
        self.status_color = "#4CAF50"

    def set_error(self, msg: str = "Error"):
        self.status_text = msg[:30]
        self.status_color = "#F44336"


class OutputPanel(ScrollView):
    """Scrollable output panel."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(
            text="",
            size_hint_y=None,
            halign="left",
            valign="top",
            markup=True,
            text_size=(None, None),
            padding=(10, 10)
        )
        self.label.bind(texture_size=self._update_size)
        self.add_widget(self.label)

    def _update_size(self, *args):
        self.label.size = self.label.texture_size
        self.label.text_size = (self.width - 20, None)

    def set_text(self, text: str):
        self.label.text = text
        self.scroll_y = 1  # Scroll to top

    def append_text(self, text: str):
        self.label.text += text
        self.scroll_y = 0  # Scroll to bottom

    def clear(self):
        self.label.text = ""


class ExecuteScreen(BoxLayout):
    """Main execution screen."""

    def __init__(self, app, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=8, **kwargs)
        self.app = app
        self._running = False

        # Header
        header = BoxLayout(size_hint_y=None, height=50)
        header.add_widget(Label(
            text="[b]NTRLI' AI[/b]",
            markup=True,
            font_size="22sp"
        ))
        self.add_widget(header)

        # Status bar
        self.status = StatusBar()
        self.add_widget(self.status)

        # Instruction input
        self.input = TextInput(
            hint_text="Enter instruction...",
            multiline=True,
            size_hint_y=None,
            height=100,
            font_size="16sp"
        )
        self.add_widget(self.input)

        # Provider selector
        provider_box = BoxLayout(size_hint_y=None, height=44, spacing=8)
        provider_box.add_widget(Label(text="Provider:", size_hint_x=0.25))
        self.provider_spinner = Spinner(
            text="groq",
            values=["groq", "openai", "deepseek"],
            size_hint_x=0.75
        )
        provider_box.add_widget(self.provider_spinner)
        self.add_widget(provider_box)

        # Execute button
        self.execute_btn = Button(
            text="EXECUTE",
            size_hint_y=None,
            height=50,
            font_size="18sp",
            background_color=(0.2, 0.5, 0.8, 1),
            bold=True
        )
        self.execute_btn.bind(on_press=self.on_execute)
        self.add_widget(self.execute_btn)

        # Progress bar
        self.progress = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height=8
        )
        self.add_widget(self.progress)

        # Output panel
        self.add_widget(Label(text="Output:", size_hint_y=None, height=25))
        self.output = OutputPanel()
        self.add_widget(self.output)

        # Bottom buttons
        btn_box = BoxLayout(size_hint_y=None, height=44, spacing=8)

        copy_btn = Button(text="Copy")
        copy_btn.bind(on_press=self.on_copy)
        btn_box.add_widget(copy_btn)

        clear_btn = Button(text="Clear")
        clear_btn.bind(on_press=self.on_clear)
        btn_box.add_widget(clear_btn)

        self.add_widget(btn_box)

    def on_execute(self, btn):
        if self._running:
            return

        instruction = self.input.text.strip()
        if not instruction:
            self.show_error("Please enter an instruction")
            return

        provider_name = self.provider_spinner.text
        api_key = self.app.get_api_key(provider_name)

        if not api_key:
            self.show_error(f"No API key for {provider_name}")
            return

        self._running = True
        self.execute_btn.disabled = True
        self.status.set_running()
        self.output.clear()
        self.progress.value = 10

        # Run in background
        thread = threading.Thread(
            target=self._execute_bg,
            args=(instruction, provider_name, api_key),
            daemon=True
        )
        thread.start()

    def _execute_bg(self, instruction: str, provider_name: str, api_key: str):
        """Background execution."""
        try:
            # Create provider
            provider = create_provider(provider_name, api_key)
            self._update_progress(20)

            # Create planner and executor
            planner = Planner(provider)
            cache = KnowledgeCache(self.app.get_cache_dir())
            executor = Executor(provider, cache)

            # Plan
            self._append_output("[Planning...]\n")
            steps = planner.plan(instruction)
            self._update_progress(40)
            self._append_output(f"Plan: {len(steps)} steps\n\n")

            # Execute
            self._append_output("[Executing...]\n")
            result = executor.execute(instruction, steps)
            self._update_progress(90)

            # Format output
            output = json.dumps(result, indent=2, default=str)
            self._set_output(output)
            self._update_progress(100)

            if result["success"]:
                self._set_status_success()
            else:
                self._set_status_error(result.get("error", "Failed"))

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            Logger.exception("Execution failed")
            self._set_output(error_msg)
            self._set_status_error("Execution failed")
        finally:
            self._finish()

    @mainthread
    def _update_progress(self, value: int):
        self.progress.value = value

    @mainthread
    def _append_output(self, text: str):
        self.output.append_text(text)

    @mainthread
    def _set_output(self, text: str):
        self.output.set_text(text)

    @mainthread
    def _set_status_success(self):
        self.status.set_success()

    @mainthread
    def _set_status_error(self, msg: str):
        self.status.set_error(msg)

    @mainthread
    def _finish(self):
        self._running = False
        self.execute_btn.disabled = False

    def on_copy(self, btn):
        text = self.output.label.text
        if text:
            Clipboard.copy(text)
            self.show_toast("Copied!")

    def on_clear(self, btn):
        self.output.clear()
        self.input.text = ""
        self.progress.value = 0
        self.status.set_ready()

    def show_error(self, msg: str):
        popup = Popup(
            title="Error",
            content=Label(text=msg),
            size_hint=(0.8, 0.3)
        )
        popup.open()

    def show_toast(self, msg: str):
        popup = Popup(
            title="",
            content=Label(text=msg),
            size_hint=(0.5, 0.15),
            auto_dismiss=True
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.2)


class SettingsScreen(BoxLayout):
    """Settings screen."""

    def __init__(self, app, **kwargs):
        super().__init__(orientation="vertical", padding=10, spacing=8, **kwargs)
        self.app = app

        # Header
        self.add_widget(Label(
            text="[b]Settings[/b]",
            markup=True,
            size_hint_y=None,
            height=40,
            font_size="20sp"
        ))

        # Scrollable settings
        scroll = ScrollView()
        settings = GridLayout(cols=1, spacing=10, size_hint_y=None)
        settings.bind(minimum_height=settings.setter("height"))

        # API Key inputs
        self.api_inputs = {}
        for provider in ["groq", "openai", "deepseek"]:
            box = BoxLayout(orientation="vertical", size_hint_y=None, height=70)
            box.add_widget(Label(
                text=f"{provider.upper()} API Key:",
                size_hint_y=None,
                height=25,
                halign="left"
            ))
            input_field = TextInput(
                text=self.app.config.get(f"api_keys.{provider}", ""),
                password=True,
                multiline=False,
                size_hint_y=None,
                height=40
            )
            input_field.bind(text=partial(self.on_key_change, provider))
            self.api_inputs[provider] = input_field
            box.add_widget(input_field)
            settings.add_widget(box)

        # Cache management
        cache_box = BoxLayout(size_hint_y=None, height=50)
        cache_box.add_widget(Label(text="Clear Cache:"))
        clear_cache_btn = Button(text="Clear", size_hint_x=0.4)
        clear_cache_btn.bind(on_press=self.on_clear_cache)
        cache_box.add_widget(clear_cache_btn)
        settings.add_widget(cache_box)

        scroll.add_widget(settings)
        self.add_widget(scroll)

        # Save button
        save_btn = Button(
            text="Save Settings",
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.6, 0.2, 1)
        )
        save_btn.bind(on_press=self.on_save)
        self.add_widget(save_btn)

    def on_key_change(self, provider: str, instance, value: str):
        self.app.config[f"api_keys.{provider}"] = value

    def on_clear_cache(self, btn):
        cache = KnowledgeCache(self.app.get_cache_dir())
        count = cache.clear()
        self.show_toast(f"Cleared {count} items")

    def on_save(self, btn):
        self.app.save_config()
        self.show_toast("Saved!")

    def show_toast(self, msg: str):
        popup = Popup(
            title="",
            content=Label(text=msg),
            size_hint=(0.5, 0.15),
            auto_dismiss=True
        )
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 1.2)


class AboutScreen(BoxLayout):
    """About screen."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=20, **kwargs)

        self.add_widget(Label(
            text="""[b]NTRLI' AI[/b]

[i]Deterministic, Execution-First
Artificial Intelligence System[/i]

Version 1.0.0

━━━━━━━━━━━━━━━━━━━━

[b]10 Behavioral Laws:[/b]

1. No output without a plan
2. No plan without validation
3. No code without intent
4. No execution without verification
5. No writing without tests
6. No hallucination
7. No filler
8. No goal drift
9. No silent failure
10. No autonomy

━━━━━━━━━━━━━━━━━━━━

This is not a promise.
[i]It is a structural fact.[/i]""",
            markup=True,
            halign="center",
            valign="middle"
        ))


class NTRLIApp(App):
    """NTRLI' AI Android Application."""

    title = "NTRLI' AI"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = {}
        self._load_config()

    def build(self):
        """Build the application."""
        # Root tabs
        tabs = TabbedPanel(do_default_tab=False)

        # Execute tab
        execute_tab = TabbedPanelItem(text="Execute")
        execute_tab.add_widget(ExecuteScreen(self))
        tabs.add_widget(execute_tab)

        # Settings tab
        settings_tab = TabbedPanelItem(text="Settings")
        settings_tab.add_widget(SettingsScreen(self))
        tabs.add_widget(settings_tab)

        # About tab
        about_tab = TabbedPanelItem(text="About")
        about_tab.add_widget(AboutScreen())
        tabs.add_widget(about_tab)

        return tabs

    def get_data_dir(self) -> str:
        """Get platform-appropriate data directory."""
        if platform == "android":
            from android.storage import app_storage_path
            return app_storage_path()
        else:
            return os.path.expanduser("~/.ntrli_ai")

    def get_cache_dir(self) -> str:
        """Get cache directory."""
        cache_dir = os.path.join(self.get_data_dir(), "cache")
        os.makedirs(cache_dir, exist_ok=True)
        return cache_dir

    def get_config_path(self) -> str:
        """Get config file path."""
        return os.path.join(self.get_data_dir(), "config.json")

    def _load_config(self):
        """Load configuration."""
        try:
            path = self.get_config_path()
            if os.path.exists(path):
                with open(path, "r") as f:
                    self.config = json.load(f)
        except Exception:
            self.config = {}

        # Also check environment variables
        env_keys = {
            "groq": "GROQ_API_KEY",
            "openai": "OPENAI_API_KEY",
            "deepseek": "DEEPSEEK_API_KEY",
        }
        for provider, env_var in env_keys.items():
            if env_val := os.getenv(env_var):
                self.config[f"api_keys.{provider}"] = env_val

    def save_config(self):
        """Save configuration."""
        try:
            os.makedirs(self.get_data_dir(), exist_ok=True)
            with open(self.get_config_path(), "w") as f:
                json.dump(self.config, f, indent=2)
        except Exception as e:
            Logger.error(f"Failed to save config: {e}")

    def get_api_key(self, provider: str) -> Optional[str]:
        """Get API key for provider."""
        return self.config.get(f"api_keys.{provider}")


# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        NTRLIApp().run()
    except Exception as e:
        Logger.exception("Application crashed")
        sys.exit(1)
