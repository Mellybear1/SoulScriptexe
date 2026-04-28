"""
SoulScript.exe — Tkinter GUI Module
A retro terminal-styled graphical interface for SoulScript.exe.
Provides the same functionality as the CLI but with buttons, text areas,
and scrollable panels in a dark-themed window.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime

from core.mage import MageIdentity
from core.mood import MoodTracker
from core.spell import SpellGenerator
from core.spellbook import Spellbook
from core.analyzer import DataAnalyzer
from ui.ascii_art import TITLE_BANNER, ELEMENT_SYMBOLS


class SoulScriptGUI:
    """The Tkinter GUI application for SoulScript.exe.

    Styled to resemble a retro terminal with dark background,
    green monospace text, and a fantasy-themed layout.

    Attributes:
        root (tk.Tk): The main application window.
        mage (MageIdentity): The current user's mage profile.
        spellbook (Spellbook): The persistent spellbook.
        generator (SpellGenerator): The spell generator.
        analyzer (DataAnalyzer): The data analyzer.
        mood_tracker (MoodTracker): The mood selection handler.
    """

    # ── Color Scheme ───────────────────────────────────────
    BG_DARK = "#0a0a0e"
    BG_PANEL = "#12121a"
    BG_BUTTON = "#1a1a2e"
    BG_BUTTON_HOVER = "#2a2a4e"
    FG_GREEN = "#00ff41"
    FG_AMBER = "#ffb000"
    FG_CYAN = "#00d4ff"
    FG_RED = "#ff4444"
    FG_WHITE = "#e0e0e0"
    FG_DIM = "#666680"
    FONT_MONO = ("Consolas", 11)
    FONT_MONO_BOLD = ("Consolas", 11, "bold")
    FONT_TITLE = ("Consolas", 16, "bold")
    FONT_SMALL = ("Consolas", 9)

    def __init__(self):
        """Initialize the GUI application and all core modules."""
        self.root = tk.Tk()
        self.root.title("SoulScript.exe")
        self.root.geometry("800x650")
        self.root.configure(bg=self.BG_DARK)
        self.root.resizable(True, True)
        self.root.minsize(700, 550)

        # Core modules
        self.mage = None
        self.spellbook = Spellbook()
        self.generator = SpellGenerator()
        self.mood_tracker = MoodTracker()
        self.analyzer = DataAnalyzer(self.spellbook)

        # Load or create mage
        self.mage = MageIdentity.load()
        if self.mage is None:
            self.mage = MageIdentity.create_new()
            self.mage.save()

        # Build the UI
        self._build_ui()
        self._refresh_status()

    def _build_ui(self):
        """Construct the main application layout."""
        # ── Top: Title Banner ──────────────────────────────
        self.frame_top = tk.Frame(self.root, bg=self.BG_DARK)
        self.frame_top.pack(fill="x", padx=10, pady=(10, 0))

        self.label_title = tk.Label(
            self.frame_top, text="✦ SoulScript.exe ✦",
            font=self.FONT_TITLE, fg=self.FG_GREEN, bg=self.BG_DARK,
        )
        self.label_title.pack()

        # ── Status Bar ─────────────────────────────────────
        self.frame_status = tk.Frame(self.root, bg=self.BG_PANEL, bd=1, relief="sunken")
        self.frame_status.pack(fill="x", padx=10, pady=5)

        self.label_status = tk.Label(
            self.frame_status, text="",
            font=self.FONT_SMALL, fg=self.FG_AMBER, bg=self.BG_PANEL, anchor="w",
        )
        self.label_status.pack(fill="x", padx=8, pady=3)

        # ── Main Content Area ──────────────────────────────
        self.frame_content = tk.Frame(self.root, bg=self.BG_DARK)
        self.frame_content.pack(fill="both", expand=True, padx=10, pady=5)

        # Text display area with scrollbar
        self.text_frame = tk.Frame(self.frame_content, bg=self.BG_PANEL, bd=1, relief="sunken")
        self.text_frame.pack(fill="both", expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.text_output = tk.Text(
            self.text_frame,
            font=self.FONT_MONO, fg=self.FG_GREEN, bg=self.BG_PANEL,
            insertbackground=self.FG_GREEN, selectbackground=self.BG_BUTTON_HOVER,
            wrap="word", state="disabled", cursor="arrow",
            yscrollcommand=self.scrollbar.set,
        )
        self.text_output.pack(fill="both", expand=True, padx=2, pady=2)
        self.scrollbar.config(command=self.text_output.yview)

        # ── Button Panel ───────────────────────────────────
        self.frame_buttons = tk.Frame(self.root, bg=self.BG_DARK)
        self.frame_buttons.pack(fill="x", padx=10, pady=(5, 10))

        buttons = [
            ("✦ Cast Spell", self._on_cast_spell),
            ("📖 Spellbook", self._on_view_spellbook),
            ("📊 Analyze", self._on_analyze),
            ("🧙 Profile", self._on_view_profile),
            ("⚙ Settings", self._on_settings),
        ]

        for text, command in buttons:
            btn = tk.Button(
                self.frame_buttons, text=text,
                font=self.FONT_MONO, fg=self.FG_GREEN, bg=self.BG_BUTTON,
                activebackground=self.BG_BUTTON_HOVER, activeforeground=self.FG_CYAN,
                bd=0, padx=12, pady=6, cursor="hand2",
                command=command,
            )
            btn.pack(side="left", padx=3, expand=True, fill="x")
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.BG_BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.BG_BUTTON))

    # ── Text Output Helpers ────────────────────────────────

    def _clear_output(self):
        """Clear the text output area."""
        self.text_output.config(state="normal")
        self.text_output.delete("1.0", "end")
        self.text_output.config(state="disabled")

    def _append_output(self, text, color=None):
        """Append text to the output area, optionally with a color tag.

        Args:
            text (str): The text to append.
            color (str, optional): Foreground color for the text.
        """
        self.text_output.config(state="normal")

        if color:
            tag_name = f"color_{color}"
            self.text_output.tag_configure(tag_name, foreground=color)
            self.text_output.insert("end", text, tag_name)
        else:
            self.text_output.insert("end", text)

        self.text_output.see("end")
        self.text_output.config(state="disabled")

    def _display(self, text, color=None):
        """Clear and display text in the output area.

        Args:
            text (str): The text to display.
            color (str, optional): Foreground color.
        """
        self._clear_output()
        self._append_output(text, color)

    def _refresh_status(self):
        """Update the status bar with current mage info."""
        if self.mage:
            total = self.spellbook.get_total_entries()
            today_status = "✦ Spell cast today" if self.spellbook.has_entry_for_today() else "○ No spell today"
            status = (
                f"  {self.mage.name} {self.mage.title}  │  "
                f"Element: {self.mage.element}  │  Familiar: {self.mage.familiar}  │  "
                f"Spells: {total}  │  {today_status}"
            )
            self.label_status.config(text=status)

    # ── Button Handlers ────────────────────────────────────

    def _on_cast_spell(self):
        """Handle the Cast Spell button — opens mood selection dialog."""
        # Check daily limit
        if self.spellbook.has_entry_for_today():
            self._display(
                "\n  Your daily spell has already been cast.\n"
                "  Return tomorrow when the mana flows anew.\n\n",
                self.FG_AMBER,
            )
            today_entry = self.spellbook.get_today_entry()
            if today_entry:
                self._append_entry(today_entry)
            return

        self._show_mood_dialog()

    def _show_mood_dialog(self):
        """Show a dialog for mood and intensity selection."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Record Your Mood")
        dialog.geometry("500x450")
        dialog.configure(bg=self.BG_DARK)
        dialog.transient(self.root)
        dialog.grab_set()

        # Title
        tk.Label(
            dialog, text="What stirs within your soul?",
            font=self.FONT_TITLE, fg=self.FG_GREEN, bg=self.BG_DARK,
        ).pack(pady=(15, 10))

        # Mood buttons
        mood_frame = tk.Frame(dialog, bg=self.BG_DARK)
        mood_frame.pack(fill="both", expand=True, padx=20, pady=5)

        categories = self.mood_tracker.get_categories()
        self._selected_mood = tk.StringVar()

        for i, category in enumerate(categories):
            cat_data = self.mood_tracker.mood_mappings["mood_categories"][category]
            examples = ", ".join(cat_data["example_moods"])
            element = cat_data["element"]

            btn = tk.Button(
                mood_frame,
                text=f"{category} ({examples}) [{element}]",
                font=self.FONT_SMALL, fg=self.FG_GREEN, bg=self.BG_BUTTON,
                activebackground=self.BG_BUTTON_HOVER, activeforeground=self.FG_CYAN,
                bd=0, pady=8, cursor="hand2",
                command=lambda c=category: self._select_mood(c, dialog),
            )
            btn.pack(fill="x", pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.BG_BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.BG_BUTTON))

    def _select_mood(self, mood, mood_dialog):
        """Handle mood selection and show intensity slider.

        Args:
            mood (str): The selected mood category.
            mood_dialog (tk.Toplevel): The mood dialog to close.
        """
        mood_dialog.destroy()

        # Show intensity dialog
        intensity = simpledialog.askinteger(
            "Mood Intensity",
            f"You feel {mood}.\n\nOn a scale of 1-10, how strongly?\n(1 = whisper  |  10 = torrent)",
            parent=self.root, minvalue=1, maxvalue=10,
        )

        if intensity is None:
            return  # User cancelled

        # Generate spell
        spell = self.generator.generate(mood, intensity)

        # Display spell
        self._display_spell(spell)

        # Save to spellbook
        self.spellbook.add_entry(spell, self.mage)
        self._refresh_status()

    def _display_spell(self, spell):
        """Display a generated spell in the output area.

        Args:
            spell (Spell): The spell to display.
        """
        self._clear_output()

        self._append_output("\n  ══════════════════════════════════════════════════\n", self.FG_DIM)
        self._append_output("              ✦ SPELL GENERATED ✦\n", self.FG_CYAN)
        self._append_output("  ══════════════════════════════════════════════════\n", self.FG_DIM)
        self._append_output(f"\n  Spell:    {spell.name}\n", self.FG_GREEN)
        self._append_output(f"  Element:  {spell.element}\n", self.FG_AMBER)
        self._append_output(f"  Power:    {spell.power_level}/10 — {spell.power_tier}\n", self.FG_GREEN)
        self._append_output(f"  Duration: {spell.duration}\n", self.FG_GREEN)
        self._append_output(f"  Mood:     {spell.mood_source}\n", self.FG_GREEN)
        self._append_output("\n  ══════════════════════════════════════════════════\n", self.FG_DIM)
        self._append_output(f'  "{spell.incantation}"\n', self.FG_CYAN)
        self._append_output("  ══════════════════════════════════════════════════\n", self.FG_DIM)
        self._append_output(f"\n  Effect: {spell.effect}\n\n", self.FG_GREEN)
        self._append_output("  ✦ Spell inscribed into your spellbook. ✦\n", self.FG_AMBER)

    def _append_entry(self, entry):
        """Append a spellbook entry to the output area.

        Args:
            entry (dict): The spellbook entry to display.
        """
        self._append_output(f"\n  ── Today's Spell ──\n", self.FG_CYAN)
        self._append_output(f"  Date: {entry.get('date', '')} at {entry.get('time', '')}\n")
        self._append_output(f"  Mage: {entry.get('mage_name', '')} {entry.get('mage_title', '')}\n")
        self._append_output(f"  Mood: {entry.get('mood', '')} ({entry.get('element', '')})\n")
        self._append_output(f"  Spell: {entry.get('spell_name', '')}\n")
        self._append_output(f"  Power: {entry.get('power_level', '')}/10 — {entry.get('power_tier', '')}\n")
        self._append_output(f"  Duration: {entry.get('duration', '')}\n")
        self._append_output(f'  Incantation: "{entry.get("incantation", "")}"\n', self.FG_CYAN)
        self._append_output(f"  Effect: {entry.get('effect', '')}\n")

    # ── Spellbook View ─────────────────────────────────────

    def _on_view_spellbook(self):
        """Display the spellbook in the output area."""
        self.spellbook.load_all()
        entries = self.spellbook.entries

        if not entries:
            self._display(
                "\n  The spellbook lies empty and dormant.\n"
                "  Cast your first spell to begin your magical archive.\n",
                self.FG_AMBER,
            )
            return

        self._clear_output()
        self._append_output(f"\n  ══ SPELLBOOK ══  ({len(entries)} entries)\n\n", self.FG_CYAN)

        for i, entry in enumerate(reversed(entries), 1):
            element = entry.get("element", "")
            self._append_output(f"  ── Entry {i} ──\n", self.FG_DIM)
            self._append_output(f"  Date: {entry.get('date', '')} at {entry.get('time', '')}\n")
            self._append_output(f"  Mood: {entry.get('mood', '')} ", self.FG_GREEN)
            self._append_output(f"[{element}]\n", self.FG_AMBER)
            self._append_output(f"  Spell: {entry.get('spell_name', '')}\n", self.FG_GREEN)
            self._append_output(f"  Power: {entry.get('power_level', '')}/10 — {entry.get('power_tier', '')}\n")
            self._append_output(f'  "{entry.get("incantation", "")}"\n', self.FG_CYAN)
            self._append_output(f"  Effect: {entry.get('effect', '')}\n")
            self._append_output("\n")

    # ── Analysis View ──────────────────────────────────────

    def _on_analyze(self):
        """Display the analysis summary in the output area."""
        # Show period selection dialog
        dialog = tk.Toplevel(self.root)
        dialog.title("Analyze Trends")
        dialog.geometry("350x250")
        dialog.configure(bg=self.BG_DARK)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog, text="Analyze Emotional Trends",
            font=self.FONT_TITLE, fg=self.FG_GREEN, bg=self.BG_DARK,
        ).pack(pady=(20, 15))

        periods = [("Past Week", "week"), ("Past Month", "month"), ("All Time", "all")]
        for label, period in periods:
            btn = tk.Button(
                dialog, text=label,
                font=self.FONT_MONO, fg=self.FG_GREEN, bg=self.BG_BUTTON,
                activebackground=self.BG_BUTTON_HOVER, activeforeground=self.FG_CYAN,
                bd=0, pady=8, cursor="hand2",
                command=lambda p=period, d=dialog: self._show_analysis(p, d),
            )
            btn.pack(fill="x", padx=30, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.BG_BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.BG_BUTTON))

    def _show_analysis(self, period, dialog):
        """Display the analysis summary for a given period.

        Args:
            period (str): "week", "month", or "all".
            dialog (tk.Toplevel): The dialog to close.
        """
        dialog.destroy()

        summary = self.analyzer.generate_summary(period)
        mood_dist = summary["mood_distribution"]
        elem_dist = summary["element_distribution"]

        self._clear_output()
        self._append_output(f"\n  ══ {summary['period_label'].upper()} SUMMARY ══\n\n", self.FG_CYAN)
        self._append_output(f"  Total Spells:  {summary['total_spells']}\n", self.FG_GREEN)
        self._append_output(f"  Date Range:    {summary['date_range']}\n", self.FG_GREEN)
        self._append_output(f"  Avg Power:     {summary['average_power']}/10\n", self.FG_GREEN)
        self._append_output(f"  Top Mood:      {summary['most_common_mood']} ({summary['most_common_mood_count']}x)\n\n", self.FG_AMBER)

        if mood_dist:
            self._append_output("  ── Mood Frequency ──\n", self.FG_CYAN)
            max_val = max(mood_dist.values()) if mood_dist else 1
            for mood, count in mood_dist.items():
                bar_len = int((count / max_val) * 20)
                bar = "█" * bar_len
                self._append_output(f"  {mood:<14} {bar} ({count})\n")
            self._append_output("\n")

        if elem_dist:
            self._append_output("  ── Element Distribution ──\n", self.FG_CYAN)
            max_val = max(elem_dist.values()) if elem_dist else 1
            for elem, count in elem_dist.items():
                bar_len = int((count / max_val) * 20)
                bar = "█" * bar_len
                self._append_output(f"  {elem:<14} {bar} ({count})\n")

    # ── Profile View ───────────────────────────────────────

    def _on_view_profile(self):
        """Display the mage's identity card."""
        if not self.mage:
            self._display("\n  No mage profile loaded.\n", self.FG_RED)
            return

        self._clear_output()
        self._append_output("\n  ══════════════════════════════════════════════════\n", self.FG_DIM)
        self._append_output("              ✦ MAGE IDENTITY ✦\n", self.FG_CYAN)
        self._append_output("  ══════════════════════════════════════════════════\n", self.FG_DIM)
        self._append_output(f"\n  Name:    {self.mage.name}\n", self.FG_GREEN)
        self._append_output(f"  Title:   {self.mage.title}\n", self.FG_AMBER)
        self._append_output(f"  Element: {self.mage.element}\n", self.FG_GREEN)
        self._append_output(f"  Familiar:{self.mage.familiar}\n", self.FG_GREEN)
        self._append_output(f"  Since:   {self.mage.creation_date}\n\n", self.FG_GREEN)
        self._append_output("  ══════════════════════════════════════════════════\n", self.FG_DIM)

    # ── Settings ───────────────────────────────────────────

    def _on_settings(self):
        """Show the settings dialog."""
        dialog = tk.Toplevel(self.root)
        dialog.title("Settings")
        dialog.geometry("400x250")
        dialog.configure(bg=self.BG_DARK)
        dialog.transient(self.root)
        dialog.grab_set()

        tk.Label(
            dialog, text="⚙ Settings",
            font=self.FONT_TITLE, fg=self.FG_GREEN, bg=self.BG_DARK,
        ).pack(pady=(20, 15))

        options = [
            ("Reset Mage Profile", self._reset_mage),
            ("Clear Spellbook", self._clear_spellbook),
            ("Close", dialog.destroy),
        ]

        for text, command in options:
            btn = tk.Button(
                dialog, text=text,
                font=self.FONT_MONO, fg=self.FG_GREEN, bg=self.BG_BUTTON,
                activebackground=self.BG_BUTTON_HOVER, activeforeground=self.FG_CYAN,
                bd=0, pady=8, cursor="hand2",
                command=lambda c=command, d=dialog: self._run_setting(c, d),
            )
            btn.pack(fill="x", padx=30, pady=3)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=self.BG_BUTTON_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=self.BG_BUTTON))

    def _run_setting(self, command, dialog):
        """Execute a setting action and close the dialog.

        Args:
            command (callable): The setting function to run.
            dialog (tk.Toplevel): The dialog to close.
        """
        dialog.destroy()
        command()

    def _reset_mage(self):
        """Reset the mage profile after confirmation."""
        if messagebox.askyesno("Confirm Reset", "Delete your mage identity and create a new one?"):
            profile_path = MageIdentity.PROFILE_PATH
            if os.path.exists(profile_path):
                os.remove(profile_path)
            self.mage = MageIdentity.create_new()
            self.mage.save()
            self._refresh_status()
            self._display("\n  ✦ Mage profile reset successfully. ✦\n", self.FG_AMBER)

    def _clear_spellbook(self):
        """Clear the spellbook after confirmation."""
        if messagebox.askyesno("Confirm Clear", "Delete ALL spellbook entries permanently?"):
            if os.path.exists(self.spellbook.filepath):
                os.remove(self.spellbook.filepath)
            self.spellbook._ensure_file_exists()
            self.spellbook.entries = []
            self._refresh_status()
            self._display("\n  ✦ Spellbook cleared. ✦\n", self.FG_AMBER)

    # ── Run ────────────────────────────────────────────────

    def run(self):
        """Start the GUI application main loop."""
        # Show welcome message
        self._display(
            f"\n  ✦ SoulScript.exe ✦\n\n"
            f"  Welcome, {self.mage.name} {self.mage.title}\n"
            f"  Element: {self.mage.element} | Familiar: {self.mage.familiar}\n"
            f"  Active Since: {self.mage.creation_date}\n\n"
            f"  Select an action from the buttons below.\n",
            self.FG_GREEN,
        )
        self.root.mainloop()
