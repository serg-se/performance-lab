"""
Tests for 'task2'.
"""

import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "circle_path, dot_path, expected_output",
    [
        ("tests/task2_cases/1/circle.txt", "tests/task2_cases/1/dot.txt", "1\n0\n2"),
        ("tests/task2_cases/2/circle.txt", "tests/task2_cases/2/dot.txt", "0\n0\n0\n2\n0"),
        ("tests/task2_cases/3/circle.txt", "tests/task2_cases/3/dot.txt", "1\n0\n0\n2\n1"),
        ("tests/task2_cases/4/circle.txt", "tests/task2_cases/4/dot.txt", "1\n0\n0\n1"),
    ],
)
def test_task4(circle_path, dot_path, expected_output):
    """Test circle.txt and dot.txt and check for correct output."""

    # Run the script using the current Python executable
    result = subprocess.run(
        [sys.executable, "task2/task2.py", circle_path, dot_path],
        stdout=subprocess.PIPE,  # Capture standard output
        stderr=subprocess.PIPE,  # Capture standard error
        text=True,  # Return the output as a string instead of bytes
    )
    # Check that the script ran successfully (exit code 0)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    # Check that the output matches the expected value
    assert result.stdout.strip() == expected_output, f"Unexpected output: {result.stdout}"
