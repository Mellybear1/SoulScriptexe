"""
SoulScript.exe — DataAnalyzer Module
Provides data analysis features for the spellbook, including
mood frequency, element distribution, streaks, and summaries.
"""

from collections import Counter
from datetime import datetime, timedelta


class DataAnalyzer:
    """Analyzes spellbook data to reveal emotional trends and patterns.

    Attributes:
        spellbook (Spellbook): Reference to the spellbook for data access.
    """

    def __init__(self, spellbook):
        """Initialize the DataAnalyzer with a spellbook reference.

        Args:
            spellbook (Spellbook): The spellbook to analyze.
        """
        self.spellbook = spellbook

    def _get_entries(self, period="all"):
        """Get entries filtered by a time period.

        Args:
            period (str): "week", "month", or "all".

        Returns:
            list[dict]: Filtered entries.
        """
        self.spellbook.load_all()
        entries = self.spellbook.entries

        if period == "all" or not entries:
            return entries

        today = datetime.now()
        if period == "week":
            cutoff = today - timedelta(days=7)
        elif period == "month":
            cutoff = today - timedelta(days=30)
        else:
            return entries

        cutoff_str = cutoff.strftime("%Y-%m-%d")
        return [e for e in entries if e.get("date", "") >= cutoff_str]

    def most_common_mood(self, period="all"):
        """Find the most frequently occurring mood in a time period.

        Args:
            period (str): "week", "month", or "all".

        Returns:
            tuple: (mood_name, count) or (None, 0) if no entries.
        """
        entries = self._get_entries(period)
        if not entries:
            return None, 0

        moods = [e.get("mood", "Unknown") for e in entries]
        counter = Counter(moods)
        most_common = counter.most_common(1)[0]
        return most_common

    def mood_frequency_distribution(self, period="all"):
        """Calculate the frequency of each mood category.

        Args:
            period (str): "week", "month", or "all".

        Returns:
            dict: Mapping of mood names to their counts, sorted by frequency.
        """
        entries = self._get_entries(period)
        if not entries:
            return {}

        moods = [e.get("mood", "Unknown") for e in entries]
        counter = Counter(moods)
        return dict(counter.most_common())

    def element_distribution(self, period="all"):
        """Calculate the frequency of each element.

        Args:
            period (str): "week", "month", or "all".

        Returns:
            dict: Mapping of element names to their counts, sorted by frequency.
        """
        entries = self._get_entries(period)
        if not entries:
            return {}

        elements = [e.get("element", "Unknown") for e in entries]
        counter = Counter(elements)
        return dict(counter.most_common())

    def average_power_level(self, period="all"):
        """Calculate the average spell power level.

        Args:
            period (str): "week", "month", or "all".

        Returns:
            float: The average power level, or 0.0 if no entries.
        """
        entries = self._get_entries(period)
        if not entries:
            return 0.0

        levels = []
        for e in entries:
            try:
                levels.append(int(e.get("power_level", 0)))
            except (ValueError, TypeError):
                pass

        return round(sum(levels) / len(levels), 1) if levels else 0.0

    def mood_streaks(self):
        """Find consecutive-day streaks of the same mood category.

        Returns:
            list[dict]: List of streaks with mood, start_date, end_date, and length.
        """
        entries = self._get_entries("all")
        if not entries:
            return []

        # Sort entries by date
        sorted_entries = sorted(entries, key=lambda e: e.get("date", ""))

        streaks = []
        current_mood = None
        current_start = None
        current_end = None
        streak_length = 0

        for entry in sorted_entries:
            mood = entry.get("mood", "Unknown")
            date = entry.get("date", "")

            if mood == current_mood:
                # Continue streak
                current_end = date
                streak_length += 1
            else:
                # End previous streak if it was 2+ days
                if streak_length >= 2 and current_mood:
                    streaks.append({
                        "mood": current_mood,
                        "start_date": current_start,
                        "end_date": current_end,
                        "length": streak_length,
                    })
                # Start new streak
                current_mood = mood
                current_start = date
                current_end = date
                streak_length = 1

        # Don't forget the last streak
        if streak_length >= 2 and current_mood:
            streaks.append({
                "mood": current_mood,
                "start_date": current_start,
                "end_date": current_end,
                "length": streak_length,
            })

        # Sort by length descending
        streaks.sort(key=lambda s: s["length"], reverse=True)
        return streaks

    def generate_summary(self, period="all"):
        """Generate a comprehensive summary for a time period.

        Args:
            period (str): "week", "month", or "all".

        Returns:
            dict: Summary data including counts, distributions, and averages.
        """
        entries = self._get_entries(period)
        period_label = {"week": "Past Week", "month": "Past Month", "all": "All Time"}.get(
            period, "All Time"
        )

        total = len(entries)
        most_common = self.most_common_mood(period)
        mood_dist = self.mood_frequency_distribution(period)
        elem_dist = self.element_distribution(period)
        avg_power = self.average_power_level(period)

        # Date range
        if entries:
            dates = [e.get("date", "") for e in entries if e.get("date")]
            first_date = min(dates) if dates else "Unknown"
            last_date = max(dates) if dates else "Unknown"
        else:
            first_date = "N/A"
            last_date = "N/A"

        return {
            "period_label": period_label,
            "total_spells": total,
            "date_range": f"{first_date} to {last_date}",
            "most_common_mood": most_common[0],
            "most_common_mood_count": most_common[1],
            "mood_distribution": mood_dist,
            "element_distribution": elem_dist,
            "average_power": avg_power,
        }

    def display_chart(self, data, title="Distribution", bar_char="█", max_width=30):
        """Generate a simple text-based horizontal bar chart.

        Args:
            data (dict): Mapping of labels to values.
            title (str): Chart title.
            bar_char (str): Character used for bars.
            max_width (int): Maximum bar width in characters.

        Returns:
            str: The formatted bar chart string.
        """
        if not data:
            return f"  {title}: No data available."

        max_value = max(data.values()) if data else 1
        lines = [f"\n  ── {title} ──\n"]

        for label, value in data.items():
            if max_value > 0:
                bar_length = int((value / max_value) * max_width)
            else:
                bar_length = 0
            bar = bar_char * bar_length
            lines.append(f"  {label:<14} {bar} ({value})")

        return "\n".join(lines)

    def display_summary(self, period="all"):
        """Return a formatted summary string for display.

        Args:
            period (str): "week", "month", or "all".

        Returns:
            str: The formatted summary text.
        """
        summary = self.generate_summary(period)

        lines = [
            "",
            "╔══════════════════════════════════════════════════╗",
            f"║        ✦ {summary['period_label']:<14} SUMMARY ✦                ║",
            "╠══════════════════════════════════════════════════╣",
            f"║  Total Spells:  {summary['total_spells']:<33} ║",
            f"║  Date Range:    {summary['date_range']:<33} ║",
            f"║  Avg Power:     {summary['average_power']:<33} ║",
            "╠══════════════════════════════════════════════════╣",
            f"║  Most Common Mood: {summary['most_common_mood']:<29} ║",
            f"║  Mood Count:       {summary['most_common_mood_count']:<29} ║",
            "╚══════════════════════════════════════════════════╝",
        ]

        result = "\n".join(lines)

        # Add mood chart
        if summary["mood_distribution"]:
            result += self.display_chart(
                summary["mood_distribution"], title="Mood Frequency"
            )

        # Add element chart
        if summary["element_distribution"]:
            result += self.display_chart(
                summary["element_distribution"], title="Element Distribution"
            )

        return result
