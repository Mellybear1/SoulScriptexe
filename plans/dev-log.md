# SoulScript.exe — Development Log

> A comprehensive record of the design decisions, implementation progress, and technical challenges encountered while building SoulScript.exe. Use this as source material for your class presentation.

---

## Dev Log 0 — Project Brainstorm & Architecture Planning
**Date**: 2026-04-28

### What We Did
- Conducted a full brainstorming session for the SoulScript.exe project
- Defined the project vision: an emotion-to-magic journal system with terminal aesthetics
- Designed the complete architecture including class hierarchy, data models, and UI flows
- Made all key design decisions through collaborative discussion

### Design Decisions Made

#### 1. Mood Input Method
**Decision**: Fixed categories with example moods displayed in parentheses
**Rationale**: Provides clear structure for users while offering enough variety through 8 categories. Easy to implement and map to elements consistently.

**Example display**:
```
1. Joyful     (happy, excited, euphoric, grateful)
2. Melancholy (sad, lonely, nostalgic, grieving)
3. Angry      (furious, irritated, frustrated, resentful)
4. Anxious    (worried, nervous, overwhelmed, restless)
5. Calm       (peaceful, serene, content, relaxed, indifferent)
6. Mysterious (curious, confused, dreamy, wondering)
7. Dark       (hopeless, bitter, vengeful, despairing)
8. Empowered  (confident, determined, passionate, bold)
```

#### 2. Mood-to-Element Mapping
**Decision**: Custom mapping that pairs emotional states with fantasy elements
**Rationale**: The user carefully considered which elements best represent each emotional quality:

| Mood Category | Element | Spell Flavor |
|---|---|---|
| Joyful | Air | Breezy, uplifting, soaring, freedom spells |
| Melancholy | Light | Radiant, bittersweet, luminous, revelation spells |
| Angry | Fire | Destructive, blazing, inferno spells |
| Anxious | Water | Flowing, tidal, turbulent, depth spells |
| Calm | Earth | Grounding, stable, growth, fortress spells |
| Mysterious | Shadow | Shrouded, elusive, whispering, twilight spells |
| Dark | Void | Consuming, vast, empty, eclipse, oblivion spells |
| Empowered | Lightning | Striking, charged, thunder, storm spells |

#### 3. Spell Uniqueness
**Decision**: Weighted random generation + one spell per day limit
**Rationale**: Weighted random ensures variety across sessions while avoiding near-duplicates. The daily limit reinforces the journaling aspect — each spell is a deliberate, once-daily reflection that makes every entry feel special.

**Key mechanic**: Once a spell is logged for the day, the generation option is disabled until midnight. Users can still browse their spellbook and analyze trends.

#### 4. Project Scope
**Decision**: Build CLI and Tkinter GUI together from the start
**Rationale**: Both interfaces share the same core logic, so building them together ensures the architecture stays clean and modular from the beginning.

#### 5. Dependencies
**Decision**: `colorama` + `rich` for CLI, `tkinter` for GUI
**Rationale**: `colorama` handles Windows terminal color compatibility, `rich` provides advanced formatting (tables, panels, progress bars), and `tkinter` is built into Python — no extra install needed for the GUI.

### Architecture Overview

```
SoulScriptexe/
├── main.py                    # Entry point - choose CLI or GUI
├── requirements.txt           # colorama, rich
├── README.md
├── data/
│   ├── spellbook.csv          # Persistent spell/entry storage
│   ├── mage_profile.json      # Saved mage identity
│   ├── spell_components.json  # Spell name parts, incantation words, effects
│   └── mood_mappings.json     # Mood-to-element and mood-to-magic mappings
├── core/
│   ├── __init__.py
│   ├── mage.py                # MageIdentity class
│   ├── mood.py                # MoodTracker class
│   ├── spell.py               # Spell and SpellGenerator classes
│   ├── spellbook.py           # Spellbook - file I/O class
│   └── analyzer.py            # DataAnalyzer class
├── ui/
│   ├── __init__.py
│   ├── terminal.py            # CLI with rich/colorama
│   ├── gui_app.py             # Tkinter GUI
│   └── ascii_art.py           # ASCII art banners
└── plans/
    ├── soulscript-brainstorm.md
    └── dev-log.md             # This file
```

### Core Classes (6 Total)

1. **MageIdentity** — Creates and manages the user's mage profile (name, title, element, familiar)
2. **MoodTracker** — Displays mood menu, accepts and validates mood selection and intensity
3. **Spell** — Data class representing a generated spell with all its properties
4. **SpellGenerator** — Procedurally generates unique spells from mood + intensity using weighted random component assembly
5. **Spellbook** — Manages CSV file I/O, stores entries, checks daily spell limit
6. **DataAnalyzer** — Computes emotional trends, frequency distributions, and summaries

### Implementation Plan (12 Steps)

1. Set up project structure, requirements.txt, and README.md skeleton
2. Create data files (spell_components.json, mood_mappings.json)
3. Implement MageIdentity class with save/load
4. Implement MoodTracker class with category menu
5. Implement Spell and SpellGenerator classes with weighted random
6. Implement Spellbook class with CSV read/write and daily spell check
7. Implement DataAnalyzer class with trend analysis
8. Create ASCII art assets and decorations
9. Build CLI terminal UI with rich/colorama formatting
10. Build Tkinter GUI with retro terminal styling
11. Create main.py entry point with interface selection
12. Testing, polish, and final documentation

### Python Concepts Covered
- Variables and data types
- Control flow (if/else logic)
- Functions for modular behavior
- Classes to structure spells and entries
- File handling (CSV, JSON) for saving and loading data
- Basic data analysis using collections and iteration
- GUI development with Tkinter

---

## Dev Log 1 — Project Setup
**Date**: 2026-04-28

### What We Did
- Created the project directory structure with `core/`, `ui/`, `data/`, and `plans/` directories
- Set up `requirements.txt` with `colorama>=0.4.6` and `rich>=13.0.0`
- Created `README.md` with full project documentation
- Created `core/__init__.py` with imports for all 6 core classes
- Created `ui/__init__.py` as the UI module initializer

### Files Created
- `requirements.txt`
- `README.md`
- `core/__init__.py`
- `ui/__init__.py`

### Challenges & Solutions
- No challenges — straightforward project scaffolding

---

## Dev Log 2 — Data Files & Spell Components
**Date**: 2026-04-28

### What We Did
- Created `data/mood_mappings.json` with 8 mood categories, each mapped to an element with example moods, descriptions, spell flavors, and intensity labels
- Created `data/spell_components.json` with comprehensive component pools for spell generation:
  - 8 prefixes per element (64 total)
  - 24 root words across 3 intensity tiers
  - 8 suffixes per element (64 total)
  - 14 incantation words per element (112 total)
  - 5 effect templates per element (40 total)
  - 18 effect actions across 3 tiers
  - 5-6 durations per tier (16 total)
  - 20 mage titles
  - 5 familiars per element (40 total)

### Files Created
- `data/mood_mappings.json`
- `data/spell_components.json`

### Challenges & Solutions
- Designed the JSON structure to be flat and easy to look up by element name
- Used descriptive keys like "low", "mid", "high" for intensity-based pools

---

## Dev Log 3 — MageIdentity Class
**Date**: 2026-04-28

### What We Did
- Implemented `MageIdentity` class in `core/mage.py`
- Features: create_new() with interactive name input, random title/element/familiar assignment
- save/load using JSON file at `data/mage_profile.json`
- `display_title_card()` returns a formatted box-drawing character card
- Fallback components if data files are missing

### Files Created
- `core/mage.py`

### Key Code Concepts
- **Class methods** (`@classmethod`) for `create_new()` and `load()` — alternative constructors
- **JSON file I/O** with `json.load()` and `json.dump()`
- **Random selection** with `random.choice()` from loaded component pools
- **Date formatting** with `datetime.now().strftime()`

---

## Dev Log 4 — MoodTracker Class
**Date**: 2026-04-28

### What We Did
- Implemented `MoodTracker` class in `core/mood.py`
- Displays mood categories with example moods in parentheses and element labels
- Validates user input for mood selection (1-8) and intensity (1-10)
- Returns mood data as a dictionary for use by SpellGenerator

### Files Created
- `core/mood.py`

### Key Code Concepts
- **Input validation** with try/except for ValueError
- **Dictionary lookups** for mood-to-element mapping
- **Formatted string output** with box-drawing characters

---

## Dev Log 5 — Spell & SpellGenerator Classes
**Date**: 2026-04-28

### What We Did
- Implemented `Spell` data class with name, incantation, element, power_level, duration, effect
- Implemented `SpellGenerator` with **weighted random** component assembly:
  - `_weighted_choice()` assigns 0.1x weight to recently used components, 1.0x to fresh ones
  - Tracks last 3 used components per category to avoid repetition
  - `_build_name()` assembles Prefix + Root + Suffix
  - `_build_incantation()` picks 2-6 words based on intensity tier
  - `_build_effect()` combines templates with mood-specific actions
  - `_determine_duration()` selects from tier-appropriate durations

### Files Created
- `core/spell.py`

### Key Code Concepts
- **Weighted random selection** with `random.choices(weights=...)`
- **Component assembly pattern** — building complex outputs from simple pools
- **Intensity tiers** — mapping 1-10 scale to "low"/"mid"/"high" categories
- **Data class pattern** — Spell holds data, SpellGenerator creates it

### Example Output
```
Spell: EmberRuin Inferno
Element: Fire | Power: 8/10 — Powerful Incantation
Incantation: "Vorax Flammis Caminus Incendium Pyras Ustio!"
Effect: Summons embers from the deep that overwhelms everything in its path
```

---

## Dev Log 6 — Spellbook Class
**Date**: 2026-04-28

### What We Did
- Implemented `Spellbook` class in `core/spellbook.py`
- CSV-based storage with 14 columns per entry
- `has_entry_for_today()` — checks for daily spell limit enforcement
- `get_today_entry()` — retrieves today's spell if it exists
- Filter methods: by date range, mood, element, and keyword search
- Paginated display with `display_all()` generator

### Files Created
- `core/spellbook.py`

### Key Code Concepts
- **CSV file I/O** with `csv.DictReader` and `csv.DictWriter`
- **Date comparison** using string comparison (YYYY-MM-DD format is sortable)
- **Generator pattern** for paginated display (`yield`)
- **Free-text search** iterating over all dictionary values

---

## Dev Log 7 — DataAnalyzer Class
**Date**: 2026-04-28

### What We Did
- Implemented `DataAnalyzer` class in `core/analyzer.py`
- `most_common_mood()` — finds the most frequent mood in a period
- `mood_frequency_distribution()` — counts all moods, sorted by frequency
- `element_distribution()` — counts all elements, sorted by frequency
- `average_power_level()` — calculates mean power level
- `mood_streaks()` — finds consecutive-day streaks of the same mood
- `display_chart()` — generates text-based horizontal bar charts

### Files Created
- `core/analyzer.py`

### Key Code Concepts
- **`collections.Counter`** for frequency counting
- **`datetime` and `timedelta`** for date range filtering
- **List comprehensions** for filtering entries
- **Text-based data visualization** with proportional bar widths

---

## Dev Log 8 — ASCII Art & Visual Assets
**Date**: 2026-04-28

### What We Did
- Created `ui/ascii_art.py` with all visual assets
- Title banner using block characters (█████)
- Boot sequence messages for startup animation
- Casting animation frames (✦ progressively filling)
- Menu templates for main, spellbook, analysis, and settings
- Element symbols (emoji) and ANSI color codes per element
- Special messages: already cast, empty spellbook, goodbye

### Files Created
- `ui/ascii_art.py`

### Key Code Concepts
- **String constants** for reusable UI elements
- **ANSI escape codes** for terminal colors
- **Unicode box-drawing characters** (╔═╗║╚╝╠╣)
- **Emoji integration** for element symbols

---

## Dev Log 9 — CLI Terminal UI
**Date**: 2026-04-28

### What We Did
- Implemented `TerminalUI` class in `ui/terminal.py`
- Boot sequence with animated typing effect
- Main menu loop with 6 options
- Mood recording flow: mood selection → intensity → casting animation → spell display → save
- Daily spell limit check before allowing new casts
- Spellbook viewer with browse, filter, and search
- Analysis viewer with period selection
- Settings: reset mage profile, clear spellbook
- Graceful colorama degradation if not installed

### Files Created
- `ui/terminal.py`

### Key Code Concepts
- **Main loop pattern** with while True and break
- **Optional imports** with try/except for colorama and rich
- **Typing animation** with `sys.stdout.write()` and `time.sleep()`
- **ANSI color integration** with colorama Fore/Style

---

## Dev Log 10 — Tkinter GUI
**Date**: 2026-04-28

### What We Did
- Implemented `SoulScriptGUI` class in `ui/gui_app.py`
- Dark terminal theme: `#0a0a0e` background, `#00ff41` green text, Consolas font
- Layout: title bar → status bar → scrollable text area → button panel
- Mood selection via popup dialog with element-labeled buttons
- Intensity input via `simpledialog.askinteger()`
- Spell display with colored sections (cyan headers, green data, amber highlights)
- Spellbook viewer showing all entries in reverse chronological order
- Analysis viewer with period selection dialog and text-based bar charts
- Settings with confirmation dialogs for destructive operations

### Files Created
- `ui/gui_app.py`

### Key Code Concepts
- **Tkinter widgets**: Tk, Frame, Label, Button, Text, Scrollbar, Toplevel
- **Color theming** with consistent hex color constants
- **Event binding** for hover effects (`<Enter>`, `<Leave>`)
- **Modal dialogs** with `transient()` and `grab_set()`
- **Text widget tags** for colored output sections

---

## Dev Log 11 — Main Entry Point & Integration
**Date**: 2026-04-28

### What We Did
- Created `main.py` as the application entry point
- Command-line argument parsing: `--cli` for CLI mode, `--help` for usage
- Automatic dependency checking with optional auto-install
- Tkinter availability check with graceful CLI fallback
- Windows UTF-8 encoding fix (`sys.stdout.reconfigure(encoding="utf-8")`)
- Ensures `data/` directory exists on startup

### Files Created
- `main.py`

### Challenges & Solutions
- **Challenge**: Windows `cmd.exe` uses cp1252 encoding by default, which can't display Unicode box-drawing characters (╔, ═, ╗, etc.)
- **Solution**: Added `sys.stdout.reconfigure(encoding="utf-8")` at the start of `main()` for Windows systems
- **Challenge**: Tkinter might not be available on all systems
- **Solution**: Wrapped GUI import in try/except and fall back to CLI mode

---

## Dev Log 12 — Testing & Verification
**Date**: 2026-04-28

### What We Did
- Installed dependencies: `colorama 0.4.6` and `rich 15.0.0`
- Verified all core module imports successfully
- Tested spell generation pipeline end-to-end:
  - Generated 5 spells for different moods (Angry, Calm, Joyful, Anxious, Dark)
  - All spells correctly mapped to their elements (Fire, Earth, Air, Water, Void)
  - Power levels correctly set to 5/10 (Standard Spell)
  - Weighted random produced unique spell names for each mood
- Tested CSV storage: entries saved and loaded correctly
- Tested daily spell limit: `has_entry_for_today()` returned True after adding entries
- Tested analyzer: mood distribution, element distribution, average power all correct
- Tested keyword search: found matching entries

### Test Results
```
[Fire] VulcanDrift Eruption (Power: 5/10 — Standard Spell)
[Earth] RootEcho Bastion (Power: 5/10 — Standard Spell)
[Air] AeroWave Breeze (Power: 5/10 — Standard Spell)
[Water] FathomSurge Depth (Power: 5/10 — Standard Spell)
[Void] ChasmFlare Rift (Power: 5/10 — Standard Spell)

Total entries: 5
Has entry for today: True
Most common mood: ('Angry', 1)
Avg power: 5.0
✓ All tests passed!
```

---

## Presentation Tips

### Suggested Slide Outline
1. **Title Slide** — SoulScript.exe: Emotion-to-Magic Journal System
2. **Project Vision** — What is SoulScript.exe? (the core concept)
3. **Design Process** — Brainstorming session, architecture diagrams
4. **Architecture** — File structure, class hierarchy diagram
5. **Core Features** — Mood tracking, spell generation, spellbook, analysis
6. **Mood-to-Magic System** — The mapping table, how spells are generated
7. **Daily Spell Mechanic** — One spell per day, the journaling philosophy
8. **Code Highlights** — Key Python concepts demonstrated
9. **CLI Demo** — Screenshots of the terminal interface
10. **GUI Demo** — Screenshots of the Tkinter interface
11. **Challenges & Solutions** — Technical hurdles overcome
12. **Future Enhancements** — What could be added next
13. **Q&A**

### Key Talking Points
- This project demonstrates OOP principles (6 classes with clear responsibilities)
- File I/O with both CSV and JSON formats
- Data analysis using Python collections module
- GUI development with Tkinter
- Creative coding: merging emotional journaling with fantasy storytelling
