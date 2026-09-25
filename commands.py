"""
commands.py - Command Definitions and Data Structures

This module contains predefined data structures for the Voice Command Launcher.
It demonstrates core Python data types:
- Lists: for ordered menu items
- Tuples: for immutable application configurations and tips
- Sets: for fast membership testing of keywords and exit commands
- Dictionaries: for mapping user commands to URLs, applications, and actions
"""

import os

# LIST: Ordered list of available menu commands displayed to the user
# Preserves 1 to 9 indices for backward compatibility with existing tests
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

# DICTIONARY: Maps voice commands / keywords to official website URLs
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

# DICTIONARY: Quick aliases mapping to standard voice commands
COMMAND_ALIASES = {
    "yt": "open youtube",
    "google": "open google",
    "gh": "open github",
}

# DICTIONARY & TUPLES: Maps voice commands to fixed (Application Name, Executable) tuples
# Designed specifically for Windows operating systems
APPLICATION_COMMANDS = {
    "open calculator": ("Calculator", "calc.exe"),
    "calculator": ("Calculator", "calc.exe"),
    "open notepad": ("Notepad", "notepad.exe"),
    "notepad": ("Notepad", "notepad.exe"),
}

# DICTIONARY & TUPLES: Maps folder voice commands to fixed (Folder Name, Absolute Path) tuples
# Uses safe predefined system directories on Windows
FOLDER_COMMANDS = {
    "open downloads": ("Downloads", os.path.join(os.path.expanduser("~"), "Downloads")),
    "downloads": ("Downloads", os.path.join(os.path.expanduser("~"), "Downloads")),
    "open documents": ("Documents", os.path.join(os.path.expanduser("~"), "Documents")),
    "documents": ("Documents", os.path.join(os.path.expanduser("~"), "Documents")),
    "open desktop": ("Desktop", os.path.join(os.path.expanduser("~"), "Desktop")),
    "desktop": ("Desktop", os.path.join(os.path.expanduser("~"), "Desktop")),
}

# SET: Unique collection of commands that safely terminate the launcher
EXIT_COMMANDS = {
    "exit",
    "quit",
    "close",
    "stop",
    "bye"
}

# SET: Core action verbs recognized by the command processing engine
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

# TUPLE: Immutable collection of usage tips displayed in the help menu
HELP_TIPS = (
    "Commands are case-insensitive ('Open YouTube' is the same as 'open youtube').",
    "Extra spaces at the beginning, end, or between words are automatically cleaned.",
    "Use 'search <topic>' (e.g., 'search python programming') to search on Google.",
    "Use 'calculate <num1> <op> <num2>' (e.g., 'calculate 25 + 50') for safe math.",
    "Type 'history' to view previous commands, or 'stats' for session statistics.",
    "You can type the command name or enter the corresponding menu number.",
    "Type 'exit', 'quit', or 'bye' anytime to close the launcher safely."
)

# DICTIONARY: Maps numeric menu options (strings) to their corresponding voice command strings
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
