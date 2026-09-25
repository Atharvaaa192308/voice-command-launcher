"""
main.py - Entry Point for Voice Command Launcher

This module acts as the application entry point. It controls the main event loop,
tracks session statistics, and orchestrates user interaction.

Demonstrates:
- while loop: continuous event loop
- break: exiting the loop cleanly
- continue: skipping empty or whitespace-only inputs
- Arithmetic operators: incrementing command execution counters
- List operations: appending to session command history
- Exception handling: catching KeyboardInterrupt and EOFError
"""

from launcher import SESSION_DATA, process_command, show_menu


def main() -> None:
    """
    Main application function executing the command-line interface.
    """
    # Show application banner and numbered menu
    show_menu()

    # Loop control variable
    is_running = True

    # Continuous while loop
    while is_running:
        try:
            # Prompt the user for input
            print("\nEnter command:")
            user_input = input("> ")

        except (KeyboardInterrupt, EOFError):
            # Gracefully handle Ctrl+C or terminal EOF
            print("\n\nSession terminated by user. Goodbye!")
            break

        # Check for empty input; use continue to skip to the next iteration
        if len(user_input.strip()) == 0:
            print("No input detected. Please enter a command or type 'help'.")
            continue

        # Process command and determine whether the loop should continue
        is_running = process_command(user_input)

        # Check if exit was requested; use break to terminate the loop
        if not is_running:
            break

    # Summary upon exit using session stats
    if SESSION_DATA["total"] > 0:
        print(f"Session Summary: {SESSION_DATA['total']} command(s) processed.")
        print("Have a great day!\n")


if __name__ == "__main__":
    main()
