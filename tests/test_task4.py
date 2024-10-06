"""
Tests for 'task4'.
"""

import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "nums_path, expected_output",
    [
        ("tests/task4_cases/1/numbers.txt", "2"),
        ("tests/task4_cases/2/numbers.txt", "16"),
        ("tests/task4_cases/3/numbers.txt", "14"),
    ],
)
def test_task4(nums_path, expected_output):
    """Test numbers.txt and check for correct output."""

    # Run the script using the current Python executable
    result = subprocess.run(
        [sys.executable, "task4/task4.py", nums_path],
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.PIPE,  # Capture standard error
        text=True,  # Return the output as a string instead of bytes
    )
    # Check that the script ran successfully (exit code 0)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    # Check that the output matches the expected value
    assert result.stdout.strip() == expected_output, f"Unexpected output: {result.stdout}"
