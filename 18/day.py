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

    def flood_fill(self, start: Loc):
        new_map = Map([list(line) for line in self.data])
        new_map.set(start, 0)
        queue = [start]
        while queue:
            loc = queue.pop(0)
            for direction in [UP, DOWN, LEFT, RIGHT]:
                new_loc = loc + direction
                if new_map.get(new_loc) == ".":
                    new_value = new_map.get(loc) + 1
                    new_map.set(new_loc, new_value)
                    queue.append(new_loc)
                elif isinstance(new_map.get(new_loc), int):
                    assert new_map.get(new_loc) <= new_map.get(loc) + 1
        return new_map


def part1(filename, w_and_h, drop_count):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n")

    m = Map([["." for _ in range(w_and_h + 1)] for _ in range(w_and_h + 1)])

    # Part 1
    for line in input_data[:drop_count]:
        i, j = list(map(int, line.split(",")))
        m.set(Loc(i, j), "#")
    from_start = m.flood_fill(Loc(0, 0))
    result1 = from_start.get(Loc(w_and_h, w_and_h))
    print(f"Part 1 {filename}: ", result1)
    return result1


def part2(filename, w_and_h):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n")

    m = Map([["." for _ in range(w_and_h + 1)] for _ in range(w_and_h + 1)])

    for row_i, line in enumerate(input_data):
        i, j = list(map(int, line.split(",")))
        m.set(Loc(i, j), "#")
        if w_and_h > 50 and row_i < 1024:
            continue
        from_start = m.flood_fill(Loc(0, 0))
        if from_start.get(Loc(w_and_h, w_and_h)) == ".":
            result2 = line
            break
    print(f"Part 2 {filename}: ", result2)
    return result2


if __name__ == "__main__":
    try:
        assert part1("input_example.txt", w_and_h=6, drop_count=12) == 22
        assert part1("input.txt", w_and_h=70, drop_count=1024) == 446
        assert part2("input_example.txt", w_and_h=6) == "6,1"
        assert part2("input.txt", w_and_h=70) == "39,40"
    except AssertionError:
        print("❌ wrong")
