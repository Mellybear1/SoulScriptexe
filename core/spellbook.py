"""
SoulScript.exe — Spellbook Module
Handles persistent storage of spell entries in CSV format,
including the daily spell limit check and entry retrieval.
"""

import csv
import os
from datetime import datetime


class Spellbook:
    """Manages the persistent spellbook stored as a CSV file.

    Provides methods for adding entries, loading all entries,
    checking the daily spell limit, and searching/filtering entries.

    Attributes:
        filepath (str): Path to the spellbook CSV file.
        entries (list[dict]): In-memory cache of all spellbook entries.
    """

    CSV_HEADERS = [
        "date", "time", "mage_name", "mage_title", "element",
        "mood", "mood_category", "intensity", "spell_name",
        "incantation", "power_level", "power_tier", "duration", "effect",
    ]

    def __init__(self, filepath=None):
        """Initialize the Spellbook.

        Args:
            filepath (str, optional): Path to the CSV file.
                Defaults to "data/spellbook.csv".
        """
        self.filepath = filepath or os.path.join("data", "spellbook.csv")
        self.entries = []
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        """Create the CSV file with headers if it doesn't exist."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        if not os.path.exists(self.filepath):
            with open(self.filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=self.CSV_HEADERS)
                writer.writeheader()

    def load_all(self):
        """Read the entire CSV file into memory.

        Returns:
            list[dict]: All spellbook entries.
        """
        self.entries = []

        if not os.path.exists(self.filepath):
            return self.entries

        try:
            with open(self.filepath, "r", newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    self.entries.append(dict(row))
        except (csv.Error, OSError):
            pass

        return self.entries

    def add_entry(self, spell, mage):
        """Add a new spell entry to the spellbook.

        Combines spell data with mage data and writes to the CSV file.

        Args:
            spell (Spell): The generated spell object.
            mage (MageIdentity): The mage who cast the spell.

        Returns:
            dict: The entry that was added.
        """
        now = datetime.now()
        entry = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "mage_name": mage.name,
            "mage_title": mage.title,
            "element": spell.element,
            "mood": spell.mood_source,
            "mood_category": spell.mood_source,
            "intensity": str(spell.power_level),
            "spell_name": spell.name,
            "incantation": spell.incantation,
            "power_level": str(spell.power_level),
            "power_tier": spell.power_tier,
            "duration": spell.duration,
            "effect": spell.effect,
        }

        # Append to file
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.CSV_HEADERS)
            writer.writerow(entry)

        # Update in-memory cache
        self.entries.append(entry)
        return entry

    def has_entry_for_today(self):
        """Check if a spell has already been cast today.

        Returns:
            bool: True if an entry exists with today's date.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        self.load_all()

        for entry in self.entries:
            if entry.get("date") == today:
                return True
        return False

    def get_today_entry(self):
        """Get today's spell entry if it exists.

        Returns:
            dict or None: Today's entry, or None if not found.
        """
        today = datetime.now().strftime("%Y-%m-%d")
        self.load_all()

        for entry in self.entries:
            if entry.get("date") == today:
                return entry
        return None

    def get_entries_by_date_range(self, start_date, end_date):
        """Get entries within a date range (inclusive).

        Args:
            start_date (str): Start date in YYYY-MM-DD format.
            end_date (str): End date in YYYY-MM-DD format.

        Returns:
            list[dict]: Entries within the date range.
        """
        self.load_all()
        results = []
        for entry in self.entries:
            entry_date = entry.get("date", "")
            if start_date <= entry_date <= end_date:
                results.append(entry)
        return results

    def get_entries_by_mood(self, mood):
        """Get all entries matching a specific mood category.

        Args:
            mood (str): The mood category to filter by.

        Returns:
            list[dict]: Entries matching the mood.
        """
        self.load_all()
        return [e for e in self.entries if e.get("mood_category", "").lower() == mood.lower()]

    def get_entries_by_element(self, element):
        """Get all entries matching a specific element.

        Args:
            element (str): The element to filter by.

        Returns:
            list[dict]: Entries matching the element.
        """
        self.load_all()
        return [e for e in self.entries if e.get("element", "").lower() == element.lower()]

    def search(self, keyword):
        """Free-text search across all entry fields.

        Args:
            keyword (str): The search term.

        Returns:
            list[dict]: Entries containing the keyword in any field.
        """
        self.load_all()
        keyword_lower = keyword.lower()
        results = []
        for entry in self.entries:
            for value in entry.values():
                if keyword_lower in str(value).lower():
                    results.append(entry)
                    break
        return results

    def get_total_entries(self):
        """Get the total number of entries in the spellbook.

        Returns:
            int: The total entry count.
        """
        self.load_all()
        return len(self.entries)

    def display_entry(self, entry):
        """Return a formatted string for a single spellbook entry.

        Args:
            entry (dict): The spellbook entry to display.

        Returns:
            str: The formatted entry display.
        """
        lines = [
            f"  Date: {entry.get('date', 'Unknown')} at {entry.get('time', 'Unknown')}",
            f"  Mage: {entry.get('mage_name', 'Unknown')} {entry.get('mage_title', '')}",
            f"  Mood: {entry.get('mood', 'Unknown')} ({entry.get('element', 'Unknown')})",
            f"  Spell: {entry.get('spell_name', 'Unknown')}",
            f"  Power: {entry.get('power_level', '?')}/10 — {entry.get('power_tier', '')}",
            f"  Duration: {entry.get('duration', 'Unknown')}",
            f"  Incantation: \"{entry.get('incantation', '')}\"",
            f"  Effect: {entry.get('effect', 'Unknown')}",
        ]
        return "\n".join(lines)

    def display_all(self, page_size=5):
        """Generator that yields pages of entries for paginated display.

        Args:
            page_size (int): Number of entries per page.

        Yields:
            list[str]: A page of formatted entry strings.
        """
        self.load_all()

        if not self.entries:
            yield ["  The spellbook is empty. No spells have been cast yet."]
            return

        for i in range(0, len(self.entries), page_size):
            page = self.entries[i:i + page_size]
            page_lines = []
            for j, entry in enumerate(page, 1):
                page_lines.append(f"\n  ── Entry {i + j} of {len(self.entries)} ──")
                page_lines.append(self.display_entry(entry))
            yield page_lines
