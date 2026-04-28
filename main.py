#!/usr/bin/env python3
"""
SoulScript.exe — Entry Point
Launches the SoulScript application in either GUI or CLI mode.

Usage:
    python main.py          # Launch with GUI (default)
    python main.py --cli    # Launch with CLI only
    python main.py --help   # Show help message
"""

import sys
import os


def print_help():
    """Print the help message."""
    print("""
╔══════════════════════════════════════════════════╗
║              SoulScript.exe v1.0                  ║
║       Emotion-to-Magic Journal System             ║
╠══════════════════════════════════════════════════╣
║                                                  ║
║  Usage:                                          ║
║    python main.py          Launch GUI (default)  ║
║    python main.py --cli    Launch CLI only       ║
║    python main.py --help   Show this message     ║
║                                                  ║
╚══════════════════════════════════════════════════╝
""")


def check_dependencies():
    """Check that required dependencies are installed.

    Returns:
        list[str]: List of missing package names.
    """
    missing = []
    try:
        import colorama
    except ImportError:
        missing.append("colorama")

    try:
        import rich
    except ImportError:
        missing.append("rich")

    return missing


def install_dependencies():
    """Offer to install missing dependencies."""
    missing = check_dependencies()
    if not missing:
        return True

    print(f"  Missing dependencies: {', '.join(missing)}")
    print(f"  Install them with: pip install {' '.join(missing)}")
    print()

    choice = input("  Would you like to install them now? (y/n): ").strip().lower()
    if choice == "y":
        import subprocess
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install"] + missing
            )
            print("\n  ✦ Dependencies installed successfully. ✦\n")
            return True
        except subprocess.CalledProcessError:
            print("\n  ✗ Failed to install dependencies. Please install manually.")
            return False
    else:
        print("  Continuing without optional dependencies (some features may be limited).\n")
        return True


def main():
    """Main entry point for SoulScript.exe."""
    # Fix Windows UTF-8 encoding for Unicode characters
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
            sys.stderr.reconfigure(encoding="utf-8")
        except (AttributeError, OSError):
            pass

    # Parse command line arguments
    args = sys.argv[1:]

    if "--help" in args or "-h" in args:
        print_help()
        return

    use_cli = "--cli" in args

    # Ensure we're in the right directory for relative paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)

    # Check and optionally install dependencies
    if not install_dependencies():
        return

    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)

    if use_cli:
        # Launch CLI mode
        from ui.terminal import TerminalUI
        app = TerminalUI()
        app.run()
    else:
        # Launch GUI mode (default)
        try:
            import tkinter as tk  # noqa: F401 — check if Tkinter is available
            from ui.gui_app import SoulScriptGUI
            app = SoulScriptGUI()
            app.run()
        except (ImportError, Exception):
            print("  ✗ Tkinter is not available on this system.")
            print("  Falling back to CLI mode...\n")
            from ui.terminal import TerminalUI
            app = TerminalUI()
            app.run()


if __name__ == "__main__":
    main()
