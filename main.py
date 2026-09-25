"""
main.py - Entry Point for Voice Command Launcher

This module is the starting point of the Voice Command Launcher.
It runs the main interactive loop, prompts the user for typed voice-style
commands, calls the command processor, and prints a session summary on exit.

Python Essentials concepts demonstrated:
- while loop: runs the continuous command-line interface loop
- break: exits the loop cleanly when the user quits or presses Ctrl+C
- continue: skips empty input and prompts again
- try / except: handles keyboard interrupts (Ctrl+C) and EOF signals safely
- if / elif / else: checks loop state and decides when to exit
- Functions and module imports: connects launcher functions together
"""

from launcher import SESSION_DATA, process_command, show_menu


def main():
    """
    Main function that runs the interactive command-line interface.
    """
    # Display the welcome banner and the 20 numbered menu options
    # so the user knows what commands are available right away.
    show_menu()

    # This boolean variable controls the continuous loop.
    # When process_command() returns False (on exit), is_running becomes False.
    is_running = True

    # Main event loop: keeps asking the user for commands until they decide to exit.
    while is_running:
        try:
            # Prompt the user to enter a command.
            print("\nEnter command:")
            user_input = input("> ")

        except (KeyboardInterrupt, EOFError):
            # If the user presses Ctrl+C or sends an end-of-file signal,
            # catch the exception so the program exits cleanly without an error message.
            print("\n\nSession terminated by user. Goodbye!")
            break

        # If the user just pressed Enter without typing anything,
        # skip processing and ask for input again.
        if len(user_input.strip()) == 0:
            print("No input detected. Please enter a command or type 'help'.")
            continue

        # Pass the input to process_command() in launcher.py.
        # It handles the command and returns:
        # - True: if the program should keep running
        # - False: if the user typed an exit command
        is_running = process_command(user_input)

        # If the user requested to exit, break out of the while loop immediately.
        if not is_running:
            break

    # After exiting the loop, print a brief summary of how many commands were run.
    if SESSION_DATA["total"] > 0:
        print(f"Session Summary: {SESSION_DATA['total']} command(s) processed.")
        print("Have a great day!\n")


if __name__ == "__main__":
    main()
