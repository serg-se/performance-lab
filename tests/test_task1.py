"""
Tests for 'task1'.
"""

import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "args, expected_output",
    [
        (["4", "3"], "13"),  # 1234 -> 123, 341
        (["5", "4"], "14253"),  # 12345 -> 1234, 4512, 2345, 5123, 3451
        (["1", "1"], "1"),  # 1 -> 1
        (["1", "9"], "1"),  # 1 -> 1
        (["9", "1"], "1"),  # 123456789 -> 1
        (["9", "2"], "123456789"),  # 123456789 -> 12, 23, 34, 45, 56, 67, 78, 89, 91
    ],
)
def test_task1(args, expected_output):
    """Test cmd arguments and check if the output matches the expected values."""

    # Run the script using the current Python executable
    result = subprocess.run(
        [sys.executable, "task1/task1.py", *args],  # Pass dynamic arguments
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.PIPE,  # Capture standard error
        text=True,  # Return the output as a string instead of bytes
    )
    # Check that the script ran successfully (exit code 0)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    # Check that the output matches the expected value
    assert result.stdout.strip() == expected_output, f"Unexpected output: {result.stdout}"
