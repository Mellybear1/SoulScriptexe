"""
SoulScript.exe — ASCII Art Assets
Contains all ASCII art banners, decorations, and visual elements
used throughout the CLI and GUI interfaces.
"""

# Main title banner displayed on startup
TITLE_BANNER = r"""
  █████████     ███████    █████  █████ █████        █████████    █████████  ███████████   █████ ███████████  ███████████                                 
 ███░░░░░███  ███░░░░░███ ░░███  ░░███ ░░███        ███░░░░░███  ███░░░░░███░░███░░░░░███ ░░███ ░░███░░░░░███░█░░░███░░░█                                 
░███    ░░░  ███     ░░███ ░███   ░███  ░███       ░███    ░░░  ███     ░░░  ░███    ░███  ░███  ░███    ░███░   ░███  ░      ██████  █████ █████  ██████ 
░░█████████ ░███      ░███ ░███   ░███  ░███       ░░█████████ ░███          ░██████████   ░███  ░██████████     ░███        ███░░███░░███ ░░███  ███░░███
 ░░░░░░░░███░███      ░███ ░███   ░███  ░███        ░░░░░░░░███░███          ░███░░░░░███  ░███  ░███░░░░░░      ░███       ░███████  ░░░█████░  ░███████ 
 ███    ░███░░███     ███  ░███   ░███  ░███      █ ███    ░███░░███     ███ ░███    ░███  ░███  ░███            ░███       ░███░░░    ███░░░███ ░███░░░  
░░█████████  ░░░███████░   ░░████████   ███████████░░█████████  ░░█████████  █████   █████ █████ █████           █████    ██░░██████  █████ █████░░██████ 
 ░░░░░░░░░     ░░░░░░░      ░░░░░░░░   ░░░░░░░░░░░  ░░░░░░░░░    ░░░░░░░░░  ░░░░░   ░░░░░ ░░░░░ ░░░░░           ░░░░░    ░░  ░░░░░░  ░░░░░ ░░░░░  ░░░░░░  
"""

# Short version for compact displays
TITLE_SHORT = "✦ SoulScript.exe ✦"

# Loading/boot sequence messages
BOOT_MESSAGES = [
    "Initializing arcane subsystem...",
    "Loading elemental matrices...",
    "Calibrating mood sensors...",
    "Compiling spell components...",
    "Establishing connection to the ether...",
    "System ready.",
]

# Divider lines used for section separation
DIVIDER_THIN = "─" * 52
DIVIDER_THICK = "═" * 52
DIVIDER_FANCY = "╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌╌"

# Spell casting animation frames
CASTING_FRAMES = [
    "  ✦ Channeling arcane energy...",
    "  ✦✦ The spell takes shape...",
    "  ✦✦✦ Words of power form...",
    "  ✦✦✦✦ Reality bends to your will...",
    "  ✦✦✦✦✦ The spell is complete! ✦",
]

# Spell already cast today message
ALREADY_CAST_MSG = """
  ╔══════════════════════════════════════════════════╗
  ║     Your daily spell has already been cast.      ║
  ║     Return tomorrow when the mana flows anew.    ║
  ╚══════════════════════════════════════════════════╝
"""

# Empty spellbook message
EMPTY_SPELLBOOK_MSG = """
  ╔══════════════════════════════════════════════════╗
  ║        The spellbook lies empty and dormant.     ║
  ║        Cast your first spell to begin your        ║
  ║        magical archive.                           ║
  ╚══════════════════════════════════════════════════╝
"""

# Goodbye message
GOODBYE_MSG = """
  ╔══════════════════════════════════════════════════╗
  ║        The arcane threads fade into silence...    ║
  ║        Until we meet again, dear mage.            ║
  ╚══════════════════════════════════════════════════╝
"""

# Welcome back message template
WELCOME_BACK = """
  Welcome back, {name} {title}
  Element: {element} | Familiar: {familiar}
  Spells Cast: {total} | Active Since: {since}
"""

# Main menu options
MAIN_MENU = """
╔══════════════════════════════════════════════════╗
║                  MAIN MENU                       ║
╠══════════════════════════════════════════════════╣
║  1. ✦ Record Mood & Cast Spell                   ║
║  2. 📖 View Spellbook                            ║
║  3. 📊 Analyze Trends                            ║
║  4. 🧙 View Mage Profile                         ║
║  5. ⚙️  Settings                                  ║
║  6. 🚪 Exit                                      ║
╚══════════════════════════════════════════════════╝
"""

# Analysis period menu
ANALYSIS_MENU = """
╔══════════════════════════════════════════════════╗
║            ANALYZE EMOTIONAL TRENDS               ║
╠══════════════════════════════════════════════════╣
║  1. Past Week                                    ║
║  2. Past Month                                   ║
║  3. All Time                                     ║
║  4. Back to Main Menu                            ║
╚══════════════════════════════════════════════════╝
"""

# Spellbook view menu
SPELLBOOK_MENU = """
╔══════════════════════════════════════════════════╗
║              VIEW SPELLBOOK                       ║
╠══════════════════════════════════════════════════╣
║  1. Browse All Entries                           ║
║  2. Filter by Date Range                         ║
║  3. Filter by Mood                               ║
║  4. Filter by Element                            ║
║  5. Search by Keyword                            ║
║  6. View Today's Spell                           ║
║  7. Back to Main Menu                            ║
╚══════════════════════════════════════════════════╝
"""

# Settings menu
SETTINGS_MENU = """
╔══════════════════════════════════════════════════╗
║                  SETTINGS                         ║
╠══════════════════════════════════════════════════╣
║  1. Reset Mage Profile                           ║
║  2. Clear Spellbook                              ║
║  3. Back to Main Menu                            ║
╚══════════════════════════════════════════════════╝
"""

# Element symbols for display
ELEMENT_SYMBOLS = {
    "Air": "🌪️",
    "Light": "✨",
    "Fire": "🔥",
    "Water": "🌊",
    "Earth": "🌿",
    "Shadow": "🌑",
    "Void": "🕳️",
    "Lightning": "⚡",
}

# Element colors for terminal display (ANSI codes)
ELEMENT_COLORS = {
    "Air": "\033[96m",       # Cyan
    "Light": "\033[93m",     # Yellow
    "Fire": "\033[91m",      # Red
    "Water": "\033[94m",     # Blue
    "Earth": "\033[92m",     # Green
    "Shadow": "\033[90m",    # Dark gray
    "Void": "\033[95m",      # Magenta
    "Lightning": "\033[97m", # White/Bright
}
