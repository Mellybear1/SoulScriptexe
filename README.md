# SoulScript.exe

> *A terminal-themed emotion-to-magic journal system*

SoulScript.exe is a Python application that translates your daily emotional states into magical spells. Part mood tracker, part fantasy spellbook, it transforms how you feel into a structured archive of emotional patterns expressed through a fantasy lens.

## Features

- **Mage Identity System** — Create your own mage profile with name, title, element, and familiar
- **Mood Tracking** — Select from 8 mood categories, each mapped to a fantasy element
- **Spell Generation** — Procedurally generates unique spells based on your mood and its intensity
- **Daily Spell Limit** — One spell per day makes each entry a deliberate reflection
- **Digital Spellbook** — All entries saved to CSV for persistent storage
- **Data Analysis** — Track emotional trends, view frequency distributions, and discover patterns
- **Dual Interface** — Full-featured CLI with rich terminal formatting AND a retro-styled Tkinter GUI

## Mood → Element Mapping

| Mood | Element |
|---|---|
| Joyful | Air |
| Melancholy | Light |
| Angry | Fire |
| Anxious | Water |
| Calm | Earth |
| Mysterious | Shadow |
| Dark | Void |
| Empowered | Lightning |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
# Launch with GUI (default)
python main.py

# Launch with CLI only
python main.py --cli
```

## Project Structure

```
SoulScriptexe/
├── main.py                    # Entry point
├── requirements.txt           # Dependencies
├── README.md                  # This file
├── data/
│   ├── spellbook.csv          # Spell entries
│   ├── mage_profile.json      # Mage identity
│   ├── spell_components.json  # Spell generation data
│   └── mood_mappings.json     # Mood-to-element mappings
├── core/
│   ├── mage.py                # MageIdentity class
│   ├── mood.py                # MoodTracker class
│   ├── spell.py               # Spell & SpellGenerator classes
│   ├── spellbook.py           # Spellbook class (CSV I/O)
│   └── analyzer.py            # DataAnalyzer class
├── ui/
│   ├── terminal.py            # CLI interface
│   ├── gui_app.py             # Tkinter GUI
│   └── ascii_art.py           # ASCII art assets
└── plans/
    ├── soulscript-brainstorm.md
    └── dev-log.md
```

## Python Concepts Demonstrated

- Variables and data types
- Control flow (if/else logic)
- Functions for modular behavior
- Classes and object-oriented design
- File handling (CSV and JSON)
- Data analysis with collections and iteration
- GUI development with Tkinter

## License

This project is for educational purposes.
