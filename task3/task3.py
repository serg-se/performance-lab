import json
from argparse import ArgumentParser
from pathlib import Path
from typing import Callable


def parse_args() -> dict:
    """Return command-line arguments as a dictionary of key:value pairs."""
    parser = ArgumentParser(description="Generate a test results report.")
    parser.add_argument("values_path", type=Path, help="Path to the test results JSON file.")
    parser.add_argument("tests_path", type=Path, help="Path to the test structure JSON file.")
    parser.add_argument("report_path", type=Path, help="Path to save the generated JSON report.")
    args = parser.parse_args()
    return vars(args)


def join_dict_hook(join_key: str, on_key: str, target_dict: dict) -> Callable:
    """Function serves as an `object_hook` for `json.loads()`. It transforms JSON objects
    as they are being parsed by replacing the value of `join_key` with a corresponding value
    from `target_dict`, using the value of `on_key` as a lookup index.

    Args:
        on_key: Key in JSON dict whose value is the index used to look up in `target_dict`.
        join_key: Key in the JSON dict whose value will be replaced.
        target_dict: Dictionary mapping indexes to new values.

    Returns:
        A hook function to transform each JSON object.

    Example:
        For JSON: {"id": "653", "value": ""}

        And the following hook configuration:
        target_dict = {"653": "passed"}
        transform_data_hook = join_dict_hook(join_key="value", on_key="id", target_dict=target_dict)

        Now, using `json.loads()` with `object_hook=transform_data_hook`,
        the JSON will be transformed to: {"id": "653", "value": "passed"}

    Notes:
        - The `object_hook` is called for every JSON object (i.e., every dictionary) in the
          structure, including nested objects.
        - Non-dictionary types (lists, strings, numbers) are not affected.
    """

    def _hook(json_dict):
        if on_key in json_dict:
            idx = json_dict[on_key]
            if idx in target_dict:
                target_val = target_dict[idx]
                json_dict[join_key] = target_val
        return json_dict

    return _hook


def read_json(file_path: Path, object_hook: Callable = None) -> dict:
    """Read a JSON file and return its data."""
    try:
        return json.loads(file_path.read_text(encoding="utf-8"), object_hook=object_hook)
    except json.decoder.JSONDecodeError as e:
        raise IOError(f"Error decoding json data from {file_path}") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No such file or directory: {file_path}") from e
    except Exception as e:
        raise IOError(f"Unexpected error reading file {file_path}: {e}") from e


def write_json(file: Path, data: dict) -> None:
    """Write data to a JSON file."""
    try:
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    except IOError as e:
        raise IOError(f"Error writing json data to {file}") from e


def make_report(values_path: Path, tests_path: Path, report_path: Path) -> None:
    """Make a report by joining values from a `values` file into a `tests` file.
    Save the resulting report.

    Args:
        values_path: Path to the test results JSON file.
        tests_path: Path to the test structure JSON file.
        report_path: Path to save the generated JSON report.
    """
    try:
        values_data = read_json(values_path)

        # Extract values and create the join hook.
        value_by_id = {data["id"]: data["value"] for data in values_data["values"]}
        object_hook = join_dict_hook(join_key="value", on_key="id", target_dict=value_by_id)
        report_data = read_json(tests_path, object_hook=object_hook)

        write_json(report_path, report_data)

        print("Report generated successfully!")

    except Exception as e:
        print(f"Error: {e}")


def main():
    args = parse_args()
    make_report(**args)


if __name__ == "__main__":
    main()
