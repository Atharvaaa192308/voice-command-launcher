"""
utils.py - Utility and Helper Functions

This module provides helper functions for string cleaning, Google search URL
formatting, system date and time formatting, and console output.

Python Essentials concepts demonstrated:
- String methods: lower(), strip(), split(), and join()
- Module imports: datetime and urllib.parse
- Type conversion: str() for safe string handling
- String repetition operator: using * to create decorative divider lines
- Conditionals: checking operating system type with os.name
"""

from datetime import datetime
import os
import urllib.parse


def normalize_command(command_text):
    """
    Cleans and standardizes raw user input.
    - Strips leading and trailing whitespace
    - Converts text to lowercase
    - Collapses multiple spaces between words into a single space

    Example:
        "  OPEN   YOUTUBE  " -> "open youtube"
    """
    # If None was passed, return an empty string to avoid errors.
    if command_text is None:
        return ""

    # Convert the input to a string in case the caller passed a number.
    text = str(command_text)

    # Remove extra spaces from the start and end, and convert all characters
    # to lowercase so that "YouTube", "YOUTUBE", and "youtube" match the same way.
    cleaned = text.strip().lower()

    # Split the string by whitespace into a list of words, then rejoin them
    # with a single space. This turns "open    google" into "open google".
    words = cleaned.split()
    normalized = " ".join(words)

    return normalized


def build_search_url(query):
    """
    Builds a valid Google Search URL from a user's search query string.
    Uses urllib.parse.quote_plus to safely encode spaces and special characters.

    Example:
        "python programming" -> "https://www.google.com/search?q=python+programming"
    """
    # Remove any extra leading or trailing spaces from the search query.
    cleaned_query = query.strip()

    # Safely encode the search text. This replaces spaces with '+' and
    # converts special characters (like ?, &, =) into percent-encoded strings.
    encoded_query = urllib.parse.quote_plus(cleaned_query)

    # Combine the base Google search URL with the encoded query string.
    search_url = f"https://www.google.com/search?q={encoded_query}"
    return search_url


def format_current_time():
    """
    Returns the current system date and time as a readable string.
    Example: "Friday, 25 September 2026 | 06:15:30 PM"
    """
    # Get current date and time from the system clock.
    now = datetime.now()

    # Format the datetime object using standard strftime directives:
    # %A: Full weekday name (e.g. Friday)
    # %d: Two-digit day of month (e.g. 25)
    # %B: Full month name (e.g. September)
    # %Y: Four-digit year (e.g. 2026)
    # %I: Hour in 12-hour format (01-12)
    # %M: Minute (00-59)
    # %S: Second (00-59)
    # %p: AM or PM
    return now.strftime("%A, %d %B %Y | %I:%M:%S %p")


def format_current_date():
    """
    Returns the current system date as a readable string.
    Example: "Friday, 25 September 2026"
    """
    # Get current date from the system clock.
    now = datetime.now()

    # Format as: Day of week, Day Month Year
    return now.strftime("%A, %d %B %Y")


def clear_terminal():
    """
    Clears the terminal screen.
    Uses 'cls' on Windows systems and 'clear' on macOS or Linux systems.
    """
    # Check if the operating system is Windows (os.name is 'nt')
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_banner():
    """
    Prints a clean welcome header for the application.
    Demonstrates string repetition using the * operator.
    """
    separator = "=" * 40
    print(separator)
    print("        VOICE COMMAND LAUNCHER")
    print(separator)


def print_separator(char="-", length=40):
    """
    Prints a divider line of the specified character and length.
    Demonstrates default function argument values and string repetition (*).
    """
    print(char * length)
