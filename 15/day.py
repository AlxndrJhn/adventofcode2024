import itertools
import os
import re
from collections import defaultdict


this_folder = "\\".join(__file__.split("\\")[:-1])

FREE = "."
WALL = "#"
OBJECT = "O"
ROBOT = "@"

DIR_TO_OFFSET = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}


def add_tuples(t1, t2):
    return tuple(x + y for x, y in zip(t1, t2))


def scalar_mult(s, t):
    return tuple(x * s for x in t)


def sum_gps(map):
    sum_ = 0
    for i, line in enumerate(map):
        for j, c in enumerate(line):
            if c == OBJECT:
                sum_ += 100 * i + j
    return sum_


def main(filename):
    map_str, actions_str = open(f"{this_folder}/{filename}", "r").read().split("\n\n")
    map = [list(line) for line in map_str.split("\n")]
    robot_loc = next(
        (i, j) for i, line in enumerate(map) for j, c in enumerate(line) if c == ROBOT
    )
    map[robot_loc[0]][robot_loc[1]] = FREE
    actions = [x for x in list(actions_str) if x in DIR_TO_OFFSET]

    for action in actions:
        offset = DIR_TO_OFFSET[action]
        new_loc = add_tuples(robot_loc, offset)
        new_field_content = map[new_loc[0]][new_loc[1]]
        if new_field_content == WALL:
            continue
        if new_field_content == FREE:
            robot_loc = new_loc
            continue
        if new_field_content == OBJECT:
            is_free_behind = False
            objects_found = 1
            while True:
                loc_behind = add_tuples(
                    robot_loc, scalar_mult(objects_found + 1, offset)
                )
                content_behind = map[loc_behind[0]][loc_behind[1]]
                if content_behind == WALL:
                    break
                if content_behind == FREE:
                    is_free_behind = True
                    break
                if content_behind == OBJECT:
                    objects_found += 1
            if is_free_behind:
                robot_loc = new_loc
                map[new_loc[0]][new_loc[1]] = FREE
                map[loc_behind[0]][loc_behind[1]] = OBJECT

    # Part 1
    result1 = sum_gps(map)
    print(f"Part 1 {filename}: ", result1)

    # Part 2
    result2 = 24
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        assert main("input_example2.txt") == (2028, 24)
        assert main("input_example.txt") == (10092, 24)
        assert main("input.txt") == (1415498, 24)
    except AssertionError:
        print("❌ wrong")
