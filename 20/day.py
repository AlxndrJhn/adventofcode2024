import itertools
import os
import re
from collections import defaultdict

this_folder = "\\".join(__file__.split("\\")[:-1])


class Loc:
    row: int
    col: int

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __repr__(self):
        return f"Loc({self.row}, {self.col})"


class Map:
    def __init__(self, data):
        self.data = data
        self.height = len(data)
        self.width = len(data[0])

    def __add__(self, other):
        assert self.height == other.height
        assert self.width == other.width
        new_map = Map([["#" for _ in range(self.width)] for _ in range(self.height)])
        for row in range(self.height):
            for col in range(self.width):
                loc = Loc(row, col)
                if isinstance(self.get(loc), int):
                    new_map.set(loc, self.get(loc) + other.get(loc))
        return new_map

    def find(self, char: str) -> Loc:
        for row in range(self.height):
            for col in range(self.width):
                if self.data[row][col] == char:
                    return Loc(row, col)

    def get(self, loc: Loc):
        return self.data[loc.row][loc.col]

    def get_ij(self, i, j):
        return self.data[i][j]

    def set(self, loc: Loc, value):
        self.data[loc.row][loc.col] = value

    def flood_fill(self, start: Loc, end: Loc):
        new_map = Map([list(line) for line in self.data])
        new_map.set(start, 0)
        new_map.set(end, ".")
        queue = [start]
        while queue:
            loc = queue.pop(0)
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_loc = Loc(loc.row + direction[0], loc.col + direction[1])
                if new_map.get(new_loc) == ".":
                    new_map.set(new_loc, new_map.get(loc) + 1)
                    queue.append(new_loc)
                elif isinstance(new_map.get(new_loc), int):
                    assert new_map.get(new_loc) <= new_map.get(loc) + 1
        return new_map

    def render(self):
        map_str = ""
        for row in self.data:
            map_str += "".join(map(str, row)) + "\n"
        return map_str

    def __str__(self):
        return self.render()


def part1(filename, saving_min):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n")
    map = Map([list(line) for line in input_data])
    s = map.find("S")
    e = map.find("E")

    flood_from_goal = map.flood_fill(e, end=s)
    optimal_length = flood_from_goal.get(s)
    flood_from_start = map.flood_fill(s, end=e)
    summed = flood_from_goal + flood_from_start

    # check horizontal cheats
    cheats_found = set()
    for i in range(0, flood_from_goal.height):
        for j in range(0, flood_from_goal.width - 2):
            left_loc = Loc(i, j)
            left = flood_from_goal.get(left_loc)
            center = flood_from_goal.get_ij(i, j + 1)
            right_loc = Loc(i, j + 2)
            right = flood_from_goal.get(right_loc)
            if not (center == "#" and left != "#" and right != "#"):
                continue
            assert summed.get(left_loc) == summed.get(right_loc) == optimal_length
            improvement = abs(left - right) - 2
            if improvement >= saving_min:
                cheats_found.add((left_loc, right_loc))

    # check vertical cheats
    for i in range(0, flood_from_goal.height - 2):
        for j in range(0, flood_from_goal.width):
            top_loc = Loc(i, j)
            top = flood_from_goal.get(top_loc)
            center = flood_from_goal.get_ij(i + 1, j)
            bottom_loc = Loc(i + 2, j)
            bottom = flood_from_goal.get(bottom_loc)
            if not (center == "#" and top != "#" and bottom != "#"):
                continue
            assert summed.get(top_loc) == summed.get(bottom_loc) == optimal_length
            improvement = abs(top - bottom) - 2
            if improvement >= saving_min:
                cheats_found.add((top_loc, bottom_loc))
    result1 = len(cheats_found)
    print(f"Part 1 {filename}: ", result1)
    return result1


def part2(filename, saving_min):
    input_data = open(f"{this_folder}/{filename}", "r").read().strip().split("\n")
    map = Map([list(line) for line in input_data])

    s = map.find("S")
    e = map.find("E")

    MAX_CHEAT_TIME = 20

    flood_from_goal = map.flood_fill(e, end=s)
    optimal_length = flood_from_goal.get(s)

    result2 = 0
    print(f"Part 2 {filename}: ", result2)
    return result2


if __name__ == "__main__":
    try:
        # Part 1
        assert part1("input_example.txt", saving_min=2) == 44
        assert part1("input.txt", saving_min=100) == 1406

        # Part 2
        assert part2("input_example.txt", saving_min=50) == 285
        # assert part2("input.txt", saving_min=100) == 285

    except AssertionError:
        print("❌ wrong")
