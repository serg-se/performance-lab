import statistics
from argparse import ArgumentParser
from pathlib import Path
from typing import Iterable


def parse_args() -> dict:
    """Return command-line arguments as a dictionary of key:value pairs."""
    parser = ArgumentParser(description="Calculate the minimum number of turns.")
    parser.add_argument("nums_path", type=Path, help="Path to the nums array TXT file.")
    args = parser.parse_args()
    return vars(args)


def read_nums(nums_path: Path) -> list[int]:
    """Read a TXT file and return a list of integers."""
    try:
        with nums_path.open("r", encoding="utf-8") as txt_file:
            return [int(line.strip()) for line in txt_file]
    except ValueError as e:
        raise ValueError(f"File contains invalid integer values: {e}") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No such file or directory: {nums_path}") from e
    except Exception as e:
        raise IOError(f"Unexpected error reading file {nums_path}: {e}") from e


def get_min_turns(nums: Iterable[int]) -> int:
    """Return the minimum number of turns required to make all the elements equal."""
    median = statistics.median_low(nums)
    return sum(abs(num - median) for num in nums)


def print_min_turns(nums_path: Path) -> None:
    """Read nums from the file and print the minimum number of turns."""
    try:
        nums = read_nums(nums_path)
        min_turns = get_min_turns(nums)
        print(min_turns)

    except Exception as e:
        print(f"Error: {e}")


def main():
    kwargs = parse_args()
    print_min_turns(**kwargs)


if __name__ == "__main__":
    main()
