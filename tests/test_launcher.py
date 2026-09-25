"""
test_launcher.py - Unit Test Suite for Voice Command Launcher

Covers:
1. Command normalization
2. YouTube command recognition & aliases
3. Google command recognition & aliases
4. GitHub command recognition & aliases
5. Additional websites (Gmail, Wikipedia)
6. Search command parsing and URL construction
7. Time command recognition and formatting
8. Date command recognition and formatting
9. Unknown command handling
10. Exit command handling and aliases
11. Application command recognition and safety
12. Folder shortcuts (Downloads, Documents, Desktop)
13. Safe calculator (valid, division by zero, invalid input)
14. Session command history and statistics
15. Clear screen and about commands
"""

import os
import sys
import unittest
from unittest.mock import patch

# Ensure the project root directory is in sys.path for direct script execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from commands import (
    APPLICATION_COMMANDS,
    AVAILABLE_COMMANDS,
    COMMAND_ALIASES,
    EXIT_COMMANDS,
    FOLDER_COMMANDS,
    MENU_NUMBER_MAP,
    WEBSITE_URLS,
)
from launcher import (
    SESSION_DATA,
    calculate_expression,
    clear_screen,
    open_application,
    open_folder,
    open_website,
    process_command,
    reset_session_data,
    search_web,
    show_about,
    show_date,
    show_help,
    show_history,
    show_menu,
    show_stats,
    show_time,
)
from utils import (
    build_search_url,
    clear_terminal,
    format_current_date,
    format_current_time,
    normalize_command,
)


class TestVoiceCommandLauncher(unittest.TestCase):
    """Test suite testing all core components of Voice Command Launcher."""

    def setUp(self):
        """Reset session data before each test."""
        reset_session_data()

    # --------------------------------------------------------------------------
    # 1. Command Normalization Tests
    # --------------------------------------------------------------------------
    def test_normalize_command_strips_and_lowercases(self):
        """Test that extra whitespace is trimmed and text is lowercased."""
        self.assertEqual(normalize_command("  Open YouTube  "), "open youtube")
        self.assertEqual(normalize_command("OPEN GOOGLE"), "open google")
        self.assertEqual(normalize_command("\tSEARCH   python   code \n"), "search python code")

    def test_normalize_command_handles_edge_cases(self):
        """Test normalization with empty strings and non-string types."""
        self.assertEqual(normalize_command(""), "")
        self.assertEqual(normalize_command("   "), "")
        self.assertEqual(normalize_command(123), "123")
        self.assertEqual(normalize_command(None), "")

    # --------------------------------------------------------------------------
    # 2. YouTube Command Recognition & Alias Tests
    # --------------------------------------------------------------------------
    @patch("webbrowser.open")
    def test_youtube_command_recognition(self, mock_browser_open):
        """Test that YouTube commands route correctly to YouTube URL."""
        # Test lowercase
        result = process_command("open youtube")
        self.assertTrue(result)
        mock_browser_open.assert_called_with("https://www.youtube.com")

        # Test mixed case with padding
        mock_browser_open.reset_mock()
        result_upper = process_command("  OPEN YOUTUBE  ")
        self.assertTrue(result_upper)
        mock_browser_open.assert_called_with("https://www.youtube.com")

        # Test menu number 1
        mock_browser_open.reset_mock()
        result_num = process_command("1")
        self.assertTrue(result_num)
        mock_browser_open.assert_called_with("https://www.youtube.com")

    @patch("webbrowser.open")
    def test_aliases(self, mock_browser_open):
        """Test aliases: yt, google, gh map to their respective website targets."""
        # yt alias
        res_yt = process_command("yt")
        self.assertTrue(res_yt)
        mock_browser_open.assert_called_with("https://www.youtube.com")

        # gh alias
        mock_browser_open.reset_mock()
        res_gh = process_command("gh")
        self.assertTrue(res_gh)
        mock_browser_open.assert_called_with("https://www.github.com")

        # google alias
        mock_browser_open.reset_mock()
        res_google = process_command("google")
        self.assertTrue(res_google)
        mock_browser_open.assert_called_with("https://www.google.com")

    # --------------------------------------------------------------------------
    # 3. Google & GitHub Command Recognition Tests
    # --------------------------------------------------------------------------
    @patch("webbrowser.open")
    def test_google_command_recognition(self, mock_browser_open):
        """Test that Google commands route correctly to Google URL."""
        result = process_command("open google")
        self.assertTrue(result)
        mock_browser_open.assert_called_with("https://www.google.com")

        # Test menu number 2
        mock_browser_open.reset_mock()
        result_num = process_command("2")
        self.assertTrue(result_num)
        mock_browser_open.assert_called_with("https://www.google.com")

    @patch("webbrowser.open")
    def test_github_command_recognition(self, mock_browser_open):
        """Test that GitHub commands route correctly to GitHub URL."""
        result = process_command("open github")
        self.assertTrue(result)
        mock_browser_open.assert_called_with("https://www.github.com")

        # Test menu number 3
        mock_browser_open.reset_mock()
        result_num = process_command("3")
        self.assertTrue(result_num)
        mock_browser_open.assert_called_with("https://www.github.com")

    @patch("webbrowser.open")
    def test_new_websites(self, mock_browser_open):
        """Test website shortcuts: Gmail and Wikipedia, and menu numbers 9 and 10."""
        # Gmail
        res_gmail = process_command("open gmail")
        self.assertTrue(res_gmail)
        mock_browser_open.assert_called_with("https://mail.google.com")

        # Menu option 9 (Gmail)
        mock_browser_open.reset_mock()
        res_num9 = process_command("9")
        self.assertTrue(res_num9)
        mock_browser_open.assert_called_with("https://mail.google.com")

        # Wikipedia
        mock_browser_open.reset_mock()
        res_wiki = process_command("open wikipedia")
        self.assertTrue(res_wiki)
        mock_browser_open.assert_called_with("https://www.wikipedia.org")

        # Menu option 10 (Wikipedia)
        mock_browser_open.reset_mock()
        res_num10 = process_command("10")
        self.assertTrue(res_num10)
        mock_browser_open.assert_called_with("https://www.wikipedia.org")

    # --------------------------------------------------------------------------
    # 4. Search Command Parsing Tests
    # --------------------------------------------------------------------------
    def test_build_search_url(self):
        """Test query encoding in search URL builder."""
        url1 = build_search_url("python")
        self.assertEqual(url1, "https://www.google.com/search?q=python")

        url2 = build_search_url("python programming")
        self.assertEqual(url2, "https://www.google.com/search?q=python+programming")

        url3 = build_search_url("data science")
        self.assertEqual(url3, "https://www.google.com/search?q=data+science")

    @patch("webbrowser.open")
    def test_search_command_execution(self, mock_browser_open):
        """Test that search commands parse query and open Google search."""
        result = process_command("search python programming")
        self.assertTrue(result)
        mock_browser_open.assert_called_with(
            "https://www.google.com/search?q=python+programming"
        )

        mock_browser_open.reset_mock()
        result_search = process_command("search data science")
        self.assertTrue(result_search)
        mock_browser_open.assert_called_with(
            "https://www.google.com/search?q=data+science"
        )

    def test_search_web_empty_query(self):
        """Test that an empty search query is rejected safely."""
        result = search_web("   ")
        self.assertFalse(result)

    # --------------------------------------------------------------------------
    # 5. Time & Date Recognition Tests
    # --------------------------------------------------------------------------
    def test_format_current_time(self):
        """Test that time formatting returns a non-empty string with date elements."""
        time_str = format_current_time()
        self.assertIsInstance(time_str, str)
        self.assertGreater(len(time_str), 10)
        self.assertIn("|", time_str)

    def test_format_current_date(self):
        """Test that date formatting returns a valid date string."""
        date_str = format_current_date()
        self.assertIsInstance(date_str, str)
        self.assertGreater(len(date_str), 5)

    @patch("launcher.show_time")
    def test_time_command_recognition(self, mock_show_time):
        """Test that 'show time', 'time', and menu number '7' trigger show_time."""
        result1 = process_command("show time")
        self.assertTrue(result1)
        self.assertEqual(mock_show_time.call_count, 1)

        result2 = process_command("time")
        self.assertTrue(result2)
        self.assertEqual(mock_show_time.call_count, 2)

        result3 = process_command("7")
        self.assertTrue(result3)
        self.assertEqual(mock_show_time.call_count, 3)

    @patch("launcher.show_date")
    def test_date_command(self, mock_show_date):
        """Test that 'show date' and 'date' trigger show_date."""
        result1 = process_command("show date")
        self.assertTrue(result1)
        self.assertEqual(mock_show_date.call_count, 1)

        result2 = process_command("date")
        self.assertTrue(result2)
        self.assertEqual(mock_show_date.call_count, 2)

    # --------------------------------------------------------------------------
    # 6. Unknown Command Handling Tests
    # --------------------------------------------------------------------------
    def test_unknown_command_handling(self):
        """Test that unknown commands do not crash and keep the launcher running."""
        result = process_command("play despacito")
        self.assertTrue(result)

        result2 = process_command("open invalid_program")
        self.assertTrue(result2)

        result3 = process_command("xyz 123 random")
        self.assertTrue(result3)

    def test_empty_command_handling(self):
        """Test that empty or whitespace command does not crash."""
        result = process_command("")
        self.assertTrue(result)
        result_spaces = process_command("     ")
        self.assertTrue(result_spaces)

    # --------------------------------------------------------------------------
    # 7. Exit Command Handling and Aliases Tests
    # --------------------------------------------------------------------------
    def test_exit_command_returns_false(self):
        """Test that exit commands return False to signal loop termination."""
        self.assertFalse(process_command("exit"))
        self.assertFalse(process_command("quit"))
        self.assertFalse(process_command("stop"))
        self.assertFalse(process_command("bye"))
        self.assertFalse(process_command("20"))  # Menu number 20 is Exit

    def test_exit_aliases(self):
        """Test that exit aliases ('exit', 'quit', 'bye') all return False."""
        self.assertFalse(process_command("exit"))
        self.assertFalse(process_command("quit"))
        self.assertFalse(process_command("bye"))

    # --------------------------------------------------------------------------
    # 8. Application Launcher and Safety Tests
    # --------------------------------------------------------------------------
    @patch("subprocess.Popen")
    def test_open_calculator(self, mock_popen):
        """Test launching calculator application on Windows."""
        result = process_command("open calculator")
        self.assertTrue(result)
        mock_popen.assert_called_with(["calc.exe"])

        # Test menu number 4
        mock_popen.reset_mock()
        result_num = process_command("4")
        self.assertTrue(result_num)
        mock_popen.assert_called_with(["calc.exe"])

    @patch("subprocess.Popen")
    def test_open_notepad(self, mock_popen):
        """Test launching notepad application on Windows."""
        result = process_command("open notepad")
        self.assertTrue(result)
        mock_popen.assert_called_with(["notepad.exe"])

        # Test menu number 5
        mock_popen.reset_mock()
        result_num = process_command("5")
        self.assertTrue(result_num)
        mock_popen.assert_called_with(["notepad.exe"])

    @patch("subprocess.Popen")
    def test_arbitrary_command_execution_blocked(self, mock_popen):
        """Safety test: arbitrary command strings must NOT be passed to subprocess."""
        process_command("open powershell")
        mock_popen.assert_not_called()

        process_command("rm -rf /")
        mock_popen.assert_not_called()

        process_command("calc.exe & echo hacked")
        mock_popen.assert_not_called()

    # --------------------------------------------------------------------------
    # 9. Folder Shortcuts Tests
    # --------------------------------------------------------------------------
    @patch("subprocess.Popen")
    def test_folder_commands(self, mock_popen):
        """Test opening Downloads, Documents, and Desktop folders."""
        res_dl = process_command("open downloads")
        self.assertTrue(res_dl)
        self.assertEqual(mock_popen.call_args[0][0][0], "explorer.exe")
        self.assertIn("Downloads", mock_popen.call_args[0][0][1])

        mock_popen.reset_mock()
        res_doc = process_command("open documents")
        self.assertTrue(res_doc)
        self.assertEqual(mock_popen.call_args[0][0][0], "explorer.exe")
        self.assertIn("Documents", mock_popen.call_args[0][0][1])

        mock_popen.reset_mock()
        res_desk = process_command("open desktop")
        self.assertTrue(res_desk)
        self.assertEqual(mock_popen.call_args[0][0][0], "explorer.exe")
        self.assertIn("Desktop", mock_popen.call_args[0][0][1])

    def test_open_folder_invalid(self):
        """Test open_folder returns False for unsupported folder names."""
        self.assertFalse(open_folder("unsupported_folder"))

    # --------------------------------------------------------------------------
    # 10. Safe Calculator Tests
    # --------------------------------------------------------------------------
    def test_calculator_valid_input(self):
        """Test valid calculator expressions (+, -, *, /)."""
        self.assertTrue(calculate_expression("25 + 50"))
        self.assertTrue(calculate_expression("100 / 4"))
        self.assertTrue(calculate_expression("15 * 6"))
        self.assertTrue(calculate_expression("50 - 20"))
        self.assertTrue(process_command("calculate 25 + 50"))
        self.assertTrue(process_command("calculate 100 / 4"))
        self.assertTrue(process_command("calculate 15 * 6"))

    def test_calculator_invalid_input(self):
        """Test invalid calculator inputs (division by zero, syntax errors, empty)."""
        self.assertFalse(calculate_expression("100 / 0"))
        self.assertFalse(calculate_expression("abc + 10"))
        self.assertFalse(calculate_expression("25 ^ 2"))
        self.assertFalse(calculate_expression(""))
        self.assertFalse(calculate_expression("50 +"))

        # Incomplete command 'calculate' prompts user safely
        self.assertTrue(process_command("calculate"))

    # --------------------------------------------------------------------------
    # 11. Command History & Session Statistics Tests
    # --------------------------------------------------------------------------
    @patch("webbrowser.open")
    def test_command_history(self, mock_browser):
        """Test that executed commands are recorded in session history."""
        reset_session_data()
        process_command("open youtube")
        process_command("calculate 10 + 20")
        process_command("history")

        self.assertIn("open youtube", SESSION_DATA["history"])
        self.assertIn("calculate 10 + 20", SESSION_DATA["history"])
        self.assertIn("history", SESSION_DATA["history"])

    @patch("webbrowser.open")
    def test_statistics(self, mock_browser):
        """Test that session statistics correctly count total, successful, and unknown commands."""
        reset_session_data()
        process_command("open youtube")      # successful
        process_command("invalid_cmd_xyz")   # unknown
        process_command("stats")             # successful

        self.assertEqual(SESSION_DATA["total"], 3)
        self.assertEqual(SESSION_DATA["successful"], 2)
        self.assertEqual(SESSION_DATA["unknown"], 1)

    @patch("webbrowser.open", return_value=False)
    def test_statistics_failed_operation(self, mock_browser):
        """Test that failed operations count towards unknown rather than successful."""
        reset_session_data()
        process_command("open youtube")      # browser failure -> counted in unknown
        self.assertEqual(SESSION_DATA["total"], 1)
        self.assertEqual(SESSION_DATA["successful"], 0)
        self.assertEqual(SESSION_DATA["unknown"], 1)

    # --------------------------------------------------------------------------
    # 12. Clear Screen & About Commands Tests
    # --------------------------------------------------------------------------
    @patch("os.system")
    def test_clear_command(self, mock_os_system):
        """Test that the 'clear' command triggers screen clearing safely."""
        result = process_command("clear")
        self.assertTrue(result)
        mock_os_system.assert_called_once()

    @patch("launcher.show_about")
    def test_about_command(self, mock_show_about):
        """Test that 'about' command invokes show_about."""
        result = process_command("about")
        self.assertTrue(result)
        mock_show_about.assert_called_once()

    # --------------------------------------------------------------------------
    # 13. Help, Menu, and Edge Case Tests
    # --------------------------------------------------------------------------
    @patch("launcher.show_help")
    def test_help_command_recognition(self, mock_show_help):
        """Test that 'help', 'show help', and menu option 8 invoke show_help."""
        result = process_command("help")
        self.assertTrue(result)
        self.assertEqual(mock_show_help.call_count, 1)

        result2 = process_command("show help")
        self.assertTrue(result2)
        self.assertEqual(mock_show_help.call_count, 2)

        result3 = process_command("8")
        self.assertTrue(result3)
        self.assertEqual(mock_show_help.call_count, 3)

    def test_show_menu_runs_without_error(self):
        """Test that show_menu executes cleanly."""
        try:
            show_menu()
            success = True
        except Exception:
            success = False
        self.assertTrue(success)

    def test_incomplete_commands_handled_safely(self):
        """Test that incomplete commands like 'open' or 'search' prompt user without crashing."""
        self.assertTrue(process_command("open"))
        self.assertTrue(process_command("search"))
        self.assertTrue(process_command("search the web"))

    def test_open_website_invalid_target(self):
        """Test that open_website returns False for unrecognized website names."""
        self.assertFalse(open_website("nonexistent_site"))

    def test_open_application_unsupported_key(self):
        """Test that open_application returns False for unlisted applications."""
        self.assertFalse(open_application("unsupported_app_key"))


if __name__ == "__main__":
    unittest.main()
