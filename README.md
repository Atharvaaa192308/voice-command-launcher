# Voice Command Launcher

> **Python Essentials College Project**  
> Built for the **Python Essentials** course (Vityarthi syllabus).  
> *Note: This is an educational command-line application that simulates voice-style command execution through terminal input. It is NOT a cloud AI voice assistant or commercial speech recognition system.*

---

## 1. Project Overview

The **Voice Command Launcher** is a simple Python command-line launcher for common desktop tasks. It allows users to control routine computer activities—opening popular websites, launching Windows apps and user folders, performing web searches, running basic math calculations, checking command history and session statistics, and viewing system time and date—by typing natural, voice-style commands into the terminal.

Instead of clicking around desktop menus, users can type natural commands like `open youtube`, `search python programming`, `calculate 25 + 50`, `open downloads`, or `history`.

The project is built entirely with the **Python Standard Library** and demonstrates fundamental first-year programming concepts like variables, loops, conditionals, functions, lists, dictionaries, tuples, sets, and basic error handling.

---

## 2. Features

- **Natural Command Input**: Accepts commands regardless of uppercase, lowercase, extra spaces, or mixed case.
- **Website Launcher**: Opens predefined websites (YouTube, Google, GitHub, Gmail, Wikipedia) in your default browser.
- **Command Aliases**: Quick shortcuts like `yt` for YouTube, `google` for Google, and `gh` for GitHub.
- **Application Launcher**: Opens Windows desktop apps (`Calculator`, `Notepad`) safely.
- **Folder Shortcuts**: Opens common user folders (`Downloads`, `Documents`, `Desktop`) in Windows File Explorer.
- **Safe Calculator**: Calculates basic math expressions (`+`, `-`, `*`, `/`) with input validation and zero-division protection without using `eval()`.
- **Web Search**: Searches Google directly from the terminal with safe URL encoding.
- **System Time & Date**: Displays the current local time (`show time`) and date (`show date`).
- **Command History**: Lists all commands entered in the current session with numbers (`history`).
- **Session Statistics**: Displays counts for total, successful, and unknown commands (`stats`).
- **Console Utilities**: Clears the screen (`clear`) and displays project info (`about`).
- **Categorized Help**: Clean, organized help guide (`help`) showing all commands by category.
- **Clean Exit**: Safely closes on `exit`, `quit`, `bye`, or `Ctrl+C`.

---

## 3. Python Concepts Used

This project demonstrates the core topics from the **Python Essentials** course:

| Topic | How It Is Used in the Project |
| :--- | :--- |
| **Variables & Types** | Numbers (`total`, `successful`), text strings (`user_input`, URLs), boolean flags (`is_running`), lists, tuples, sets, and dictionaries. |
| **Input & Output** | `input("> ")` to prompt for commands; formatted `print()` with f-strings for output. |
| **Strings** | `.lower()`, `.strip()`, `.split()`, `.startswith()`, and `.replace()` for cleaning input. |
| **Type Conversion** | Converting user numbers with `float()` and `int()`; string conversion with `str()`. |
| **Operators** | Math (`+`, `-`, `*`, `/`), comparisons (`==`, `!=`, `<`, `>`), logic (`and`, `or`, `not`), and membership (`in`, `not in`). |
| **Lists** | `AVAILABLE_COMMANDS` for the menu; `SESSION_DATA["history"]` for session history. |
| **Tuples** | Fixed application pairs `("Calculator", "calc.exe")` and immutable `HELP_TIPS`. |
| **Sets** | `EXIT_COMMANDS` (`{"exit", "quit", "bye", ...}`) and `CORE_ACTION_KEYWORDS`. |
| **Dictionaries** | Key-value pairs for `WEBSITE_URLS`, `APPLICATION_COMMANDS`, `FOLDER_COMMANDS`, `COMMAND_ALIASES`, and `MENU_NUMBER_MAP`. |
| **Conditions** | `if` / `elif` / `else` branches in `process_command()` to route commands. |
| **Loops** | `while` loop for the main application; `for` loops to display menu items, history, and tips. |
| **Loop Control** | `break` to exit the launcher; `continue` to skip empty input lines. |
| **Functions** | Separate functions for each task (`show_menu`, `open_website`, `open_application`, `calculate_expression`, etc.). |
| **Standard Modules** | `os`, `subprocess`, `webbrowser`, `datetime`, `urllib.parse`, and `unittest`. |
| **Exception Handling** | `try ... except` blocks to catch browser errors, missing files, division by zero, and `KeyboardInterrupt`. |

---

## 4. Project Structure

```text
Voice Command Launcher/
│
├── main.py              # Application entry point & main event loop
├── launcher.py          # Command functions, safe calculator, & command routing
├── commands.py          # Predefined lists, tuples, sets, and dictionaries
├── utils.py             # Helper functions (normalization, URLs, time, date, clear)
├── requirements.txt     # Standard library dependencies declaration
├── statement.md         # Academic problem statement and project scope
├── README.md            # Complete user guide and documentation
│
└── tests/
    ├── __init__.py      # Package initializer for unit testing
    └── test_launcher.py # Automated unit tests using unittest
```

---

## 5. Requirements

- **Python**: Version 3.10+
- **Operating System**: Windows (for application shortcuts `calc.exe`, `notepad.exe` and folder shortcuts)
- **External Dependencies**: **None**. The project uses only standard Python libraries.

---

## 6. Installation & Setup

1. Open your terminal (PowerShell or Command Prompt).
2. Navigate into the project folder:

```powershell
cd "d:\Voice Command Launcher"
```

3. Check your Python version:

```powershell
python --version
```

*(No `pip install` commands are needed because no external libraries are required.)*

---

## 7. How to Run

To run the application, type:

```powershell
python main.py
```

You will see the welcome banner and the menu of available commands:

```text
========================================
        VOICE COMMAND LAUNCHER
========================================
Available commands:

1. Open YouTube
2. Open Google
3. Open GitHub
4. Open Calculator
5. Open Notepad
6. Search the Web
7. Show Time
8. Show Help
9. Open Gmail
10. Open Wikipedia
11. Open Downloads
12. Open Documents
13. Open Desktop
14. Calculate (e.g. 25 + 50)
15. Show Date
16. Command History
17. Session Statistics
18. Clear Screen
19. About Project
20. Exit

Type "help" to see available commands.

Enter command:
> 
```

---

## 8. Available Commands

You can type the command name, an alias, or the menu number:

| Category | Command | Shortcut / Alias | Description |
| :--- | :--- | :--- | :--- |
| **Websites** | `open youtube` | `1` or `yt` | Opens YouTube in default browser |
| **Websites** | `open google` | `2` or `google` | Opens Google Search homepage |
| **Websites** | `open github` | `3` or `gh` | Opens GitHub in default browser |
| **Websites** | `open gmail` | `9` or `gmail` | Opens Gmail inbox |
| **Websites** | `open wikipedia` | `10` or `wikipedia`| Opens Wikipedia homepage |
| **Applications** | `open calculator` | `4` or `calculator`| Launches Windows Calculator |
| **Applications** | `open notepad` | `5` or `notepad` | Launches Windows Notepad |
| **Folders** | `open downloads` | `11` or `downloads`| Opens Downloads folder in File Explorer |
| **Folders** | `open documents` | `12` or `documents`| Opens Documents folder in File Explorer |
| **Folders** | `open desktop` | `13` or `desktop` | Opens Desktop folder in File Explorer |
| **Utilities** | `search <topic>` | `6` (prompts) | Searches Google for the given topic |
| **Utilities** | `calculate <expression>` | `14` (e.g. `calculate 25 + 50`) | Evaluates basic math expression |
| **Utilities** | `show time` | `7` or `time` | Displays system date and time |
| **Utilities** | `show date` | `15` or `date` | Displays system date |
| **System** | `history` | `16` | Displays session command history |
| **System** | `stats` | `17` | Displays session statistics |
| **System** | `clear` | `18` | Clears the terminal screen |
| **System** | `about` | `19` | Displays project information |
| **System** | `help` | `8` or `show help` | Displays the detailed command guide |
| **System** | `exit` | `20`, `quit`, or `bye` | Closes the launcher cleanly |

---

## 9. Example Usage

### Example 1: Opening Websites & Using Aliases
```text
Enter command:
> yt

Opening Youtube...
```

### Example 2: Performing Calculations Safely
```text
Enter command:
> calculate 25 + 50
----------------------------------------
CALCULATION RESULT:
  25 + 50 = 75
----------------------------------------
```

### Example 3: Opening Folders
```text
Enter command:
> open downloads

Opening Downloads folder...
```

### Example 4: Checking System Date
```text
Enter command:
> show date
----------------------------------------
CURRENT SYSTEM DATE:
  Friday, 25 September 2026
----------------------------------------
```

### Example 5: Reviewing Command History
```text
Enter command:
> history
----------------------------------------
COMMAND HISTORY (Current Session):
  1. yt
  2. calculate 25 + 50
  3. open downloads
  4. history
----------------------------------------
```

### Example 6: Checking Session Statistics
```text
Enter command:
> stats
----------------------------------------
SESSION STATISTICS:
Total commands: 5
Successful commands: 5
Unknown commands: 0
----------------------------------------
```

### Example 7: Exiting the Application
```text
Enter command:
> bye

Thank you for using Voice Command Launcher. Goodbye!

Session Summary: 6 command(s) processed.
Have a great day!
```

---

## 10. Testing

The project includes unit tests using Python's built-in `unittest` module.

### How to Run the Tests:

Run the following command from the project root:

```powershell
python -m unittest discover -s tests -v
```

### What the Tests Verify:
1. **Command Normalization**: Tests cleaning of uppercase, mixed case, and extra spaces.
2. **Websites & Aliases**: Checks URL matching for all 6 websites and aliases (`yt`, `google`, `gh`).
3. **App & Folder Launching**: Verifies predefined apps (`calc.exe`, `notepad.exe`) and folders (`Downloads`, `Documents`, `Desktop`).
4. **Safe Calculator**: Verifies math operations (`+`, `-`, `*`, `/`) and error handling for division by zero and invalid input without `eval()`.
5. **Search Query Builder**: Asserts safe encoding of search queries.
6. **Date & Time Formats**: Verifies correct output from `datetime`.
7. **Session History & Stats**: Confirms that command history and counters update accurately.
8. **Input Validation**: Ensures empty input, incomplete commands, and unknown words do not crash the app.
9. **Exit Commands**: Asserts that `exit`, `quit`, and `bye` terminate the loop.

---

## 11. Limitations

- **Terminal Text Input**: Commands are typed in the terminal. The project does not currently record audio from a microphone.
- **Windows Specific**: App shortcuts (`calc.exe`, `notepad.exe`) and folder paths are configured for Windows.
- **Predefined Options Only**: Only predefined websites, apps, and folders can be opened. Arbitrary commands are blocked for safety.
- **Internet Connection**: Web searches and website opening require an active internet connection.

---

## 12. Future Enhancements

- **Microphone Voice Input (Future)**: Add an optional speech recognition module using a library like `SpeechRecognition` to capture spoken voice.
- **Text-to-Speech Output (Future)**: Add optional audio voice feedback using a library like `pyttsx3`.
- **Cross-Platform Compatibility (Future)**: Detect the operating system (Windows, macOS, Linux) to open system-specific apps.
- **Custom Configuration (Future)**: Allow users to add their favorite websites and folders in a simple text or JSON file.
