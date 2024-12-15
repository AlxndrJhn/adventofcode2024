from hmac import new
import itertools
import os
import re
from collections import defaultdict
from webbrowser import get

from numpy import add


this_folder = "\\".join(__file__.split("\\")[:-1])

FREE = "."
WALL = "#"
OBJECT = "O"
WIDE_BOX = ["[", "]"]
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
            if c == OBJECT or c == WIDE_BOX[0]:
                sum_ += 100 * i + j
    return sum_


def widen_map(map):
    new_map = []
    for i, line in enumerate(map):
        new_line = []
        for j, c in enumerate(line):
            if c == WALL:
                new_line.extend([WALL, WALL])
            elif c == OBJECT:
                new_line.extend(WIDE_BOX)
            elif c == FREE:
                new_line.extend([FREE, FREE])
            elif c == ROBOT:
                new_line.extend([ROBOT, FREE])
        new_map.append(new_line)
    return new_map


def get_wide_box_locs(map, loc):
    content_at_loc = map[loc[0]][loc[1]]
    assert content_at_loc in WIDE_BOX
    if content_at_loc == WIDE_BOX[0]:
        return {loc, add_tuples(loc, (0, 1))}
    return {add_tuples(loc, (0, -1)), loc}


def render_map(map, robot_loc):
    map = [line.copy() for line in map]
    map[robot_loc[0]][robot_loc[1]] = ROBOT
    for line in map:
        print("".join(line))
    print()


def main(filename):
    map_str, actions_str = open(f"{this_folder}/{filename}", "r").read().split("\n\n")
    original_map = [list(line) for line in map_str.split("\n")]
    map = [line.copy() for line in original_map]
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
    map = widen_map(original_map)
    robot_loc = next(
        (i, j) for i, line in enumerate(map) for j, c in enumerate(line) if c == ROBOT
    )
    map[robot_loc[0]][robot_loc[1]] = FREE
    for action in actions:
        # render_map(map, robot_loc)
        offset = DIR_TO_OFFSET[action]
        new_loc = add_tuples(robot_loc, offset)
        new_field_content = map[new_loc[0]][new_loc[1]]
        if new_field_content == WALL:
            continue
        if new_field_content == FREE:
            robot_loc = new_loc
            continue
        if new_field_content in WIDE_BOX:
            is_free_behind = True
            objects_to_move = get_wide_box_locs(map, new_loc)
            to_explore = [add_tuples(o, offset) for o in objects_to_move]
            while to_explore:
                loc = to_explore.pop()
                if loc in objects_to_move:
                    continue
                content_behind = map[loc[0]][loc[1]]
                if content_behind == WALL:
                    is_free_behind = False
                    break
                if content_behind == FREE:
                    continue
                if content_behind in WIDE_BOX:
                    additional_objects = get_wide_box_locs(map, loc)
                    objects_to_move = objects_to_move.union(additional_objects)
                    to_explore.extend(
                        [add_tuples(o, offset) for o in additional_objects]
                    )
            if is_free_behind:
                robot_loc = new_loc
                new_locs = []
                for i, j in objects_to_move:
                    content = map[i][j]
                    new_locs.append((content, add_tuples((i, j), offset)))
                for o in objects_to_move:
                    map[o[0]][o[1]] = FREE
                for content, (i, j) in new_locs:
                    map[i][j] = content
    result2 = sum_gps(map)
    print(f"Part 2 {filename}: ", result2)
    return result1, result2


if __name__ == "__main__":
    try:
        # assert main("input_example2.txt") == (2028, 24)
        assert main("input_example3.txt") == (908, 618)
        assert main("input_example.txt") == (10092, 9021)
        assert main("input.txt") == (1415498, 1432898)
    except AssertionError:
        print("❌ wrong")
