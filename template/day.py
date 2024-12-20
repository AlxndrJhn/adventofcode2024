import itertools
import os
import re
from collections import defaultdict

from tqdm import tqdm

this_folder = "\\".join(__file__.split("\\")[:-1])


class Loc:
    row: int
    col: int

    def __init__(self, row, col, repr_char=None):
        self.row = row
        self.col = col
        self.repr_char = repr_char

    def __repr__(self):
        if self.repr_char is None:
            return f"Loc({self.row}, {self.col})"
        return self.repr_char

    def __add__(self, other):
        return Loc(self.row + other.row, self.col + other.col)

    def __hash__(self):
        return hash((self.row, self.col))

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col


UP = Loc(-1, 0, "^")
DOWN = Loc(1, 0, "v")
LEFT = Loc(0, -1, "<")
RIGHT = Loc(0, 1, ">")
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


class Map:
    def __init__(self, data):
        self.data = data
        self.height = len(data)
        self.width = len(data[0])

    def print(self):
        for row in self.data:
            print("".join(map(str, row)))
        print()

    def find(self, char: str) -> Loc:
        for row in range(self.height):
            for col in range(self.width):
                if self.data[row][col] == char:
                    return Loc(row, col)

    def get(self, loc: Loc):
        if loc.row < 0 or loc.row >= self.height:
            return None
        if loc.col < 0 or loc.col >= self.width:
            return None
        return self.data[loc.row][loc.col]

    def set(self, loc: Loc, value):
        self.data[loc.row][loc.col] = value


def main(filename):
    input_data = open(f"{this_folder}/{filename}", "r").read().split("\n")
    map = Map([list(line) for line in input_data])

    # Part 1
    result1 = 42
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example.txt") == (42, 24)
        # assert main("input.txt") == (42, 24)
    except AssertionError:
        print("❌ wrong")
