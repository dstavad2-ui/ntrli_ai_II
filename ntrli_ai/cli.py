#!/usr/bin/env python3
# ============================================================================
# NTRLI' AI - CLI INTERFACE
# ============================================================================
"""
Command-line interface for NTRLI' AI.

Commands:
    ntrli run <instruction>     Execute an instruction
    ntrli config                Show current configuration
    ntrli config get <key>      Get a config value
    ntrli config set <key> <value>  Set a config value
    ntrli config reset          Reset to defaults
    ntrli config init           Initialize config files
    ntrli providers             List available providers
    ntrli providers enable <name>   Enable a provider
    ntrli providers disable <name>  Disable a provider
"""

import sys
import json
import argparse
from typing import List, Optional

from config import (
    get_config,
    init_config,
    config_get,
    config_set,
    config_list,
    config_reset,
    USER_CONFIG_DIR,
    USER_SETTINGS_FILE,
)


class Colors:
    """ANSI color codes for terminal output."""
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'

    @classmethod
    def disable(cls):
        """Disable colors."""
        cls.HEADER = ''
        cls.BLUE = ''
        cls.CYAN = ''
        cls.GREEN = ''
        cls.YELLOW = ''
        cls.RED = ''
        cls.BOLD = ''
        cls.DIM = ''
        cls.RESET = ''


def print_header(text: str) -> None:
    """Print a header."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{text}{Colors.RESET}")
    print(f"{Colors.DIM}{'─' * len(text)}{Colors.RESET}")


def print_success(text: str) -> None:
    """Print success message."""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text: str) -> None:
    """Print error message."""
    print(f"{Colors.RED}✗{Colors.RESET} {text}", file=sys.stderr)


def print_info(text: str) -> None:
    """Print info message."""
    print(f"{Colors.BLUE}ℹ{Colors.RESET} {text}")


def print_key_value(key: str, value: str, indent: int = 0) -> None:
    """Print key-value pair."""
    prefix = "  " * indent
    print(f"{prefix}{Colors.CYAN}{key}{Colors.RESET}: {value}")


def cmd_config_show(args: argparse.Namespace) -> int:
    """Show current configuration."""
    config = get_config()
    settings = config.to_dict()

    print_header("NTRLI' AI Configuration")

    # Show config file locations
    print_info(f"User config: {USER_SETTINGS_FILE}")
    print()

    # Show settings by section
    for section, values in settings.items():
        print(f"{Colors.BOLD}{section}:{Colors.RESET}")
        if isinstance(values, dict):
            for key, value in values.items():
                if isinstance(value, dict):
                    print(f"  {Colors.CYAN}{key}{Colors.RESET}:")
                    for k, v in value.items():
                        print_key_value(k, str(v), indent=2)
                else:
                    print_key_value(key, str(value), indent=1)
        else:
            print(f"  {values}")
        print()

    return 0


def cmd_config_get(args: argparse.Namespace) -> int:
    """Get a configuration value."""
    value = config_get(args.key)
    if value is None:
        print_error(f"Key not found: {args.key}")
        return 1

    if isinstance(value, (dict, list)):
        print(json.dumps(value, indent=2))
    else:
        print(value)
    return 0


def cmd_config_set(args: argparse.Namespace) -> int:
    """Set a configuration value."""
    # Try to parse value as JSON for complex types
    try:
        value = json.loads(args.value)
    except json.JSONDecodeError:
        # Use as string
        value = args.value

        # Convert common string values
        if value.lower() == "true":
            value = True
        elif value.lower() == "false":
            value = False
        elif value.isdigit():
            value = int(value)

    config_set(args.key, value)
    print_success(f"Set {args.key} = {value}")
    return 0


def cmd_config_reset(args: argparse.Namespace) -> int:
    """Reset configuration to defaults."""
    config_reset()
    print_success("Configuration reset to defaults")
    return 0


def cmd_config_init(args: argparse.Namespace) -> int:
    """Initialize configuration files."""
    init_config()
    print_success(f"Configuration initialized at {USER_CONFIG_DIR}")
    return 0


def cmd_providers_list(args: argparse.Namespace) -> int:
    """List available providers."""
    config = get_config()

    print_header("LLM Providers")

    providers = config.settings.providers
    enabled = config.get_enabled_providers()

    for name in enabled:
        cfg = providers[name]
        model = cfg.get("model", "default")
        priority = cfg.get("priority", 99)
        print(f"  {Colors.GREEN}●{Colors.RESET} {Colors.BOLD}{name}{Colors.RESET}")
        print(f"    model: {model}")
        print(f"    priority: {priority}")
        print()

    disabled = [n for n in providers if n not in enabled]
    if disabled:
        print(f"{Colors.DIM}Disabled: {', '.join(disabled)}{Colors.RESET}")

    return 0


def cmd_providers_enable(args: argparse.Namespace) -> int:
    """Enable a provider."""
    config = get_config()
    config.enable_provider(args.name)
    config.save_user_settings()
    print_success(f"Enabled provider: {args.name}")
    return 0


def cmd_providers_disable(args: argparse.Namespace) -> int:
    """Disable a provider."""
    config = get_config()
    config.disable_provider(args.name)
    config.save_user_settings()
    print_success(f"Disabled provider: {args.name}")
    return 0


def cmd_providers_set_model(args: argparse.Namespace) -> int:
    """Set model for a provider."""
    config = get_config()
    config.set_provider_model(args.name, args.model)
    config.save_user_settings()
    print_success(f"Set {args.name} model to: {args.model}")
    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """Run an instruction."""
    # Import here to avoid circular imports
    from main import main as run_main

    # Set instruction in sys.argv
    sys.argv = ["ntrli", args.instruction]
    return run_main() or 0


def cmd_version(args: argparse.Namespace) -> int:
    """Show version."""
    print("NTRLI' AI v1.0.0")
    return 0


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog="ntrli",
        description="NTRLI' AI - Deterministic Execution-First AI System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output"
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output in JSON format"
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # run command
    run_parser = subparsers.add_parser("run", help="Execute an instruction")
    run_parser.add_argument("instruction", help="The instruction to execute")
    run_parser.set_defaults(func=cmd_run)

    # config command
    config_parser = subparsers.add_parser("config", help="Configuration commands")
    config_subparsers = config_parser.add_subparsers(dest="config_command")

    # config show (default)
    config_show = config_subparsers.add_parser("show", help="Show configuration")
    config_show.set_defaults(func=cmd_config_show)

    # config get
    config_get_parser = config_subparsers.add_parser("get", help="Get a config value")
    config_get_parser.add_argument("key", help="Configuration key (dot notation)")
    config_get_parser.set_defaults(func=cmd_config_get)

    # config set
    config_set_parser = config_subparsers.add_parser("set", help="Set a config value")
    config_set_parser.add_argument("key", help="Configuration key (dot notation)")
    config_set_parser.add_argument("value", help="Value to set")
    config_set_parser.set_defaults(func=cmd_config_set)

    # config reset
    config_reset_parser = config_subparsers.add_parser("reset", help="Reset to defaults")
    config_reset_parser.set_defaults(func=cmd_config_reset)

    # config init
    config_init_parser = config_subparsers.add_parser("init", help="Initialize config")
    config_init_parser.set_defaults(func=cmd_config_init)

    config_parser.set_defaults(func=cmd_config_show)

    # providers command
    providers_parser = subparsers.add_parser("providers", help="Provider commands")
    providers_subparsers = providers_parser.add_subparsers(dest="providers_command")

    # providers list
    providers_list = providers_subparsers.add_parser("list", help="List providers")
    providers_list.set_defaults(func=cmd_providers_list)

    # providers enable
    providers_enable = providers_subparsers.add_parser("enable", help="Enable provider")
    providers_enable.add_argument("name", help="Provider name")
    providers_enable.set_defaults(func=cmd_providers_enable)

    # providers disable
    providers_disable = providers_subparsers.add_parser("disable", help="Disable provider")
    providers_disable.add_argument("name", help="Provider name")
    providers_disable.set_defaults(func=cmd_providers_disable)

    # providers model
    providers_model = providers_subparsers.add_parser("model", help="Set provider model")
    providers_model.add_argument("name", help="Provider name")
    providers_model.add_argument("model", help="Model name")
    providers_model.set_defaults(func=cmd_providers_set_model)

    providers_parser.set_defaults(func=cmd_providers_list)

    # version command
    version_parser = subparsers.add_parser("version", help="Show version")
    version_parser.set_defaults(func=cmd_version)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args(argv)

    # Handle color settings
    if args.no_color:
        Colors.disable()

    # Default to help if no command
    if not args.command:
        parser.print_help()
        return 0

    # Handle config subcommand default
    if args.command == "config" and not args.config_command:
        return cmd_config_show(args)

    # Handle providers subcommand default
    if args.command == "providers" and not args.providers_command:
        return cmd_providers_list(args)

    # Execute command
    if hasattr(args, "func"):
        return args.func(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
