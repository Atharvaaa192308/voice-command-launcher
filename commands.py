"""
commands.py - Command Definitions and Data Structures

This module stores all predefined data structures used by the Voice Command Launcher.
It demonstrates fundamental Python data collections:
- Lists: for the ordered 20-item startup menu
- Dictionaries: for fast key-value lookups (commands to URLs, apps, folders, and numbers)
- Tuples: for immutable pairs of application names, folder paths, and help tips
- Sets: for fast membership testing of exit keywords and action verbs
"""

import os

# LIST: Ordered list of 20 menu commands displayed to the user.
# The index in this list corresponds to menu numbers 1 through 20.
AVAILABLE_COMMANDS = [
    "Open YouTube",
    "Open Google",
    "Open GitHub",
    "Open Calculator",
    "Open Notepad",
    "Search the Web",
    "Show Time",
    "Show Help",
    "Open Gmail",
    "Open Wikipedia",
    "Open Downloads",
    "Open Documents",
    "Open Desktop",
    "Calculate (e.g. 25 + 50)",
    "Show Date",
    "Command History",
    "Session Statistics",
    "Clear Screen",
    "About Project",
    "Exit"
]

# DICTIONARY: Maps voice-style commands and website names to official URLs.
# When the user enters "open youtube" or "youtube", this dictionary provides the target URL.
WEBSITE_URLS = {
    "open youtube": "https://www.youtube.com",
    "youtube": "https://www.youtube.com",
    "open google": "https://www.google.com",
    "google": "https://www.google.com",
    "open github": "https://www.github.com",
    "github": "https://www.github.com",
    "open gmail": "https://mail.google.com",
    "gmail": "https://mail.google.com",
    "open wikipedia": "https://www.wikipedia.org",
    "wikipedia": "https://www.wikipedia.org",
}

# DICTIONARY: Short command aliases that translate quick abbreviations into full commands.
# Example: typing "yt" is translated into "open youtube".
COMMAND_ALIASES = {
    "yt": "open youtube",
    "google": "open google",
    "gh": "open github",
}

# DICTIONARY & TUPLES: Maps voice commands to fixed (Application Name, Executable) tuples.
# Tuples are used because the pairing between the display name and executable is permanent.
APPLICATION_COMMANDS = {
    "open calculator": ("Calculator", "calc.exe"),
    "calculator": ("Calculator", "calc.exe"),
    "open notepad": ("Notepad", "notepad.exe"),
    "notepad": ("Notepad", "notepad.exe"),
}

# DICTIONARY & TUPLES: Maps folder voice commands to fixed (Folder Name, Folder Path) tuples.
# os.path.expanduser("~") finds the current user's home directory (e.g., C:\Users\Username),
# and os.path.join() safely combines it with the subfolder name.
FOLDER_COMMANDS = {
    "open downloads": ("Downloads", os.path.join(os.path.expanduser("~"), "Downloads")),
    "downloads": ("Downloads", os.path.join(os.path.expanduser("~"), "Downloads")),
    "open documents": ("Documents", os.path.join(os.path.expanduser("~"), "Documents")),
    "documents": ("Documents", os.path.join(os.path.expanduser("~"), "Documents")),
    "open desktop": ("Desktop", os.path.join(os.path.expanduser("~"), "Desktop")),
    "desktop": ("Desktop", os.path.join(os.path.expanduser("~"), "Desktop")),
}

# SET: A collection of words that instruct the launcher to shut down.
# A set is ideal here because we only need to test if a command is in the set ("in" operator).
EXIT_COMMANDS = {
    "exit",
    "quit",
    "close",
    "stop",
    "bye"
}

# SET: Core action keywords recognized by the launcher.
CORE_ACTION_KEYWORDS = {
    "open",
    "search",
    "show",
    "help",
    "exit",
    "quit",
    "time",
    "date",
    "calculate",
    "history",
    "stats",
    "clear",
    "about"
}

# TUPLE: Immutable collection of helpful tips displayed when the user types "help".
HELP_TIPS = (
    "Commands are case-insensitive ('Open YouTube' is the same as 'open youtube').",
    "Extra spaces at the beginning, end, or between words are automatically cleaned.",
    "Use 'search <topic>' (e.g., 'search python programming') to search on Google.",
    "Use 'calculate <num1> <op> <num2>' (e.g., 'calculate 25 + 50') for safe math.",
    "Type 'history' to view previous commands, or 'stats' for session statistics.",
    "You can type the command name or enter the corresponding menu number.",
    "Type 'exit', 'quit', or 'bye' anytime to close the launcher safely."
)

# DICTIONARY: Maps numeric menu options (strings "1" to "20") to their voice commands.
# This allows the user to simply type a number instead of typing the whole command.
MENU_NUMBER_MAP = {
    "1": "open youtube",
    "2": "open google",
    "3": "open github",
    "4": "open calculator",
    "5": "open notepad",
    "6": "search the web",
    "7": "show time",
    "8": "help",
    "9": "open gmail",
    "10": "open wikipedia",
    "11": "open downloads",
    "12": "open documents",
    "13": "open desktop",
    "14": "calculate",
    "15": "show date",
    "16": "history",
    "17": "stats",
    "18": "clear",
    "19": "about",
    "20": "exit"
}
