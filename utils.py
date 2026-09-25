"""
utils.py - Utility and Helper Functions

This module provides helper functions for string normalization,
URL construction, time formatting, and console output formatting.
Demonstrates:
- String methods: lower(), strip(), split(), replace()
- Module imports: datetime, urllib.parse
- Arithmetic operators: string repetition (*)
- Type conversion: str()
"""

from datetime import datetime
import os
import urllib.parse


def normalize_command(command_text: str) -> str:
    """
    Normalizes raw user input by converting to lowercase, removing leading/trailing
    whitespace, and collapsing redundant internal spaces.

    Example:
        "  OPEN   YOUTUBE  " -> "open youtube"
    """
    if command_text is None:
        return ""
    
    # Type conversion to ensure input is a string
    text = str(command_text)
    
    # Strip leading and trailing whitespace, then convert to lowercase
    cleaned = text.strip().lower()
    
    # Split into words to remove internal redundant spaces, then rejoin with a single space
    words = cleaned.split()
    normalized = " ".join(words)
    
    return normalized


def build_search_url(query: str) -> str:
    """
    Constructs a valid Google Search URL from a search query string.
    Uses standard library urllib.parse to safely encode special characters and spaces.

    Example:
        "python programming" -> "https://www.google.com/search?q=python+programming"
    """
    cleaned_query = query.strip()
    # Safely encode query parameters (converts spaces to '+' and escapes special characters)
    encoded_query = urllib.parse.quote_plus(cleaned_query)
    search_url = f"https://www.google.com/search?q={encoded_query}"
    return search_url


def format_current_time() -> str:
    """
    Returns the current local system date and time formatted in a clear,
    human-readable style using the datetime module.
    """
    now = datetime.now()
    # Formats as: Day, DD Month YYYY | HH:MM:SS AM/PM
    return now.strftime("%A, %d %B %Y | %I:%M:%S %p")


def format_current_date() -> str:
    """
    Returns the current local system date formatted in a clear,
    human-readable style using the datetime module.
    """
    now = datetime.now()
    # Formats as: Day, DD Month YYYY
    return now.strftime("%A, %d %B %Y")


def clear_terminal() -> None:
    """
    Clears the terminal screen using a fixed cross-platform command.
    Safe: uses hardcoded string literal 'cls' on Windows or 'clear' on Unix.
    Never executes user input.
    """
    os.system("cls" if os.name == "nt" else "clear")


def print_banner() -> None:
    """
    Prints a clean, formatted ASCII header banner for the application.
    Demonstrates string repetition operator (*).
    """
    separator = "=" * 40
    print(separator)
    print("        VOICE COMMAND LAUNCHER")
    print(separator)


def print_separator(char: str = "-", length: int = 40) -> None:
    """
    Prints a decorative separator line of specified character and length.
    """
    print(char * length)
