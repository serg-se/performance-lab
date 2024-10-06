"""
Tests for 'task3'.
"""

import json
import subprocess
import sys
import tempfile

import pytest


@pytest.mark.parametrize(
    "values_path, tests_path, reference_report_path",
    [
        (
            "tests/task3_cases/1/values.json",
            "tests/task3_cases/1/tests.json",
            "tests/task3_cases/1/report.json",
        ),
        (
            "tests/task3_cases/2/values.json",
            "tests/task3_cases/2/tests.json",
            "tests/task3_cases/2/report.json",
        ),
        (
            "tests/task3_cases/3/values.json",
            "tests/task3_cases/3/tests.json",
            "tests/task3_cases/3/report.json",
        ),
    ],
)
def test_task4(values_path, tests_path, reference_report_path):
    """Test values.json and tests.json and check that report matches the reference report.json."""

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as generated_report:

        # Run the script using the current Python executable
        result = subprocess.run(
            [sys.executable, "task3/task3.py", values_path, tests_path, generated_report.name],
            stdout=subprocess.PIPE,  # Capture standard output
            stderr=subprocess.PIPE,  # Capture standard error
            text=True,  # Return the output as a string instead of bytes
        )

        # Check that the script ran successfully (exit code 0)
        assert result.returncode == 0, f"Script failed with error: {result.stderr}"

        # Read the reference report
        with open(generated_report.name, "r") as f:
            generated_report_content = json.load(f)

        # Read the generated report
        with open(reference_report_path, "r") as f:
            reference_report_content = json.load(f)

        # Compare the generated report content with the reference report content
        assert (
            generated_report_content == reference_report_content
        ), f"Mismatch in generated report: {generated_report.name} vs {reference_report_path}"
