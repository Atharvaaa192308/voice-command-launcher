"""
launcher.py - Main Launcher Functions and Command Dispatcher

This module implements the core business logic of the Voice Command Launcher:
- show_menu(): Displays the menu of available commands
- process_command(): Parses and routes normalized commands
- open_website(): Launches predefined websites via the webbrowser module
- open_application(): Safely starts Windows system applications via subprocess
- open_folder(): Safely opens predefined Windows user folders via subprocess
- search_web(): Performs web search with query parameter encoding
- calculate_expression(): Safely evaluates basic arithmetic expressions without eval()
- show_time(): Displays formatted current system date and time
- show_date(): Displays formatted current system date
- show_history(): Displays session command history with numbering
- show_stats(): Displays total, successful, and unknown command statistics
- show_about(): Displays project metadata and summary
- clear_screen(): Clears the terminal screen
- show_help(): Prints comprehensive command guide organized by category

Demonstrates:
- if / elif / else conditionals
- for loop iterations
- Functions with parameters and return values
- Exception handling (try / except)
- Standard library modules: os, subprocess, webbrowser, datetime
"""

import os
import subprocess
import webbrowser

from commands import (
    APPLICATION_COMMANDS,
    AVAILABLE_COMMANDS,
    COMMAND_ALIASES,
    EXIT_COMMANDS,
    FOLDER_COMMANDS,
    HELP_TIPS,
    MENU_NUMBER_MAP,
    WEBSITE_URLS,
)
from utils import (
    build_search_url,
    clear_terminal,
    format_current_date,
    format_current_time,
    normalize_command,
    print_banner,
    print_separator,
)

# SESSION STATE: Tracks history and execution statistics during the current runtime
SESSION_DATA = {
    "history": [],
    "total": 0,
    "successful": 0,
    "unknown": 0
}


def reset_session_data() -> None:
    """
    Resets the session history and counters. Useful for testing and cleanup.
    """
    SESSION_DATA["history"].clear()
    SESSION_DATA["total"] = 0
    SESSION_DATA["successful"] = 0
    SESSION_DATA["unknown"] = 0


def show_menu() -> None:
    """
    Displays the application banner and the numbered list of available commands.
    Demonstrates:
    - for loop
    - range() and len()
    - Arithmetic operator (+ 1)
    - List indexing
    """
    print_banner()
    print("Available commands:\n")
    
    # Loop over the list of available commands using numeric indices
    for index in range(len(AVAILABLE_COMMANDS)):
        menu_number = index + 1
        command_label = AVAILABLE_COMMANDS[index]
        print(f"{menu_number}. {command_label}")
    
    print("\nType \"help\" to see available commands.")


def open_website(target: str) -> bool:
    """
    Safely opens a website in the default system web browser.
    The target can be a registered keyword key (e.g., 'open youtube') or a valid URL.
    
    Returns True if launch was initiated successfully, False otherwise.
    """
    target_url = None
    display_title = "Website"

    # Check if target is a registered website keyword in the dictionary
    if target in WEBSITE_URLS:
        target_url = WEBSITE_URLS[target]
        clean_name = target.replace("open ", "").strip()
        if clean_name.lower() == "github":
            display_title = "GitHub"
        else:
            display_title = clean_name.title()
    elif target.startswith("http://") or target.startswith("https://"):
        target_url = target
        display_title = "Web Page"
    else:
        print(f"\nUnrecognized website: '{target}'")
        return False

    # Only print standard opening message if not already displaying search
    if not target_url.startswith("https://www.google.com/search"):
        print(f"\nOpening {display_title}...")

    # Safe launch with exception handling
    try:
        success = webbrowser.open(target_url)
        if success is False:
            return False
        return True
    except webbrowser.Error as web_err:
        print(f"Browser launch error: {web_err}")
        return False
    except Exception as general_err:
        print(f"Unexpected error while opening browser: {general_err}")
        return False


def open_application(app_key: str) -> bool:
    """
    Safely launches a Windows desktop application from a predefined dictionary.
    Does NOT allow execution of arbitrary user commands.

    Returns True if launch was successful, False otherwise.
    """
    if app_key not in APPLICATION_COMMANDS:
        print(f"\nUnsupported application command: '{app_key}'")
        print("Supported applications: Calculator, Notepad.")
        return False

    # Extract display name and executable from the configured tuple
    app_info = APPLICATION_COMMANDS[app_key]
    display_name = app_info[0]
    executable_name = app_info[1]

    print(f"\nOpening {display_name}...")

    # Launch application using a controlled list argument (never arbitrary shell strings)
    try:
        subprocess.Popen([executable_name])
        return True
    except FileNotFoundError:
        print(f"Error: Could not find application '{executable_name}' on this system.")
        return False
    except OSError as os_err:
        print(f"Operating system error while launching '{display_name}': {os_err}")
        return False
    except Exception as general_err:
        print(f"Unexpected error launching application: {general_err}")
        return False


def open_folder(folder_key: str) -> bool:
    """
    Safely opens a predefined Windows folder in File Explorer.
    Only allows predefined folder shortcuts: Downloads, Documents, Desktop.
    Does NOT allow opening arbitrary user paths.
    """
    if folder_key not in FOLDER_COMMANDS:
        print(f"\nUnsupported folder command: '{folder_key}'")
        print("Supported folders: Downloads, Documents, Desktop.")
        return False

    display_name, folder_path = FOLDER_COMMANDS[folder_key]
    print(f"\nOpening {display_name} folder...")

    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)
        subprocess.Popen(["explorer.exe", folder_path])
        return True
    except FileNotFoundError:
        print("Error: Windows Explorer utility not found on this system.")
        return False
    except OSError as os_err:
        print(f"Operating system error while opening {display_name}: {os_err}")
        return False
    except Exception as general_err:
        print(f"Unexpected error opening folder: {general_err}")
        return False


def search_web(query: str) -> bool:
    """
    Performs a web search by building a Google query URL and opening it in the browser.

    Returns True if search URL opened successfully, False otherwise.
    """
    clean_query = query.strip()
    
    # Check if query is empty
    if len(clean_query) == 0:
        print("\nSearch query cannot be empty.")
        print("Usage: search <topic>  (e.g., search python programming)")
        return False

    print(f"\nSearching for: {clean_query}...")
    search_url = build_search_url(clean_query)
    return open_website(search_url)


def calculate_expression(expression: str) -> bool:
    """
    Safely parses and calculates a basic arithmetic expression between two numbers.
    Supports operators: +, -, *, /
    Validates input before calculating.
    Does NOT use eval() or execute arbitrary code.
    
    Returns True if calculation was successful, False otherwise.
    """
    clean_expr = expression.strip()
    if not clean_expr:
        print("\nMissing expression to calculate.")
        print("Usage: calculate <num1> <operator> <num2>  (Example: calculate 25 + 50)")
        return False

    # Search for an arithmetic operator (+, -, *, /)
    # If the expression starts with '-', allow negative first number
    search_start = 1 if clean_expr.startswith("-") else 0
    found_op = None
    op_pos = -1

    for op in ("+", "-", "*", "/"):
        idx = clean_expr.find(op, search_start)
        if idx != -1:
            found_op = op
            op_pos = idx
            break

    if found_op is None:
        print(f"\nNo valid operator (+, -, *, /) found in '{clean_expr}'.")
        print("Usage: calculate <num1> <operator> <num2>  (Example: calculate 25 + 50)")
        return False

    left_str = clean_expr[:op_pos].strip()
    right_str = clean_expr[op_pos + 1:].strip()

    if not left_str or not right_str:
        print(f"\nIncomplete expression '{clean_expr}'.")
        print("Usage: calculate <num1> <operator> <num2>  (Example: calculate 25 + 50)")
        return False

    try:
        num1 = float(left_str)
        num2 = float(right_str)
    except ValueError:
        print(f"\nInvalid numeric values in '{clean_expr}'. Please enter numbers only.")
        return False

    if found_op == "+":
        result = num1 + num2
    elif found_op == "-":
        result = num1 - num2
    elif found_op == "*":
        result = num1 * num2
    elif found_op == "/":
        if num2 == 0:
            print("\nError: Division by zero is not allowed.")
            return False
        result = num1 / num2
    else:
        print(f"\nUnsupported operator '{found_op}'.")
        return False

    # Format result: integer if whole number, otherwise rounded float
    display_result = int(result) if result.is_integer() else round(result, 4)
    print_separator("-", 40)
    print("CALCULATION RESULT:")
    print(f"  {clean_expr} = {display_result}")
    print_separator("-", 40)
    return True


def show_time() -> None:
    """
    Displays the current system date and time in a formatted box.
    """
    current_time_str = format_current_time()
    print_separator("-", 40)
    print("CURRENT SYSTEM TIME:")
    print(f"  {current_time_str}")
    print_separator("-", 40)


def show_date() -> None:
    """
    Displays the current system date in a formatted box.
    """
    current_date_str = format_current_date()
    print_separator("-", 40)
    print("CURRENT SYSTEM DATE:")
    print(f"  {current_date_str}")
    print_separator("-", 40)


def show_history() -> None:
    """
    Displays the list of commands entered in the current session with numbering.
    """
    print_separator("-", 40)
    print("COMMAND HISTORY (Current Session):")
    if not SESSION_DATA["history"]:
        print("  No commands recorded yet.")
    else:
        for idx, cmd in enumerate(SESSION_DATA["history"], start=1):
            print(f"  {idx}. {cmd}")
    print_separator("-", 40)


def show_stats() -> None:
    """
    Displays execution counts for the current session.
    """
    print_separator("-", 40)
    print("SESSION STATISTICS:")
    print(f"Total commands: {SESSION_DATA['total']}")
    print(f"Successful commands: {SESSION_DATA['successful']}")
    print(f"Unknown commands: {SESSION_DATA['unknown']}")
    print_separator("-", 40)


def show_about() -> None:
    """
    Displays project metadata and description.
    """
    print_separator("=", 40)
    print("          ABOUT THIS PROJECT")
    print_separator("=", 40)
    print("Voice Command Launcher")
    print("Python Essentials Project")
    print("Command-line based launcher")
    print("Built using Python standard library")
    print_separator("=", 40)


def clear_screen() -> None:
    """
    Clears the console screen using cross-platform terminal clear utility.
    """
    clear_terminal()


def show_help() -> None:
    """
    Prints a detailed command guide organized by category.
    Demonstrates for loop over tuple elements.
    """
    print_separator("=", 40)
    print("          COMMAND GUIDE & HELP")
    print_separator("=", 40)
    print("\nWEBSITES")
    print("- open youtube")
    print("- open google")
    print("- open github")
    print("- open gmail")
    print("- open wikipedia\n")
    print("APPLICATIONS")
    print("- open calculator")
    print("- open notepad\n")
    print("FOLDERS")
    print("- open downloads")
    print("- open documents")
    print("- open desktop\n")
    print("UTILITIES")
    print("- search <query>")
    print("- calculate <expression>")
    print("- show time")
    print("- show date\n")
    print("SYSTEM")
    print("- history")
    print("- stats")
    print("- clear")
    print("- about")
    print("- help")
    print("- exit\n")
    print("HELPFUL TIPS:")
    for tip in HELP_TIPS:
        print(f" * {tip}")
    print_separator("=", 40)


def process_command(command: str) -> bool:
    """
    Normalizes and processes a user command.
    Routes the command to the appropriate functional handler using if/elif/else.

    Returns:
        bool: True if the launcher should continue running,
              False if an exit command was received.
    """
    normalized = normalize_command(command)

    # Empty command check
    if len(normalized) == 0:
        print("\nNo command entered. Type 'help' to see available commands.")
        return True

    # Record all non-empty commands into session history and total count
    SESSION_DATA["history"].append(command.strip())
    SESSION_DATA["total"] += 1

    # Check for command aliases (e.g. yt -> open youtube, gh -> open github, google -> open google)
    if normalized in COMMAND_ALIASES:
        normalized = COMMAND_ALIASES[normalized]

    # Check if the user entered a menu number ('1' through '21')
    if normalized in MENU_NUMBER_MAP:
        normalized = MENU_NUMBER_MAP[normalized]

    # MODULE: Exit Handling
    if normalized in EXIT_COMMANDS:
        SESSION_DATA["successful"] += 1
        print("\nThank you for using Voice Command Launcher. Goodbye!\n")
        return False

    # MODULE: Help
    elif normalized in ("help", "show help", "menu", "show menu"):
        SESSION_DATA["successful"] += 1
        show_help()
        return True

    # MODULE: Command History
    elif normalized in ("history", "show history", "command history"):
        SESSION_DATA["successful"] += 1
        show_history()
        return True

    # MODULE: Session Statistics
    elif normalized in ("stats", "statistics", "show stats"):
        SESSION_DATA["successful"] += 1
        show_stats()
        return True

    # MODULE: Clear Screen
    elif normalized == "clear":
        SESSION_DATA["successful"] += 1
        clear_screen()
        return True

    # MODULE: About Project
    elif normalized in ("about", "show about", "info"):
        SESSION_DATA["successful"] += 1
        show_about()
        return True

    # MODULE: Time
    elif normalized in ("show time", "time", "current time", "what time is it"):
        SESSION_DATA["successful"] += 1
        show_time()
        return True

    # MODULE: Date
    elif normalized in ("show date", "date", "current date", "today"):
        SESSION_DATA["successful"] += 1
        show_date()
        return True

    # MODULE: Calculator
    elif normalized.startswith("calculate ") or normalized == "calculate":
        if normalized == "calculate":
            print("\nPlease provide an expression to calculate.")
            print("Usage: calculate <num1> <operator> <num2>  (Example: calculate 25 + 50)")
            SESSION_DATA["unknown"] += 1
        else:
            clean_input = command.strip()
            parts = clean_input.split(maxsplit=1)
            expr_part = parts[1].strip() if len(parts) > 1 else ""
            success = calculate_expression(expr_part)
            if success:
                SESSION_DATA["successful"] += 1
            else:
                SESSION_DATA["unknown"] += 1
        return True

    # MODULE: Web Search
    elif normalized.startswith("search ") or normalized == "search" or normalized == "search the web":
        if normalized in ("search", "search the web"):
            print("\nPlease provide a search topic.")
            print("Usage: search <topic>  (Example: search python programming)")
            SESSION_DATA["unknown"] += 1
        else:
            # Preserve original casing of query while recognizing 'search' keyword
            clean_input = command.strip()
            parts = clean_input.split(maxsplit=1)
            if len(parts) > 1:
                query_part = parts[1].strip()
                if search_web(query_part):
                    SESSION_DATA["successful"] += 1
                else:
                    SESSION_DATA["unknown"] += 1
            else:
                print("\nPlease provide a search topic.")
                print("Usage: search <topic>  (Example: search python programming)")
                SESSION_DATA["unknown"] += 1
        return True

    # MODULE: Website Launcher
    elif normalized in WEBSITE_URLS:
        if open_website(normalized):
            SESSION_DATA["successful"] += 1
        else:
            SESSION_DATA["unknown"] += 1
        return True

    # MODULE: Application Launcher
    elif normalized in APPLICATION_COMMANDS:
        if open_application(normalized):
            SESSION_DATA["successful"] += 1
        else:
            SESSION_DATA["unknown"] += 1
        return True

    # MODULE: Folder Shortcuts
    elif normalized in FOLDER_COMMANDS:
        if open_folder(normalized):
            SESSION_DATA["successful"] += 1
        else:
            SESSION_DATA["unknown"] += 1
        return True

    # Check for incomplete "open" command
    elif normalized == "open":
        SESSION_DATA["unknown"] += 1
        print("\nPlease specify what you want to open.")
        print("Usage: open <website/app/folder>  (Example: open youtube, open calculator, open downloads)")
        print("Type 'help' to see all available commands.")
        return True

    # Check for general "open <target>" pattern
    elif normalized.startswith("open "):
        SESSION_DATA["unknown"] += 1
        target = normalized.replace("open ", "", 1).strip()
        print(f"\nCannot open '{target}'.")
        print("Available options: YouTube, Google, GitHub, Gmail, Wikipedia, Calculator, Notepad, Downloads, Documents, Desktop.")
        print("Type 'help' to see all available commands.")
        return True

    # Unknown command handling
    else:
        SESSION_DATA["unknown"] += 1
        print(f"\nCommand not recognized: '{command.strip()}'")
        print("Type 'help' to see available commands.")
        return True
