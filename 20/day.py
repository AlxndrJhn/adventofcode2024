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
        if loc.row < 0 or loc.row >= self.height:
            return None
        if loc.col < 0 or loc.col >= self.width:
            return None
        return self.data[loc.row][loc.col]

    def get_ij(self, i, j):
        return self.data[i][j]

    def set(self, loc: Loc, value):
        self.data[loc.row][loc.col] = value

    def flood_fill(self, start: Loc, end: Loc, max_time=None, fillable_char="."):
        new_map = Map([list(line) for line in self.data])
        new_map.set(start, 0)
        new_map.set(end, fillable_char)
        queue = [start]
        while queue:
            loc = queue.pop(0)
            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                new_loc = Loc(loc.row + direction[0], loc.col + direction[1])
                if new_map.get(new_loc) == fillable_char:
                    new_value = new_map.get(loc) + 1
                    new_map.set(new_loc, new_value)
                    if max_time is not None and new_value >= max_time:
                        continue
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
    flood_from_start = map.flood_fill(s, end=e)
    optimal_length = flood_from_goal.get(s)

    cheats_per_savings = defaultdict(set)
    for i in tqdm(range(0, flood_from_goal.height)):
        for j in range(0, flood_from_goal.width):
            starting_loc = Loc(i, j)
            if map.get(starting_loc) in ["#", "E"]:
                continue
            cost_at_start = flood_from_start.get(starting_loc)
            for offset_i in range(-MAX_CHEAT_TIME, MAX_CHEAT_TIME + 1):
                for offset_j in range(-MAX_CHEAT_TIME, MAX_CHEAT_TIME + 1):
                    cost_during = abs(offset_i) + abs(offset_j)
                    if cost_during > MAX_CHEAT_TIME or cost_during == 0:
                        continue
                    exit_point = starting_loc + Loc(offset_i, offset_j)
                    if exit_point.row < 0 or exit_point.row >= flood_from_goal.height:
                        continue
                    if exit_point.col < 0 or exit_point.col >= flood_from_goal.width:
                        continue
                    if map.get(exit_point) in ["#", "S"]:
                        continue

                    cost_to_end = flood_from_goal.get(exit_point)
                    total_cost = cost_at_start + cost_during + cost_to_end
                    savings = optimal_length - total_cost

                    if savings >= saving_min:
                        cheats_per_savings[savings].add((starting_loc, exit_point))

    keys_sorted = sorted(cheats_per_savings.keys())
    for key in keys_sorted:
        print(
            f"There are {len(cheats_per_savings[key])} cheats that save {key} picoseconds."
        )

    result2 = sum(len(cheats) for cheats in cheats_per_savings.values())
    print(f"Part 2 {filename}: ", result2)
    return result2


if __name__ == "__main__":
    try:
        # Part 1
        assert part1("input_example.txt", saving_min=2) == 44
        assert part1("input.txt", saving_min=100) == 1406

        # Part 2
        assert part2("input_example.txt", saving_min=50) == 285
        assert part2("input.txt", saving_min=100) == 1006101

    except AssertionError:
        print("❌ wrong")
