"""
SoulScript.exe — Terminal UI Module
The main CLI interface using colorama and rich for polished terminal output.
Provides the interactive menu system for the SoulScript application.
"""

import sys
import time

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from core.mage import MageIdentity
from core.mood import MoodTracker
from core.spell import SpellGenerator
from core.spellbook import Spellbook
from core.analyzer import DataAnalyzer
from ui.ascii_art import (
    TITLE_BANNER, BOOT_MESSAGES, MAIN_MENU, ANALYSIS_MENU,
    SPELLBOOK_MENU, SETTINGS_MENU, ALREADY_CAST_MSG,
    EMPTY_SPELLBOOK_MSG, GOODBYE_MSG, WELCOME_BACK,
    CASTING_FRAMES, ELEMENT_COLORS, DIVIDER_THIN,
)


class TerminalUI:
    """The main CLI interface for SoulScript.exe.

    Manages the interactive menu loop, user input, and display output
    using colorama for colors and rich for advanced formatting.

    Attributes:
        mage (MageIdentity): The current user's mage profile.
        spellbook (Spellbook): The persistent spellbook.
        generator (SpellGenerator): The spell generator.
        analyzer (DataAnalyzer): The data analyzer.
        mood_tracker (MoodTracker): The mood selection handler.
        console (Console): Rich console for advanced output (if available).
    """

    def __init__(self):
        """Initialize the TerminalUI and all core modules."""
        self.mage = None
        self.spellbook = Spellbook()
        self.generator = SpellGenerator()
        self.mood_tracker = MoodTracker()
        self.analyzer = DataAnalyzer(self.spellbook)
        self.console = Console() if HAS_RICH else None

    # ── Color helpers ──────────────────────────────────────

    def _color(self, text, color_code):
        """Apply ANSI color to text if colorama is available.

        Args:
            text (str): The text to colorize.
            color_code (str): ANSI escape code.

        Returns:
            str: The colorized text.
        """
        if HAS_COLORAMA:
            return f"{color_code}{text}{Style.RESET_ALL}"
        return text

    def _element_color(self, text, element):
        """Colorize text based on element type.

        Args:
            text (str): The text to colorize.
            element (str): The element name.

        Returns:
            str: The colorized text.
        """
        color = ELEMENT_COLORS.get(element, "")
        if color and HAS_COLORAMA:
            return f"{color}{text}{Style.RESET_ALL}"
        return text

    # ── Display helpers ────────────────────────────────────

    def _print(self, text="", color=None):
        """Print text, optionally with color.

        Args:
            text (str): The text to print.
            color (str, optional): ANSI color code.
        """
        if color and HAS_COLORAMA:
            print(f"{color}{text}{Style.RESET_ALL}")
        else:
            print(text)

    def _print_slow(self, text, delay=0.03):
        """Print text with a typing animation effect.

        Args:
            text (str): The text to print character by character.
            delay (float): Seconds between each character.
        """
        for char in text:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(delay)
        print()

    def _clear_screen(self):
        """Clear the terminal screen."""
        print("\033[2J\033[H", end="")

    def _pause(self, message="\n  Press Enter to continue..."):
        """Pause and wait for user to press Enter.

        Args:
            message (str): The prompt message.
        """
        input(message)

    # ── Boot sequence ──────────────────────────────────────

    def boot_sequence(self):
        """Run the startup boot sequence with animation."""
        self._clear_screen()

        # Display title banner
        if HAS_COLORAMA:
            print(Fore.CYAN + TITLE_BANNER + Style.RESET_ALL)
        else:
            print(TITLE_BANNER)

        # Animated boot messages
        for msg in BOOT_MESSAGES:
            if HAS_COLORAMA:
                self._print_slow(f"  > {msg}", delay=0.02)
            else:
                print(f"  > {msg}")
            time.sleep(0.3)

        print()

        # Load or create mage profile
        self.mage = MageIdentity.load()
        if self.mage is None:
            self.mage = MageIdentity.create_new()
            self.mage.save()
            print()
            self._print("  ✦ Mage profile saved. ✦", Fore.GREEN)
            time.sleep(1)

        # Show welcome back
        total = self.spellbook.get_total_entries()
        welcome = WELCOME_BACK.format(
            name=self.mage.name,
            title=self.mage.title,
            element=self.mage.element,
            familiar=self.mage.familiar,
            total=total,
            since=self.mage.creation_date,
        )
        self._element_color(welcome.strip(), self.mage.element)
        print(welcome)
        time.sleep(1)

    # ── Main menu loop ─────────────────────────────────────

    def run(self):
        """Run the main application loop."""
        self.boot_sequence()

        while True:
            print(MAIN_MENU)
            choice = input("  Choose an option (1-6): ").strip()

            if choice == "1":
                self._record_mood()
            elif choice == "2":
                self._view_spellbook()
            elif choice == "3":
                self._analyze_trends()
            elif choice == "4":
                self._view_profile()
            elif choice == "5":
                self._settings()
            elif choice == "6":
                print(GOODBYE_MSG)
                break
            else:
                self._print("  Invalid option. Please choose 1-6.", Fore.RED if HAS_COLORAMA else None)

    # ── Feature: Record Mood & Cast Spell ──────────────────

    def _record_mood(self):
        """Handle mood recording and spell generation with daily limit."""
        # Check daily limit
        if self.spellbook.has_entry_for_today():
            print(ALREADY_CAST_MSG)
            today_entry = self.spellbook.get_today_entry()
            if today_entry:
                print("  Today's spell:")
                print(self.spellbook.display_entry(today_entry))
            self._pause()
            return

        # Get mood selection
        mood = self.mood_tracker.get_mood_input()
        intensity = self.mood_tracker.get_intensity()

        # Casting animation
        print()
        for frame in CASTING_FRAMES:
            if HAS_COLORAMA:
                print(Fore.MAGENTA + frame + Style.RESET_ALL)
            else:
                print(frame)
            time.sleep(0.5)

        # Generate spell
        spell = self.generator.generate(mood, intensity)

        # Display spell
        spell_display = str(spell)
        element = spell.element
        if HAS_COLORAMA:
            color = ELEMENT_COLORS.get(element, Fore.WHITE)
            print(f"{color}{spell_display}{Style.RESET_ALL}")
        else:
            print(spell_display)

        # Save to spellbook
        self.spellbook.add_entry(spell, self.mage)
        self._print("\n  ✦ Spell inscribed into your spellbook. ✦",
                     Fore.GREEN if HAS_COLORAMA else None)

        self._pause()

    # ── Feature: View Spellbook ────────────────────────────

    def _view_spellbook(self):
        """Handle spellbook viewing with filter options."""
        while True:
            print(SPELLBOOK_MENU)
            choice = input("  Choose an option (1-7): ").strip()

            if choice == "1":
                self._browse_all()
                break
            elif choice == "2":
                self._filter_by_date()
                break
            elif choice == "3":
                self._filter_by_mood()
                break
            elif choice == "4":
                self._filter_by_element()
                break
            elif choice == "5":
                self._search_keyword()
                break
            elif choice == "6":
                self._view_today()
                break
            elif choice == "7":
                return
            else:
                self._print("  Invalid option.", Fore.RED if HAS_COLORAMA else None)

    def _browse_all(self):
        """Browse all spellbook entries with pagination."""
        for page in self.spellbook.display_all(page_size=3):
            for line in page:
                print(line)
            print(f"\n  {DIVIDER_THIN}")
            cont = input("  Press Enter for next page, or 'q' to go back: ").strip()
            if cont.lower() == "q":
                break
        self._pause()

    def _filter_by_date(self):
        """Filter spellbook entries by date range."""
        print("\n  Enter start date (YYYY-MM-DD): ", end="")
        start = input().strip()
        print("  Enter end date (YYYY-MM-DD): ", end="")
        end = input().strip()

        entries = self.spellbook.get_entries_by_date_range(start, end)
        self._display_entries(entries, f"Entries from {start} to {end}")

    def _filter_by_mood(self):
        """Filter spellbook entries by mood."""
        categories = self.mood_tracker.get_categories()
        print("\n  Select a mood to filter by:")
        for i, cat in enumerate(categories, 1):
            print(f"    {i}. {cat}")

        try:
            idx = int(input("\n  Enter number: ").strip())
            if 1 <= idx <= len(categories):
                mood = categories[idx - 1]
                entries = self.spellbook.get_entries_by_mood(mood)
                self._display_entries(entries, f"Entries with mood: {mood}")
            else:
                self._print("  Invalid selection.", Fore.RED if HAS_COLORAMA else None)
                self._pause()
        except ValueError:
            self._print("  Please enter a valid number.", Fore.RED if HAS_COLORAMA else None)
            self._pause()

    def _filter_by_element(self):
        """Filter spellbook entries by element."""
        elements = ["Fire", "Water", "Earth", "Air", "Shadow", "Light", "Void", "Lightning"]
        print("\n  Select an element to filter by:")
        for i, elem in enumerate(elements, 1):
            print(f"    {i}. {elem}")

        try:
            idx = int(input("\n  Enter number: ").strip())
            if 1 <= idx <= len(elements):
                element = elements[idx - 1]
                entries = self.spellbook.get_entries_by_element(element)
                self._display_entries(entries, f"Entries with element: {element}")
            else:
                self._print("  Invalid selection.", Fore.RED if HAS_COLORAMA else None)
                self._pause()
        except ValueError:
            self._print("  Please enter a valid number.", Fore.RED if HAS_COLORAMA else None)
            self._pause()

    def _search_keyword(self):
        """Search spellbook entries by keyword."""
        print("\n  Enter search keyword: ", end="")
        keyword = input().strip()

        if keyword:
            entries = self.spellbook.search(keyword)
            self._display_entries(entries, f"Search results for: \"{keyword}\"")
        else:
            self._print("  No keyword entered.", Fore.RED if HAS_COLORAMA else None)
            self._pause()

    def _view_today(self):
        """View today's spell entry."""
        entry = self.spellbook.get_today_entry()
        if entry:
            print("\n  ── Today's Spell ──")
            print(self.spellbook.display_entry(entry))
        else:
            print("\n  No spell has been cast today yet.")
        self._pause()

    def _display_entries(self, entries, title):
        """Display a list of entries with a title.

        Args:
            entries (list[dict]): The entries to display.
            title (str): The display title.
        """
        print(f"\n  ── {title} ({len(entries)} found) ──")
        if not entries:
            print("  No entries found.")
        else:
            for i, entry in enumerate(entries, 1):
                print(f"\n  ── Entry {i} ──")
                print(self.spellbook.display_entry(entry))
        self._pause()

    # ── Feature: Analyze Trends ────────────────────────────

    def _analyze_trends(self):
        """Handle the trend analysis menu."""
        print(ANALYSIS_MENU)
        choice = input("  Choose a period (1-4): ").strip()

        period_map = {"1": "week", "2": "month", "3": "all"}
        if choice in period_map:
            period = period_map[choice]
            summary = self.analyzer.display_summary(period)
            print(summary)
            self._pause()
        elif choice == "4":
            return
        else:
            self._print("  Invalid option.", Fore.RED if HAS_COLORAMA else None)
            self._pause()

    # ── Feature: View Mage Profile ────────────────────────

    def _view_profile(self):
        """Display the mage's identity card."""
        if self.mage:
            print(self.mage.display_title_card())
        else:
            self._print("  No mage profile loaded.", Fore.RED if HAS_COLORAMA else None)
        self._pause()

    # ── Feature: Settings ──────────────────────────────────

    def _settings(self):
        """Handle the settings menu."""
        print(SETTINGS_MENU)
        choice = input("  Choose an option (1-3): ").strip()

        if choice == "1":
            self._reset_mage()
        elif choice == "2":
            self._clear_spellbook()
        elif choice == "3":
            return
        else:
            self._print("  Invalid option.", Fore.RED if HAS_COLORAMA else None)

    def _reset_mage(self):
        """Reset the mage profile after confirmation."""
        print("\n  ⚠ This will delete your current mage identity.")
        confirm = input("  Type 'CONFIRM' to proceed: ").strip()
        if confirm == "CONFIRM":
            import os
            profile_path = MageIdentity.PROFILE_PATH
            if os.path.exists(profile_path):
                os.remove(profile_path)
            self._print("  ✦ Mage profile reset. Restart to create a new one. ✦",
                         Fore.GREEN if HAS_COLORAMA else None)
        else:
            print("  Cancelled.")
        self._pause()

    def _clear_spellbook(self):
        """Clear the spellbook after confirmation."""
        print("\n  ⚠ This will delete ALL spellbook entries permanently.")
        confirm = input("  Type 'CONFIRM' to proceed: ").strip()
        if confirm == "CONFIRM":
            import os
            if os.path.exists(self.spellbook.filepath):
                os.remove(self.spellbook.filepath)
            self.spellbook._ensure_file_exists()
            self.spellbook.entries = []
            self._print("  ✦ Spellbook cleared. ✦",
                         Fore.GREEN if HAS_COLORAMA else None)
        else:
            print("  Cancelled.")
        self._pause()
