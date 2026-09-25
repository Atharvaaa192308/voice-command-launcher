# Project Statement — Voice Command Launcher

## 1. Problem Statement
When using a computer, people often repeat simple daily tasks such as opening web browsers, searching on Google, checking the time and date, doing quick math, or finding apps like Calculator and Notepad. 

This project solves this by creating a simple Python command-line launcher. Instead of clicking around desktop menus, users can type natural voice-style commands into the terminal (such as `open youtube`, `calculate 25 + 50`, or `open calculator`) to quickly launch websites, run tools, and open common folders.

---

## 2. Project Purpose
The purpose of the **Voice Command Launcher** is to:
1. Build a beginner-friendly Python command-line launcher for common desktop tasks.
2. Demonstrate core first-year Python concepts from the **Python Essentials** course (variables, strings, loops, functions, lists, dictionaries, tuples, sets, and basic error handling).
3. Keep the code safe by allowing only predefined websites, apps, and folders to open.

---

## 3. Target Users
- **First-Year Programming Students**: Learning Python basics through a practical project.
- **Course Evaluators and Teachers**: Reviewing clean, modular student code that follows the course syllabus.
- **Everyday Desktop Users**: Looking for a fast terminal shortcut tool for routine tasks on Windows.

---

## 4. Scope

### In Scope (Currently Implemented):
- Runs in a continuous terminal loop.
- Cleans and normalizes user input (handles uppercase, lowercase, extra spaces).
- Opens predefined websites (YouTube, Google, GitHub, Gmail, Wikipedia) in the default browser.
- Supports short aliases (`yt`, `google`, `gh`, etc.).
- Launches Windows desktop applications (Calculator, Notepad).
- Opens common Windows user folders (Downloads, Documents, Desktop).
- Performs safe arithmetic calculations (`+`, `-`, `*`, `/`) without using `eval()`.
- Searches Google using the browser.
- Shows system time and date.
- Tracks command history and session statistics (`total`, `successful`, `unknown`).
- Provides terminal clearing (`clear`), project info (`about`), and a categorized help guide (`help`).
- Tested with automated unit tests using Python's standard `unittest` module.

### Out of Scope:
- Microphone audio recording or speech-to-text processing (commands are typed into the terminal).
- Running arbitrary shell commands or unlisted programs.
- Web scraping or online APIs.
- Graphical User Interfaces (GUIs) or web frameworks.

---

## 5. Main Features
1. **Command Processing**: Normalizes input using string methods (`lower()`, `strip()`, `split()`).
2. **Website Launcher**: Opens predefined websites and aliases in the web browser.
3. **Application & Folder Launcher**: Safely opens Calculator, Notepad, Downloads, Documents, and Desktop.
4. **Safe Calculator**: Calculates basic math expressions safely without `eval()`, with checks for division by zero.
5. **Web Search**: Creates search URLs with safe encoding and opens Google Search.
6. **Time & Date**: Displays current system time and date using `datetime`.
7. **Session History & Stats**: Shows commands entered in the current run and counts successful/unknown commands.
8. **Navigation & Help**: Supports voice-style phrases, numbered menu options, and clean categorized help.
9. **Safe Exit**: Closes cleanly on `exit`, `quit`, `bye`, or `Ctrl+C`.

---

## 6. Python Concepts Used

| Python Concept | How It Is Used in the Project |
| :--- | :--- |
| **Variables & Types** | Numbers (`total`, `successful`), text strings (`user_input`, URLs), boolean flags (`is_running`), lists, tuples, sets, and dictionaries. |
| **Input & Output** | `input("> ")` to get user commands; formatted `print()` with f-strings for output. |
| **Strings** | `.lower()`, `.strip()`, `.split()`, `.startswith()`, and `.replace()` for cleaning input. |
| **Type Conversion** | Converting user numbers with `float()` and `int()`; string conversion with `str()`. |
| **Operators** | Math (`+`, `-`, `*`, `/`), comparisons (`==`, `!=`, `<`, `>`), logic (`and`, `or`, `not`), and membership (`in`, `not in`). |
| **Lists** | `AVAILABLE_COMMANDS` for the menu list; `SESSION_DATA["history"]` for session history. |
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

## 7. Current Limitations
1. **Typed Voice-Style Input**: Commands are typed in the terminal. Direct microphone audio input is not supported.
2. **Windows Specific**: App shortcuts (`calc.exe`, `notepad.exe`) and folder shortcuts use Windows paths.
3. **Predefined Options Only**: Only predefined websites, apps, and folders can be opened.
4. **Internet Needed for Web Actions**: Opening websites and web search require an internet connection.

---

## 8. Future Scope (Planned Enhancements)
1. **Microphone Voice Input (Future)**: Add an optional audio module using a speech recognition library to listen to spoken commands.
2. **Text-to-Speech Responses (Future)**: Add optional voice replies using a text-to-speech library.
3. **Cross-Platform Support (Future)**: Add support for macOS and Linux commands using `platform.system()`.
4. **Custom Config File (Future)**: Allow users to add their own websites and folder paths in a JSON settings file.
