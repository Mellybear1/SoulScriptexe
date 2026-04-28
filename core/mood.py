"""
SoulScript.exe — MoodTracker Module
Handles mood selection, display, and intensity input for the spell generation system.
"""

import json
import os


class MoodTracker:
    """Manages mood selection and intensity input for spell generation.

    Displays mood categories with example moods, accepts user selection,
    and collects intensity rating on a 1-10 scale.

    Attributes:
        mood_mappings (dict): Loaded mood-to-element mapping data.
        selected_mood (str): The currently selected mood category.
        intensity (int): The mood intensity (1-10).
    """

    MAPPINGS_PATH = os.path.join("data", "mood_mappings.json")

    def __init__(self):
        """Initialize MoodTracker and load mood mappings."""
        self.mood_mappings = self._load_mappings()
        self.selected_mood = ""
        self.intensity = 0

    def _load_mappings(self):
        """Load mood mappings from JSON file.

        Returns:
            dict: The mood mapping data, or a minimal fallback if file not found.
        """
        if not os.path.exists(self.MAPPINGS_PATH):
            return {
                "mood_categories": {
                    "Joyful": {"element": "Air", "example_moods": ["happy", "excited"]},
                    "Melancholy": {"element": "Light", "example_moods": ["sad", "lonely"]},
                    "Angry": {"element": "Fire", "example_moods": ["furious", "irritated"]},
                    "Anxious": {"element": "Water", "example_moods": ["worried", "nervous"]},
                    "Calm": {"element": "Earth", "example_moods": ["peaceful", "serene"]},
                    "Mysterious": {"element": "Shadow", "example_moods": ["curious", "confused"]},
                    "Dark": {"element": "Void", "example_moods": ["hopeless", "bitter"]},
                    "Empowered": {"element": "Lightning", "example_moods": ["confident", "bold"]},
                },
                "intensity_labels": {
                    "1": "Minor Cantrip", "2": "Minor Cantrip", "3": "Minor Cantrip",
                    "4": "Standard Spell", "5": "Standard Spell", "6": "Standard Spell",
                    "7": "Powerful Incantation", "8": "Powerful Incantation",
                    "9": "Powerful Incantation", "10": "Arcane Masterwork",
                },
            }

        with open(self.MAPPINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_categories(self):
        """Return a list of all mood category names.

        Returns:
            list[str]: The mood category names in order.
        """
        return list(self.mood_mappings["mood_categories"].keys())

    def get_element_for_mood(self, mood_category):
        """Get the element associated with a mood category.

        Args:
            mood_category (str): The mood category name.

        Returns:
            str: The associated element, or "Unknown" if not found.
        """
        cat = self.mood_mappings["mood_categories"].get(mood_category, {})
        return cat.get("element", "Unknown")

    def get_intensity_label(self, intensity):
        """Get the descriptive label for a given intensity level.

        Args:
            intensity (int): The intensity level (1-10).

        Returns:
            str: The intensity label (e.g., "Minor Cantrip", "Standard Spell").
        """
        return self.mood_mappings.get("intensity_labels", {}).get(
            str(intensity), "Unknown"
        )

    def display_mood_menu(self):
        """Return a formatted string displaying the mood selection menu.

        Shows each category with its example moods in parentheses.

        Returns:
            str: The formatted mood menu string.
        """
        lines = [
            "",
            "╔══════════════════════════════════════════════════╗",
            "║          What stirs within your soul?            ║",
            "╠══════════════════════════════════════════════════╣",
        ]

        categories = self.get_categories()
        for i, category in enumerate(categories, 1):
            cat_data = self.mood_mappings["mood_categories"][category]
            examples = ", ".join(cat_data["example_moods"])
            element = cat_data["element"]

            # Format: "1. Joyful     (happy, excited, ...) [Air]"
            line = f"║  {i}. {category:<11}({examples})"
            if len(line) > 50:
                # Truncate examples if line is too long
                truncated = examples[:30] + "..."
                line = f"║  {i}. {category:<11}({truncated})"
            lines.append(f"{line:<52}║")
            lines.append(f"║{'':>14}[{element}]{'':<37}║")

        lines.append("╚══════════════════════════════════════════════════╝")
        return "\n".join(lines)

    def get_mood_input(self):
        """Prompt the user to select a mood category.

        Validates input and sets self.selected_mood.

        Returns:
            str: The selected mood category name.
        """
        categories = self.get_categories()
        print(self.display_mood_menu())

        while True:
            try:
                choice = input("\n  Enter the number of your mood: ").strip()
                idx = int(choice)
                if 1 <= idx <= len(categories):
                    self.selected_mood = categories[idx - 1]
                    element = self.get_element_for_mood(self.selected_mood)
                    print(f"\n  ✦ You feel {self.selected_mood} — the {element} stirs within you ✦")
                    return self.selected_mood
                else:
                    print(f"  Please enter a number between 1 and {len(categories)}.")
            except ValueError:
                print("  Please enter a valid number.")

    def get_intensity(self):
        """Prompt the user to set their mood intensity.

        Validates input (1-10) and sets self.intensity.

        Returns:
            int: The selected intensity level.
        """
        print("\n  On a scale of 1-10, how strongly does this mood flow through you?")
        print("  1 = barely a whisper  |  10 = overwhelming torrent")
        print()

        while True:
            try:
                choice = input("  Intensity (1-10): ").strip()
                intensity = int(choice)
                if 1 <= intensity <= 10:
                    self.intensity = intensity
                    label = self.get_intensity_label(intensity)
                    print(f"\n  ✦ Power Level: {intensity}/10 — {label} ✦")
                    return self.intensity
                else:
                    print("  Please enter a number between 1 and 10.")
            except ValueError:
                print("  Please enter a valid number.")

    def get_mood_data(self):
        """Return the complete mood data for the current selection.

        Returns:
            dict: Contains mood, element, intensity, and intensity_label.
        """
        return {
            "mood": self.selected_mood,
            "element": self.get_element_for_mood(self.selected_mood),
            "intensity": self.intensity,
            "intensity_label": self.get_intensity_label(self.intensity),
        }
