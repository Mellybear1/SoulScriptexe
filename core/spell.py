"""
SoulScript.exe — Spell & SpellGenerator Module
Contains the Spell data class and the SpellGenerator that procedurally
creates unique spells from mood and intensity using weighted random selection.
"""

import json
import os
import random
from datetime import datetime


class Spell:
    """Represents a generated spell with all its magical properties.

    Attributes:
        name (str): The generated spell name.
        incantation (str): The spoken words to cast the spell.
        element (str): The elemental affinity of the spell.
        power_level (int): The spell's power (1-10).
        power_tier (str): Descriptive power tier label.
        duration (str): How long the spell lasts.
        effect (str): What the spell does.
        mood_source (str): The mood that generated this spell.
        timestamp (str): When the spell was created.
    """

    def __init__(self, name, incantation, element, power_level, power_tier,
                 duration, effect, mood_source, timestamp=None):
        """Initialize a Spell with all its attributes."""
        self.name = name
        self.incantation = incantation
        self.element = element
        self.power_level = power_level
        self.power_tier = power_tier
        self.duration = duration
        self.effect = effect
        self.mood_source = mood_source
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """Serialize the spell to a dictionary for CSV storage.

        Returns:
            dict: The spell data as a flat dictionary.
        """
        return {
            "timestamp": self.timestamp,
            "spell_name": self.name,
            "incantation": self.incantation,
            "element": self.element,
            "power_level": self.power_level,
            "power_tier": self.power_tier,
            "duration": self.duration,
            "effect": self.effect,
            "mood_source": self.mood_source,
        }

    def display_short(self):
        """Return a one-line summary of the spell.

        Returns:
            str: Abbreviated spell display.
        """
        return f"[{self.element}] {self.name} (Power: {self.power_level}/10 — {self.power_tier})"

    def __str__(self):
        """Return the full formatted spell display.

        Returns:
            str: The complete spell card with all details.
        """
        lines = [
            "",
            "╔══════════════════════════════════════════════════╗",
            "║              ✦ SPELL GENERATED ✦                 ║",
            "╠══════════════════════════════════════════════════╣",
            f"║  Spell:    {self.name:<38} ║",
            f"║  Element:  {self.element:<38} ║",
            f"║  Power:    {self.power_level}/10 — {self.power_tier:<27} ║",
            f"║  Duration: {self.duration:<38} ║",
            f"║  Mood:     {self.mood_source:<38} ║",
            "╠══════════════════════════════════════════════════╣",
            f"║  \"{self.incantation}\"",
            "╠══════════════════════════════════════════════════╣",
            f"║  Effect: {self.effect:<40} ║",
            "╚══════════════════════════════════════════════════╝",
        ]
        return "\n".join(lines)


class SpellGenerator:
    """Procedurally generates unique spells from mood and intensity data.

    Uses weighted random selection from component pools, deprioritizing
    recently used components to ensure variety across sessions.

    Attributes:
        components (dict): Loaded spell component data.
        mood_mappings (dict): Loaded mood-to-element mapping data.
        recent_components (dict): Tracks recently used components for weighting.
    """

    COMPONENTS_PATH = os.path.join("data", "spell_components.json")
    MAPPINGS_PATH = os.path.join("data", "mood_mappings.json")
    MAX_RECENT = 3  # Number of recent items to deprioritize per category

    def __init__(self):
        """Initialize SpellGenerator and load all component data."""
        self.components = self._load_components()
        self.mood_mappings = self._load_mappings()
        self.recent_components = {
            "prefixes": [],
            "roots": [],
            "suffixes": [],
            "incantation_words": [],
            "effect_actions": [],
        }

    def _load_components(self):
        """Load spell components from JSON file.

        Returns:
            dict: The spell components data.
        """
        if not os.path.exists(self.COMPONENTS_PATH):
            return self._default_components()

        with open(self.COMPONENTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def _load_mappings(self):
        """Load mood mappings from JSON file.

        Returns:
            dict: The mood mapping data.
        """
        if not os.path.exists(self.MAPPINGS_PATH):
            return {}

        with open(self.MAPPINGS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def _default_components():
        """Return minimal fallback components if data file is missing.

        Returns:
            dict: A minimal set of spell components.
        """
        return {
            "prefixes": {"Fire": ["Pyro"], "Water": ["Aqua"], "Earth": ["Terra"],
                         "Air": ["Aero"], "Shadow": ["Umbral"], "Light": ["Lumi"],
                         "Void": ["Null"], "Lightning": ["Volt"]},
            "roots": {"low": ["Whisper"], "mid": ["Surge"], "high": ["Fury"]},
            "suffixes": {"Fire": ["Blaze"], "Water": ["Tide"], "Earth": ["Wall"],
                         "Air": ["Gust"], "Shadow": ["Shroud"], "Light": ["Ray"],
                         "Void": ["Rift"], "Lightning": ["Strike"]},
            "incantation_words": {"Fire": ["ignis"], "Water": ["aqua"],
                                  "Earth": ["terra"], "Air": ["ventis"],
                                  "Shadow": ["umbrae"], "Light": ["luminis"],
                                  "Void": ["vacui"], "Lightning": ["fulguris"]},
            "effect_templates": {"Fire": ["Channels fire, {effect}"],
                                 "Water": ["Channels water, {effect}"],
                                 "Earth": ["Channels earth, {effect}"],
                                 "Air": ["Channels air, {effect}"],
                                 "Shadow": ["Channels shadow, {effect}"],
                                 "Light": ["Channels light, {effect}"],
                                 "Void": ["Channels the void, {effect}"],
                                 "Lightning": ["Channels lightning, {effect}"]},
            "effect_actions": {"low": ["creates a faint shimmer"],
                               "mid": ["strikes with focused precision"],
                               "high": ["unleashes devastating force"]},
            "durations": {"low": ["a fleeting moment"],
                          "mid": ["three turns of the hourglass"],
                          "high": ["until the stars realign"]},
        }

    def _weighted_choice(self, pool, recent_key):
        """Select a random item from pool, deprioritizing recently used items.

        Items that appear in the recent list for the given key get a lower
        weight (0.1x), making them unlikely to be selected again soon.

        Args:
            pool (list): The list of items to choose from.
            recent_key (str): The key in recent_components to check against.

        Returns:
            The selected item from the pool.
        """
        recent = self.recent_components.get(recent_key, [])

        if not recent or len(pool) <= len(recent):
            choice = random.choice(pool)
        else:
            # Assign weights: 1.0 for fresh items, 0.1 for recently used
            weights = []
            for item in pool:
                if item in recent:
                    weights.append(0.1)
                else:
                    weights.append(1.0)

            choice = random.choices(pool, weights=weights, k=1)[0]

        # Track this choice as recent
        if recent_key in self.recent_components:
            self.recent_components[recent_key].append(choice)
            # Keep only the last MAX_RECENT items
            if len(self.recent_components[recent_key]) > self.MAX_RECENT:
                self.recent_components[recent_key] = \
                    self.recent_components[recent_key][-self.MAX_RECENT:]

        return choice

    def _get_intensity_tier(self, intensity):
        """Map intensity value to a tier label.

        Args:
            intensity (int): The intensity level (1-10).

        Returns:
            str: "low", "mid", or "high".
        """
        if intensity <= 3:
            return "low"
        elif intensity <= 6:
            return "mid"
        else:
            return "high"

    def _build_name(self, element, intensity):
        """Generate a spell name from prefix + root + suffix.

        Args:
            element (str): The spell's element.
            intensity (int): The mood intensity.

        Returns:
            str: The generated spell name.
        """
        tier = self._get_intensity_tier(intensity)

        prefix = self._weighted_choice(
            self.components["prefixes"].get(element, ["Arcane"]), "prefixes"
        )
        root = self._weighted_choice(
            self.components["roots"].get(tier, ["Spell"]), "roots"
        )
        suffix = self._weighted_choice(
            self.components["suffixes"].get(element, ["Bolt"]), "suffixes"
        )

        return f"{prefix}{root} {suffix}"

    def _build_incantation(self, element, intensity):
        """Generate an incantation from element-specific word pools.

        Args:
            element (str): The spell's element.
            intensity (int): The mood intensity.

        Returns:
            str: The generated incantation string.
        """
        word_pool = self.components["incantation_words"].get(element, ["arcana"])
        tier = self._get_intensity_tier(intensity)

        # Number of words based on intensity
        if tier == "low":
            num_words = random.randint(2, 3)
        elif tier == "mid":
            num_words = random.randint(3, 4)
        else:
            num_words = random.randint(4, 6)

        words = [self._weighted_choice(word_pool, "incantation_words")
                 for _ in range(num_words)]

        # Capitalize first letter of each word and add exclamation
        incantation = " ".join(w.capitalize() for w in words) + "!"

        return incantation

    def _build_effect(self, element, intensity):
        """Generate a spell effect description.

        Args:
            element (str): The spell's element.
            intensity (int): The mood intensity.

        Returns:
            str: The generated effect description.
        """
        tier = self._get_intensity_tier(intensity)

        template = random.choice(
            self.components["effect_templates"].get(element, ["{effect}"])
        )
        action = self._weighted_choice(
            self.components["effect_actions"].get(tier, ["does something mysterious"]),
            "effect_actions",
        )

        return template.format(effect=action)

    def _determine_duration(self, intensity):
        """Determine spell duration based on power level.

        Args:
            intensity (int): The mood intensity.

        Returns:
            str: The duration description.
        """
        tier = self._get_intensity_tier(intensity)
        durations = self.components["durations"].get(tier, ["a fleeting moment"])
        return random.choice(durations)

    def generate(self, mood_category, intensity):
        """Generate a complete spell from mood and intensity.

        This is the main entry point for spell generation. It orchestrates
        all the component assembly and returns a fully formed Spell object.

        Args:
            mood_category (str): The selected mood category.
            intensity (int): The mood intensity (1-10).

        Returns:
            Spell: The generated spell.
        """
        # Determine element from mood
        cat_data = self.mood_mappings.get("mood_categories", {}).get(mood_category, {})
        element = cat_data.get("element", "Arcane")

        # Get intensity label
        intensity_label = self.mood_mappings.get("intensity_labels", {}).get(
            str(intensity), "Unknown Spell"
        )

        # Build spell components
        name = self._build_name(element, intensity)
        incantation = self._build_incantation(element, intensity)
        effect = self._build_effect(element, intensity)
        duration = self._determine_duration(intensity)

        return Spell(
            name=name,
            incantation=incantation,
            element=element,
            power_level=intensity,
            power_tier=intensity_label,
            duration=duration,
            effect=effect,
            mood_source=mood_category,
        )
