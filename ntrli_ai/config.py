#!/usr/bin/env python3
# ============================================================================
# NTRLI' AI - CONFIGURATION SYSTEM
# ============================================================================
"""
Easy configuration system for NTRLI' AI.

Supports:
- JSON settings file (~/.ntrli_ai/settings.json)
- Environment variable overrides
- CLI configuration commands
- Project-local settings (.ntrli_ai.json)

Similar to Claude Code's configuration style.
"""

import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field, asdict


# Default paths
USER_CONFIG_DIR = Path.home() / ".ntrli_ai"
USER_SETTINGS_FILE = USER_CONFIG_DIR / "settings.json"
LOCAL_SETTINGS_FILE = Path(".ntrli_ai.json")


@dataclass
class ProviderConfig:
    """Configuration for a single LLM provider."""
    enabled: bool = True
    api_key: Optional[str] = None
    model: Optional[str] = None
    priority: int = 0  # Lower = higher priority


@dataclass
class RouterConfig:
    """Router configuration."""
    strategy: str = "fallback"  # fastest, cheapest, smartest, consensus, fallback
    timeout_seconds: int = 30
    max_retries: int = 2


@dataclass
class ExecutionConfig:
    """Execution settings."""
    sandbox_timeout: int = 30
    test_timeout: int = 60
    max_steps: int = 20
    enable_cache: bool = True
    cache_dir: str = "knowledge_cache"


@dataclass
class GitHubConfig:
    """GitHub integration settings."""
    enabled: bool = True
    auto_commit: bool = False
    branch_prefix: str = "ntrli-ai/"
    commit_author: str = "NTRLI AI"
    commit_email: str = "ntrli-ai@users.noreply.github.com"


@dataclass
class UIConfig:
    """UI and output settings."""
    verbose: bool = False
    color_output: bool = True
    show_plan: bool = True
    show_progress: bool = True
    json_output: bool = False


@dataclass
class Settings:
    """Complete NTRLI' AI settings."""
    # Provider configurations
    providers: Dict[str, Dict[str, Any]] = field(default_factory=lambda: {
        "openai": {"enabled": True, "model": "gpt-4o", "priority": 2},
        "claude": {"enabled": True, "model": "claude-sonnet-4-20250514", "priority": 1},
        "gemini": {"enabled": True, "model": "gemini-2.5-flash", "priority": 3},
        "groq": {"enabled": True, "model": "llama-3.3-70b-versatile", "priority": 0},
        "mistral": {"enabled": True, "model": "mistral-large-latest", "priority": 4},
        "together": {"enabled": True, "model": "meta-llama/Llama-3.3-70B-Instruct", "priority": 5},
        "deepseek": {"enabled": True, "model": "deepseek-chat", "priority": 6},
        "replicate": {"enabled": False, "model": "meta/meta-llama-3.3-70b-instruct", "priority": 7},
        "huggingface": {"enabled": False, "model": "meta-llama/Llama-3.3-70B-Instruct", "priority": 8},
        "cohere": {"enabled": False, "model": "command-r-plus", "priority": 9},
    })

    # Router settings
    router: Dict[str, Any] = field(default_factory=lambda: {
        "strategy": "fallback",
        "timeout_seconds": 30,
        "max_retries": 2,
    })

    # Execution settings
    execution: Dict[str, Any] = field(default_factory=lambda: {
        "sandbox_timeout": 30,
        "test_timeout": 60,
        "max_steps": 20,
        "enable_cache": True,
        "cache_dir": "knowledge_cache",
    })

    # GitHub settings
    github: Dict[str, Any] = field(default_factory=lambda: {
        "enabled": True,
        "auto_commit": False,
        "branch_prefix": "ntrli-ai/",
        "commit_author": "NTRLI AI",
        "commit_email": "ntrli-ai@users.noreply.github.com",
    })

    # UI settings
    ui: Dict[str, Any] = field(default_factory=lambda: {
        "verbose": False,
        "color_output": True,
        "show_plan": True,
        "show_progress": True,
        "json_output": False,
    })


class ConfigManager:
    """
    Configuration manager for NTRLI' AI.

    Loads settings from:
    1. Default values
    2. User config file (~/.ntrli_ai/settings.json)
    3. Local project file (.ntrli_ai.json)
    4. Environment variables
    """

    def __init__(self):
        self._settings: Optional[Settings] = None
        self._loaded = False

    @property
    def settings(self) -> Settings:
        """Get current settings, loading if necessary."""
        if not self._loaded:
            self.load()
        return self._settings

    def load(self) -> Settings:
        """Load settings from all sources."""
        # Start with defaults
        self._settings = Settings()

        # Load user config
        if USER_SETTINGS_FILE.exists():
            self._merge_from_file(USER_SETTINGS_FILE)

        # Load local config (overrides user)
        if LOCAL_SETTINGS_FILE.exists():
            self._merge_from_file(LOCAL_SETTINGS_FILE)

        # Apply environment overrides
        self._apply_env_overrides()

        self._loaded = True
        return self._settings

    def _merge_from_file(self, path: Path) -> None:
        """Merge settings from a JSON file."""
        try:
            data = json.loads(path.read_text())
            self._merge_dict(data)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Warning: Failed to load config from {path}: {e}")

    def _merge_dict(self, data: Dict[str, Any]) -> None:
        """Merge a dictionary into current settings."""
        if "providers" in data:
            for name, config in data["providers"].items():
                if name in self._settings.providers:
                    self._settings.providers[name].update(config)
                else:
                    self._settings.providers[name] = config

        if "router" in data:
            self._settings.router.update(data["router"])

        if "execution" in data:
            self._settings.execution.update(data["execution"])

        if "github" in data:
            self._settings.github.update(data["github"])

        if "ui" in data:
            self._settings.ui.update(data["ui"])

    def _apply_env_overrides(self) -> None:
        """Apply environment variable overrides."""
        # Router strategy
        if strategy := os.getenv("ROUTER_STRATEGY"):
            self._settings.router["strategy"] = strategy

        # UI settings
        if os.getenv("NTRLI_VERBOSE"):
            self._settings.ui["verbose"] = True
        if os.getenv("NTRLI_JSON_OUTPUT"):
            self._settings.ui["json_output"] = True
        if os.getenv("NO_COLOR"):
            self._settings.ui["color_output"] = False

        # Execution settings
        if timeout := os.getenv("NTRLI_SANDBOX_TIMEOUT"):
            self._settings.execution["sandbox_timeout"] = int(timeout)

    def save_user_settings(self) -> None:
        """Save current settings to user config file."""
        USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        USER_SETTINGS_FILE.write_text(
            json.dumps(asdict(self._settings), indent=2)
        )

    def save_local_settings(self) -> None:
        """Save current settings to local project file."""
        LOCAL_SETTINGS_FILE.write_text(
            json.dumps(asdict(self._settings), indent=2)
        )

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a setting by dot-notation key.

        Example: config.get("router.strategy")
        """
        parts = key.split(".")
        value = asdict(self.settings)

        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return default

        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a setting by dot-notation key.

        Example: config.set("router.strategy", "fastest")
        """
        parts = key.split(".")

        if len(parts) == 1:
            setattr(self._settings, key, value)
        elif len(parts) == 2:
            section, setting = parts
            if hasattr(self._settings, section):
                getattr(self._settings, section)[setting] = value

    def reset(self) -> None:
        """Reset to default settings."""
        self._settings = Settings()
        self._loaded = True

    def list_providers(self) -> List[str]:
        """List all configured providers."""
        return list(self.settings.providers.keys())

    def get_enabled_providers(self) -> List[str]:
        """List enabled providers sorted by priority."""
        enabled = [
            (name, config.get("priority", 99))
            for name, config in self.settings.providers.items()
            if config.get("enabled", True)
        ]
        return [name for name, _ in sorted(enabled, key=lambda x: x[1])]

    def enable_provider(self, name: str) -> None:
        """Enable a provider."""
        if name in self.settings.providers:
            self.settings.providers[name]["enabled"] = True

    def disable_provider(self, name: str) -> None:
        """Disable a provider."""
        if name in self.settings.providers:
            self.settings.providers[name]["enabled"] = False

    def set_provider_model(self, name: str, model: str) -> None:
        """Set model for a provider."""
        if name in self.settings.providers:
            self.settings.providers[name]["model"] = model

    def to_dict(self) -> Dict[str, Any]:
        """Export settings as dictionary."""
        return asdict(self.settings)

    def to_json(self, indent: int = 2) -> str:
        """Export settings as JSON string."""
        return json.dumps(self.to_dict(), indent=indent)


# Global config instance
_config: Optional[ConfigManager] = None


def get_config() -> ConfigManager:
    """Get the global configuration manager."""
    global _config
    if _config is None:
        _config = ConfigManager()
    return _config


def init_config() -> None:
    """Initialize configuration (create default files if needed)."""
    config = get_config()
    config.load()

    # Create user config dir if it doesn't exist
    if not USER_CONFIG_DIR.exists():
        USER_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
        config.save_user_settings()
        print(f"Created config directory: {USER_CONFIG_DIR}")


# CLI-style configuration functions
def config_get(key: str) -> Any:
    """Get a configuration value."""
    return get_config().get(key)


def config_set(key: str, value: Any) -> None:
    """Set a configuration value."""
    config = get_config()
    config.set(key, value)
    config.save_user_settings()


def config_list() -> Dict[str, Any]:
    """List all configuration."""
    return get_config().to_dict()


def config_reset() -> None:
    """Reset configuration to defaults."""
    config = get_config()
    config.reset()
    config.save_user_settings()
