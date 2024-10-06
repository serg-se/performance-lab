from argparse import ArgumentParser
from typing import Iterable


def parse_args() -> dict:
    """Return command-line arguments as a dictionary of key:value pairs."""
    parser = ArgumentParser(description="Generate a circular array traversal path.")
    parser.add_argument("n", type=int, help="Size of the array")
    parser.add_argument("m", type=int, help="Step size for traversal")
    args = parser.parse_args()
    if args.n < 1:
        parser.error("Array size must be at least 1.")
    if args.m == 0:
        parser.error("Step size cannot be 0.")
    return vars(args)


def get_circular_array_path(n: int, m: int) -> Iterable[int]:
    """Generate a path that, moving at intervals of length m through a given array,
    the end will be the first element.

    Args:
        n: The size of the array.
        m: The step size for traversal.

    Yields:
        The current position in the array (1-indexed) at each step.
    """
    cur_num = 0
    while True:
        yield cur_num + 1  # Convert to 1-based num
        cur_num = (cur_num + m - 1) % n
        if cur_num == 0:
            break


def print_circular_array_path(n: int, m: int) -> None:
    """Print the circular array traversal path based on the given n and m.

    Args:
        n: The size of the array.
        m: The step size for traversal.
    """
    path = get_circular_array_path(n, m)
    print(*path, sep="")


def main():
    args = parse_args()
    print_circular_array_path(**args)


if __name__ == "__main__":
    main()
