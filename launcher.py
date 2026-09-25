"""
launcher.py - Main Launcher Functions and Command Dispatcher

This module implements the core business logic of the Voice Command Launcher:
- show_menu(): Displays the 20 available numbered menu options
- process_command(): Normalizes user input and routes to the correct function
- open_website(): Safely opens predefined websites in the web browser
- open_application(): Safely starts Windows applications (Calculator, Notepad)
- open_folder(): Safely opens common Windows folders (Downloads, Documents, Desktop)
- search_web(): Performs Google searches with encoded query parameters
- calculate_expression(): Safely solves arithmetic problems (+, -, *, /) without eval()
- show_time(): Displays formatted current system date and time
- show_date(): Displays formatted current system date
- show_history(): Displays a numbered list of commands run this session
- show_stats(): Displays total, successful, and unknown command counts
- show_about(): Displays project information and course context
- clear_screen(): Clears the terminal screen
- show_help(): Displays a categorized command guide with helpful tips

Python Essentials concepts demonstrated:
- if / elif / else conditionals for command routing
- for loops and while loops for menus and repetition
- Functions with parameters and return values
- Dictionary operations for lookups and session state
- Exception handling (try / except) for safe system calls and calculations
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

# SESSION STATE: Tracks history and execution statistics during the current runtime.
# - 'history': list of command strings entered by the user
# - 'total': count of all non-empty commands entered
# - 'successful': count of commands that completed their task successfully
# - 'unknown': count of unrecognized commands or failed operations
SESSION_DATA = {
    "history": [],
    "total": 0,
    "successful": 0,
    "unknown": 0
}


def reset_session_data():
    """
    Resets the session history and counters back to zero.
    Useful for testing and for clearing session state.
    """
    # Empty the list of commands
    SESSION_DATA["history"].clear()

    # Reset all integer counters to zero
    SESSION_DATA["total"] = 0
    SESSION_DATA["successful"] = 0
    SESSION_DATA["unknown"] = 0


def show_menu():
    """
    Displays the application banner and the 20 numbered menu options.
    Demonstrates:
    - for loop over a list using range() and len()
    - Adding 1 to a zero-based index to create 1-based menu numbers
    """
    # Print the top ASCII banner
    print_banner()
    print("Available commands:\n")

    # Loop through the list of 20 available commands using range and index
    for index in range(len(AVAILABLE_COMMANDS)):
        menu_number = index + 1
        command_label = AVAILABLE_COMMANDS[index]
        print(f"{menu_number}. {command_label}")

    print('\nType "help" to see available commands.')


def open_website(target):
    """
    Safely opens a website in the default system web browser.
    The target can be a registered command (e.g. 'open youtube') or a full web URL.

    Returns:
        bool: True if the browser opened successfully, False otherwise.
    """
    target_url = None
    display_title = "Website"

    # Check if the target is a registered website key in our dictionary
    if target in WEBSITE_URLS:
        target_url = WEBSITE_URLS[target]
        # Create a clean display title (e.g., "open youtube" -> "Youtube")
        clean_name = target.replace("open ", "").strip()
        if clean_name.lower() == "github":
            display_title = "GitHub"
        else:
            display_title = clean_name.title()

    # Check if the user entered a direct http or https web address
    elif target.startswith("http://") or target.startswith("https://"):
        target_url = target
        display_title = "Web Page"

    # If the target is not recognized, print an error message and return False
    else:
        print(f"\nUnrecognized website: '{target}'")
        return False

    # Do not print "Opening..." if this is an automated Google search URL
    if not target_url.startswith("https://www.google.com/search"):
        print(f"\nOpening {display_title}...")

    # Open the browser inside a try/except block to handle any browser launch errors
    try:
        success = webbrowser.open(target_url)
        # If webbrowser.open returned False, report failure
        if success is False:
            return False
        return True

    except webbrowser.Error as web_err:
        print(f"Browser launch error: {web_err}")
        return False

    except Exception as general_err:
        print(f"Unexpected error while opening browser: {general_err}")
        return False


def open_application(app_key):
    """
    Safely launches a Windows desktop application from the predefined dictionary.
    Does NOT allow execution of arbitrary commands.

    Returns:
        bool: True if the application started successfully, False otherwise.
    """
    # Security check: only allow applications listed in APPLICATION_COMMANDS
    if app_key not in APPLICATION_COMMANDS:
        print(f"\nUnsupported application command: '{app_key}'")
        print("Supported applications: Calculator, Notepad.")
        return False

    # Unpack the display name and executable filename from the configured tuple
    app_info = APPLICATION_COMMANDS[app_key]
    display_name = app_info[0]
    executable_name = app_info[1]

    print(f"\nOpening {display_name}...")

    # Launch the process by passing the executable as a single-element list.
    # Passing a list prevents shell command injection.
    try:
        subprocess.Popen([executable_name])
        return True

    except FileNotFoundError:
        # Occurs if the executable file does not exist on this computer
        print(f"Error: Could not find application '{executable_name}' on this system.")
        return False

    except OSError as os_err:
        # Handles operating system permission or execution errors
        print(f"Operating system error while launching '{display_name}': {os_err}")
        return False

    except Exception as general_err:
        # Catch-all for any other unexpected runtime exceptions
        print(f"Unexpected error launching application: {general_err}")
        return False


def open_folder(folder_key):
    """
    Safely opens a predefined Windows user folder in File Explorer.
    Only allows predefined folder shortcuts: Downloads, Documents, Desktop.

    Returns:
        bool: True if the folder was opened successfully, False otherwise.
    """
    # Security check: verify the folder key is in our approved folder whitelist
    if folder_key not in FOLDER_COMMANDS:
        print(f"\nUnsupported folder command: '{folder_key}'")
        print("Supported folders: Downloads, Documents, Desktop.")
        return False

    # Unpack the folder display name and absolute folder path from the tuple
    display_name, folder_path = FOLDER_COMMANDS[folder_key]
    print(f"\nOpening {display_name} folder...")

    try:
        # If the target directory does not exist yet, create it safely
        if not os.path.exists(folder_path):
            os.makedirs(folder_path, exist_ok=True)

        # Launch Windows File Explorer pointing to the specific directory
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


def search_web(query):
    """
    Searches Google for the given topic and opens the results in the web browser.

    Returns:
        bool: True if the search URL opened successfully, False otherwise.
    """
    # Remove extra spaces around the query
    clean_query = query.strip()

    # Reject empty queries so we don't open a blank search page
    if len(clean_query) == 0:
        print("\nSearch query cannot be empty.")
        print("Usage: search <topic>  (e.g., search python programming)")
        return False

    print(f"\nSearching for: {clean_query}...")

    # Build the full Google search URL using urllib encoding
    search_url = build_search_url(clean_query)

    # Open the generated URL using our safe website opener function
    return open_website(search_url)


def calculate_expression(expression):
    """
    Safely evaluates a basic math expression containing two numbers and one operator.
    Supported operators: +, -, *, /
    Does NOT use eval() or exec() to ensure strict code safety.

    Returns:
        bool: True if the calculation succeeded, False if input was invalid.
    """
    clean_expr = expression.strip()

    # Check for empty expression
    if not clean_expr:
        print("\nMissing expression to calculate.")
        print("Usage: calculate <num1> <operator> <num2>  (Example: calculate 25 + 50)")
        return False

    # If the expression starts with a minus sign (like -5 + 10),
    # start searching for the operator after the first character so the negative sign isn't mistaken for subtraction.
    if clean_expr.startswith("-"):
        search_start = 1
    else:
        search_start = 0

    found_op = None
    op_pos = -1

    # Search for the first valid arithmetic operator (+, -, *, /)
    for op in ("+", "-", "*", "/"):
        idx = clean_expr.find(op, search_start)
        if idx != -1:
            found_op = op
            op_pos = idx
            break

    # If no recognized operator was found in the text, show an error message
    if found_op is None:
        print(f"\nNo valid operator (+, -, *, /) found in '{clean_expr}'.")
        print("Usage: calculate <num1> <operator> <num2>  (Example: calculate 25 + 50)")
        return False

    # Split the expression into the left number string and right number string
    left_str = clean_expr[:op_pos].strip()
    right_str = clean_expr[op_pos + 1:].strip()

    # Ensure both sides of the operator have content (e.g. reject "50 +")
    if not left_str or not right_str:
        print(f"\nIncomplete expression '{clean_expr}'.")
        print("Usage: calculate <num1> <operator> <num2>  (Example: calculate 25 + 50)")
        return False

    # Convert both number strings into float numbers inside a try/except block
    try:
        num1 = float(left_str)
        num2 = float(right_str)
    except ValueError:
        print(f"\nInvalid numeric values in '{clean_expr}'. Please enter numbers only.")
        return False

    # Perform the arithmetic operation based on the detected operator
    if found_op == "+":
        result = num1 + num2
    elif found_op == "-":
        result = num1 - num2
    elif found_op == "*":
        result = num1 * num2
    elif found_op == "/":
        # Check for division by zero before dividing to avoid ZeroDivisionError crash
        if num2 == 0:
            print("\nError: Division by zero is not allowed.")
            return False
        result = num1 / num2
    else:
        print(f"\nUnsupported operator '{found_op}'.")
        return False

    # Format the result: show whole numbers as integers (e.g. 75 instead of 75.0)
    if result.is_integer():
        display_result = int(result)
    else:
        display_result = round(result, 4)

    # Print the calculation result inside a formatted box
    print_separator("-", 40)
    print("CALCULATION RESULT:")
    print(f"  {clean_expr} = {display_result}")
    print_separator("-", 40)
    return True


def show_time():
    """
    Displays the current system date and time inside a formatted box.
    """
    current_time_str = format_current_time()
    print_separator("-", 40)
    print("CURRENT SYSTEM TIME:")
    print(f"  {current_time_str}")
    print_separator("-", 40)


def show_date():
    """
    Displays the current system date inside a formatted box.
    """
    current_date_str = format_current_date()
    print_separator("-", 40)
    print("CURRENT SYSTEM DATE:")
    print(f"  {current_date_str}")
    print_separator("-", 40)


def show_history():
    """
    Displays a numbered list of all commands entered in the current session.
    Demonstrates using enumerate() with start=1.
    """
    print_separator("-", 40)
    print("COMMAND HISTORY (Current Session):")

    # If no commands have been recorded yet, show a helpful message
    if not SESSION_DATA["history"]:
        print("  No commands recorded yet.")
    else:
        # Loop through command history list and print with numbering
        for idx, cmd in enumerate(SESSION_DATA["history"], start=1):
            print(f"  {idx}. {cmd}")

    print_separator("-", 40)


def show_stats():
    """
    Displays the total, successful, and unknown command counts for the session.
    """
    print_separator("-", 40)
    print("SESSION STATISTICS:")
    print(f"Total commands: {SESSION_DATA['total']}")
    print(f"Successful commands: {SESSION_DATA['successful']}")
    print(f"Unknown commands: {SESSION_DATA['unknown']}")
    print_separator("-", 40)


def show_about():
    """
    Displays project description, course details, and technology stack.
    """
    print_separator("=", 40)
    print("          ABOUT THIS PROJECT")
    print_separator("=", 40)
    print("Voice Command Launcher")
    print("Python Essentials Project")
    print("Command-line based launcher")
    print("Built using Python standard library")
    print_separator("=", 40)


def clear_screen():
    """
    Clears the console screen using our cross-platform utility function.
    """
    clear_terminal()


def show_help():
    """
    Prints a categorized guide of all available commands and helpful tips.
    Demonstrates looping over a tuple of tip strings.
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

    # Loop through the immutable HELP_TIPS tuple and print each tip
    for tip in HELP_TIPS:
        print(f" * {tip}")

    print_separator("=", 40)


def process_command(command):
    """
    Takes user input, cleans and normalizes it, updates session counters,
    and routes the command to the appropriate function using if/elif/else.

    Returns:
        bool: True if the launcher should keep running,
              False if the user entered an exit command.
    """
    # Normalize input: trim extra spaces, convert to lowercase
    normalized = normalize_command(command)

    # If the user entered nothing, prompt them and keep the loop running
    if len(normalized) == 0:
        print("\nNo command entered. Type 'help' to see available commands.")
        return True

    # Record every non-empty input into the session history list and increment total count
    SESSION_DATA["history"].append(command.strip())
    SESSION_DATA["total"] += 1

    # Check for short aliases (e.g., 'yt' -> 'open youtube', 'gh' -> 'open github')
    if normalized in COMMAND_ALIASES:
        normalized = COMMAND_ALIASES[normalized]

    # Check if the user entered a menu number ('1' through '20')
    if normalized in MENU_NUMBER_MAP:
        normalized = MENU_NUMBER_MAP[normalized]

    # 1. Exit Commands (exit, quit, bye, or menu number 20)
    if normalized in EXIT_COMMANDS:
        SESSION_DATA["successful"] += 1
        print("\nThank you for using Voice Command Launcher. Goodbye!\n")
        return False

    # 2. Help Command
    elif normalized in ("help", "show help", "menu", "show menu"):
        SESSION_DATA["successful"] += 1
        show_help()
        return True

    # 3. Command History
    elif normalized in ("history", "show history", "command history"):
        SESSION_DATA["successful"] += 1
        show_history()
        return True

    # 4. Session Statistics
    elif normalized in ("stats", "statistics", "show stats"):
        SESSION_DATA["successful"] += 1
        show_stats()
        return True

    # 5. Clear Screen
    elif normalized == "clear":
        SESSION_DATA["successful"] += 1
        clear_screen()
        return True

    # 6. About Project
    elif normalized in ("about", "show about", "info"):
        SESSION_DATA["successful"] += 1
        show_about()
        return True

    # 7. System Time
    elif normalized in ("show time", "time", "current time", "what time is it"):
        SESSION_DATA["successful"] += 1
        show_time()
        return True

    # 8. System Date
    elif normalized in ("show date", "date", "current date", "today"):
        SESSION_DATA["successful"] += 1
        show_date()
        return True

    # 9. Calculator Commands
    elif normalized.startswith("calculate ") or normalized == "calculate":
        if normalized == "calculate":
            # User typed just "calculate" without an expression
            print("\nPlease provide an expression to calculate.")
            print("Usage: calculate <num1> <operator> <num2>  (Example: calculate 25 + 50)")
            SESSION_DATA["unknown"] += 1
        else:
            # Extract the expression part following the word "calculate"
            clean_input = command.strip()
            parts = clean_input.split(maxsplit=1)
            if len(parts) > 1:
                expr_part = parts[1].strip()
            else:
                expr_part = ""

            # Evaluate the math expression safely without eval()
            success = calculate_expression(expr_part)
            if success:
                SESSION_DATA["successful"] += 1
            else:
                SESSION_DATA["unknown"] += 1
        return True

    # 10. Web Search Commands
    elif normalized.startswith("search ") or normalized == "search" or normalized == "search the web":
        if normalized in ("search", "search the web"):
            # User typed just "search" without a search topic
            print("\nPlease provide a search topic.")
            print("Usage: search <topic>  (Example: search python programming)")
            SESSION_DATA["unknown"] += 1
        else:
            # Extract the search query while preserving original casing
            clean_input = command.strip()
            parts = clean_input.split(maxsplit=1)
            if len(parts) > 1:
                query_part = parts[1].strip()
                # Run the search; increment successful only if browser launch succeeds
                if search_web(query_part):
                    SESSION_DATA["successful"] += 1
                else:
                    SESSION_DATA["unknown"] += 1
            else:
                print("\nPlease provide a search topic.")
                print("Usage: search <topic>  (Example: search python programming)")
                SESSION_DATA["unknown"] += 1
        return True

    # 11. Predefined Website Shortcuts
    elif normalized in WEBSITE_URLS:
        if open_website(normalized):
            SESSION_DATA["successful"] += 1
        else:
            SESSION_DATA["unknown"] += 1
        return True

    # 12. Predefined Windows Applications (Calculator, Notepad)
    elif normalized in APPLICATION_COMMANDS:
        if open_application(normalized):
            SESSION_DATA["successful"] += 1
        else:
            SESSION_DATA["unknown"] += 1
        return True

    # 13. Predefined Windows Folders (Downloads, Documents, Desktop)
    elif normalized in FOLDER_COMMANDS:
        if open_folder(normalized):
            SESSION_DATA["successful"] += 1
        else:
            SESSION_DATA["unknown"] += 1
        return True

    # 14. Incomplete "open" command
    elif normalized == "open":
        SESSION_DATA["unknown"] += 1
        print("\nPlease specify what you want to open.")
        print("Usage: open <website/app/folder>  (Example: open youtube, open calculator, open downloads)")
        print("Type 'help' to see all available commands.")
        return True

    # 15. General unrecognized "open <target>" command
    elif normalized.startswith("open "):
        SESSION_DATA["unknown"] += 1
        target = normalized.replace("open ", "", 1).strip()
        print(f"\nCannot open '{target}'.")
        print("Available options: YouTube, Google, GitHub, Gmail, Wikipedia, Calculator, Notepad, Downloads, Documents, Desktop.")
        print("Type 'help' to see all available commands.")
        return True

    # 16. Completely unrecognized command
    else:
        SESSION_DATA["unknown"] += 1
        print(f"\nCommand not recognized: '{command.strip()}'")
        print("Type 'help' to see available commands.")
        return True
