import math
from argparse import ArgumentParser
from pathlib import Path
from typing import Iterable


def parse_args() -> dict:
    """Return command-line arguments as a dictionary of key:value pairs."""
    parser = ArgumentParser(description="Calculates the dot intersections with the circle.")
    parser.add_argument("circle_path", type=Path, help="Path to circle coordinates TXT file.")
    parser.add_argument("dots_path", type=Path, help="Path to dot coordinates TXT file.")
    args = parser.parse_args()
    return vars(args)


def read_circle_coordinates(file_path: Path) -> tuple[tuple[int, int], int]:
    """Read TXT file and return a circle center coordinate and its radius."""
    try:
        with file_path.open("r", encoding="utf-8") as txt_file:
            x, y = map(int, next(txt_file).strip().split())
            radius = int(next(txt_file).strip())
            return (x, y), radius
    except ValueError as e:
        raise ValueError(f"File contains invalid integer values: {e}") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No such file or directory: {file_path}") from e
    except Exception as e:
        raise IOError(f"Unexpected error reading file {file_path}: {e}") from e


def read_dot_coordinates(file_path: Path) -> list[tuple[int, int]]:
    """Read TXT file and return a list of dot coordinates."""
    try:
        with file_path.open("r", encoding="utf-8") as txt_file:
            res = []
            for line in txt_file:
                x, y = map(int, line.strip().split())
                res.append((x, y))
            return res
    except ValueError as e:
        raise ValueError(f"File contains invalid integer values: {e}") from e
    except FileNotFoundError as e:
        raise FileNotFoundError(f"No such file or directory: {file_path}") from e
    except Exception as e:
        raise IOError(f"Unexpected error reading file {file_path}: {e}") from e


def isect_circle(
    circle_co: tuple[int, int], circle_radius: int, dots_co: list[tuple[int, int]]
) -> Iterable[int]:
    """Generate the intersections of the circle and the dots.

    Args:
        circle_co: Coordinate of the center of the circle.
        circle_radius: Radius of the circle.
        dots_co: List of coordinates of the dots.

    Yields:
        0 if the dot is on the circle edge, 1 if inside, and 2 if outside.
    """

    for point_co in dots_co:
        dist = math.dist(point_co, circle_co)
        if dist < circle_radius:  # Inside
            yield 1
        elif dist > circle_radius:  # Outside
            yield 2
        else:  # On the edge
            yield 0


def print_circle_intersections(circle_path: Path, dots_path: Path) -> None:
    """Print the intersections of the circle and the dots.

    Args:
        circle_path: Path to the file containing the circle's data.
        dots_path: Path to the file containing the dots' data.
    """
    try:
        circle_co, circle_radius = read_circle_coordinates(circle_path)
        dots_co = read_dot_coordinates(dots_path)
        res = isect_circle(circle_co, circle_radius, dots_co)
        print(*res, sep="\n")

    except Exception as e:
        print(f"Error: {e}")


def main():
    kwargs = parse_args()
    print_circle_intersections(**kwargs)


if __name__ == "__main__":
    main()
