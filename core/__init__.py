"""
SoulScript.exe — Core Module
Contains all business logic classes for the emotion-to-magic journal system.
"""

from core.mage import MageIdentity
from core.mood import MoodTracker
from core.spell import Spell, SpellGenerator
from core.spellbook import Spellbook
from core.analyzer import DataAnalyzer

__all__ = [
    "MageIdentity",
    "MoodTracker",
    "Spell",
    "SpellGenerator",
    "Spellbook",
    "DataAnalyzer",
]
