"""
SoulScript.exe — MageIdentity Module
Handles creation, saving, loading, and display of the user's mage profile.
"""

import json
import os
import random
from datetime import datetime


class MageIdentity:
    """Represents the user's mage identity within the SoulScript system.

    Attributes:
        name (str): The mage's chosen name.
        title (str): A randomly assigned fantasy title.
        element (str): The mage's elemental affinity.
        familiar (str): The mage's spirit animal companion.
        creation_date (str): When the mage profile was created.
    """

    PROFILE_PATH = os.path.join("data", "mage_profile.json")
    COMPONENTS_PATH = os.path.join("data", "spell_components.json")

    def __init__(self, name="", title="", element="", familiar="", creation_date=""):
        """Initialize a MageIdentity with given or empty attributes."""
        self.name = name
        self.title = title
        self.element = element
        self.familiar = familiar
        self.creation_date = creation_date

    @classmethod
    def create_new(cls):
        """Interactively create a new mage identity.

        Asks the user for their mage name, then randomly assigns
        a title, element, and familiar from the spell components data.

        Returns:
            MageIdentity: The newly created mage identity.
        """
        print("\n╔══════════════════════════════════════════════════╗")
        print("║          MAGE IDENTITY INITIALIZATION            ║")
        print("╚══════════════════════════════════════════════════╝\n")
        print("The arcane threads gather before you...")
        print("Speak your name, young mage: ", end="")

        name = input().strip()
        if not name:
            name = "Anonymous Mage"

        # Load components for random assignment
        components = cls._load_components()

        # Assign random title
        title = random.choice(components["mage_titles"])

        # Assign random element
        elements = list(components["familiars"].keys())
        element = random.choice(elements)

        # Assign familiar matching the element
        familiar = random.choice(components["familiars"][element])

        # Record creation date
        creation_date = datetime.now().strftime("%Y-%m-%d")

        mage = cls(
            name=name,
            title=title,
            element=element,
            familiar=familiar,
            creation_date=creation_date,
        )

        print(f"\n✦ The arcane threads have woven your identity ✦")
        print(f"  You are now known as {mage.name} {mage.title}")
        print(f"  Element: {mage.element} | Familiar:  {mage.familiar}")

        return mage

    @classmethod
    def load(cls):
        """Load a mage identity from the profile file.

        Returns:
            MageIdentity or None: The loaded identity, or None if no profile exists.
        """
        if not os.path.exists(cls.PROFILE_PATH):
            return None

        try:
            with open(cls.PROFILE_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            return cls(
                name=data.get("name", ""),
                title=data.get("title", ""),
                element=data.get("element", ""),
                familiar=data.get("familiar", ""),
                creation_date=data.get("creation_date", ""),
            )
        except (json.JSONDecodeError, KeyError):
            return None

    def save(self):
        """Save the mage identity to the profile file."""
        os.makedirs(os.path.dirname(self.PROFILE_PATH), exist_ok=True)
        with open(self.PROFILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    def to_dict(self):
        """Serialize the mage identity to a dictionary.

        Returns:
            dict: The mage identity as a dictionary.
        """
        return {
            "name": self.name,
            "title": self.title,
            "element": self.element,
            "familiar": self.familiar,
            "creation_date": self.creation_date,
        }

    def display_title_card(self):
        """Return a formatted string displaying the mage's title card."""
        border = "╔══════════════════════════════════════════════════╗"
        bottom = "╚══════════════════════════════════════════════════╝"
        lines = [
            border,
            "║            ✦ MAGE IDENTITY ✦                     ║",
            "╠══════════════════════════════════════════════════╣",
            f"║  Name:    {self.name:<38} ║",
            f"║  Title:   {self.title:<38} ║",
            f"║  Element: {self.element:<38} ║",
            f"║  Familiar:{self.familiar:<38} ║",
            f"║  Since:   {self.creation_date:<38} ║",
            bottom,
        ]
        return "\n".join(lines)

    def profile_exists(cls=None):
        """Check if a mage profile file already exists.

        Returns:
            bool: True if the profile file exists.
        """
        return os.path.exists(MageIdentity.PROFILE_PATH)

    @classmethod
    def _load_components(cls):
        """Load spell components data from JSON file.

        Returns:
            dict: The spell components data.
        """
        if not os.path.exists(cls.COMPONENTS_PATH):
            return {
                "mage_titles": ["the Wanderer"],
                "familiars": {
                    "Fire": ["Salamander"],
                    "Water": ["Dolphin"],
                    "Earth": ["Tortoise"],
                    "Air": ["Eagle"],
                    "Shadow": ["Black Cat"],
                    "Light": ["Phoenix"],
                    "Void": ["Void Serpent"],
                    "Lightning": ["Thunder Hawk"],
                },
            }

        with open(cls.COMPONENTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def __str__(self):
        """Return a brief string representation of the mage."""
        return f"{self.name} {self.title} — {self.element} Mage with {self.familiar} familiar"
