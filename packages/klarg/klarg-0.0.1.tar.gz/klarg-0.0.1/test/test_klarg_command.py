import sys
import os

sys.path.append(
     os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import klarg

ALL_ARGS = [
    "--some-number",
    "10",
    "--not-number",
    "1a",
    "--number-no-args",
    "-n"
]


class TestKlarg():

    def __init__(self):
        self.test_command = klarg.command("test")
        self.test_get_all()
        self.test_get_bool()
        self.test_exists()
        self.test_get_str()
        self.test_get_num()

    def test_get_all(self):
        """
        Tests that klarg.get_all() actually returns all the arguments possible

        """

        assert self.test_command.get_all() == ALL_ARGS

    def test_get_bool(self):
        """
        Tests that klarg.get_bool() returns if the argument exists or not.

        """

        # Tests that whena multi-letter flag is there,
        # but a single letter flag is not, klar.get_bool() returns True.
        assert self.test_command.get_bool("some-number", "s") is True

        # Tests that when both the shortened and non-shortened flags are
        # present, klarg.get_bool() returns True.
        assert self.test_command.get_bool("not-number", "n") is True

        # Tests that when a multi letter flag is not there but a shortened
        # flag is present, klarg.get_bool() returns True.
        assert self.test_command.get_bool("non-existent-args", "n") is True

        # Tests that when neither the single nor the multi letter flag is
        # present, the klarg.get_bool() returns False.
        assert self.test_command.get_bool("non-existent-args", "s") is False

    def test_exists(self):
        """
        Tests that klarg.exists() returns whether the given string exists in
        the command line arguments
        """

        # Tests that klarg.exists() returns True for existing command line
        # arguments
        assert self.test_command.exists("10") is True

        # Tests that klarg.exists() returns False for non existing
        # command line arguments
        assert self.test_command.exists("--non-existent-args") is False

    def test_get_str(self):
        """
        Tests that klarg.get_str() returns the correct values
        and also raises the right errors at the right
        conditions.
        """

        def handle_err_none():
            print("HANDLE_ERR_NONE works")

        def handle_err_mul():
            print("HANDLE_ERR_MUL works")

        handle_errors = {
            "ERR_NONE": handle_err_none,
            "ERR_MUL": handle_err_mul
        }

        # Tests klarg.get_str() returns the correct string
        assert self.test_command.get_str("some-number") == "10"

        # Tests klarg.get_str() returns the correct string
        assert self.test_command.get_str("not-number") == "1a"

        # Tests that klarg.get_str() raises the right errors
        # This should raise ERR_NONE
        should_raise_none = self.test_command.get_str(
            "number-no-args",
            on_error=handle_errors
        )
        assert should_raise_none is None

        # Tests that klarg.get_str() raises the right errors
        # This should raise ERR_MUL
        should_raise_none = self.test_command.get_str(
            "number-no-args",
            "s",
            on_error=handle_errors
        )
        assert should_raise_none is None

    def test_get_num(self):
        """
        Tests that klarg.get_num() returns that correct values
        and also raises the right errors at the right conditions.
        """

        def handle_err_num(value):
            print("HANDLE_ERR_NUM works")
            print("    Incorrect value is supposed to be 1a")
            print(f"    Incorrect value is: {value}")

        handle_errors = {
            "ERR_NUM": handle_err_num
        }

        assert self.test_command.get_num("some-number") == 10

        should_raise_errors = self.test_command.get_num(
            "not-number",
            on_error=handle_errors
        )

        assert should_raise_errors is None


TestKlarg()
print("All Tests Passed")
